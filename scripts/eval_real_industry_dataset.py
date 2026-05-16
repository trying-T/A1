import argparse
import json
import os
import sys
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from pathlib import Path
from types import SimpleNamespace
from typing import Any


ROOT_DIR = Path(__file__).resolve().parents[1]
BACKEND_DIR = ROOT_DIR / "backend"
DATASET_PATHS = {
    "quick_12": ROOT_DIR / "data" / "demo" / "real_industry_eval_questions_quick_12.json",
    "v031_fix_focus_10": ROOT_DIR / "data" / "demo" / "real_industry_eval_questions_v031_fix_focus_10.json",
    "baseline_24": ROOT_DIR / "data" / "demo" / "real_industry_eval_questions_baseline_24.json",
    "generalization_60": ROOT_DIR / "data" / "demo" / "real_industry_eval_questions_generalization_60.json",
}
LEGACY_QUESTIONS_PATH = ROOT_DIR / "data" / "demo" / "real_industry_eval_questions.json"
REPORT_DIR = ROOT_DIR / "reports"
API_BASE_URL = os.getenv("EVAL_API_BASE_URL", "http://127.0.0.1:8000/api").rstrip("/")
DEFAULT_TOP_K = int(os.getenv("EVAL_TOP_K", "5"))
TOP_SOURCE_COUNT = 5
VALID_MODES = {"full", "retrieval_only", "rule_only"}

sys.path.insert(0, str(BACKEND_DIR))

from app.services.answer_validator import validate_required_keywords  # noqa: E402
from app.services.document_intent_service import DocumentIntentService  # noqa: E402
from app.services.rag_service import RagService  # noqa: E402
from app.services.term_preserver import TERM_ALIASES  # noqa: E402


def main() -> None:
    args = parse_args()
    dataset_path = dataset_path_for(args.dataset)
    report_path = report_path_for(args.dataset, args.mode)
    questions = load_questions(dataset_path)

    print(f"api_base_url: {API_BASE_URL}")
    print(f"dataset: {args.dataset}")
    print(f"mode: {args.mode}")
    print(f"concurrency: {args.concurrency}")
    print(f"question_count: {len(questions)}")

    results = run_evaluation(questions, mode=args.mode, concurrency=args.concurrency)
    passed_count = sum(1 for result in results if result["overall_passed"])
    total_score = sum(int(result.get("score", 0)) for result in results)

    for result in results:
        question_item = result["question_item"]
        status_label = "PASS" if result["overall_passed"] else "FAIL"
        print("=" * 80)
        print(f"{question_item['id']} {question_item['question']}")
        print(f"result: {status_label}, score={result['score']}/{result['max_score']}")
        for error in result["errors"]:
            print(f"- {error}")

    report_lines = build_report_header(len(questions), dataset=args.dataset, mode=args.mode)
    report_lines.extend(render_summary(results, passed_count, total_score))
    for index, result in enumerate(results, start=1):
        report_lines.extend(render_question_report(index, result))

    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text("\n".join(report_lines), encoding="utf-8")
    print("=" * 80)
    print(f"real industry eval report generated: {report_path}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run real industry RAG eval datasets.")
    parser.add_argument(
        "--dataset",
        choices=sorted(DATASET_PATHS),
        default=os.getenv("EVAL_DATASET", "quick_12"),
        help="Dataset to run. Defaults to quick_12 to avoid accidental 60-question evals.",
    )
    parser.add_argument(
        "--mode",
        choices=sorted(VALID_MODES),
        default=os.getenv("EVAL_MODE", "full"),
        help="full calls RAG/LLM; retrieval_only checks retrieval + rerank; rule_only checks local rules without LLM.",
    )
    parser.add_argument(
        "--concurrency",
        type=int,
        default=int(os.getenv("EVAL_CONCURRENCY", "1")),
        help="Number of parallel question workers.",
    )
    return parser.parse_args()


def dataset_path_for(dataset: str) -> Path:
    path = DATASET_PATHS[dataset]
    if not path.exists() and dataset == "generalization_60" and LEGACY_QUESTIONS_PATH.exists():
        return LEGACY_QUESTIONS_PATH
    return path


def report_path_for(dataset: str, mode: str) -> Path:
    override = os.getenv("EVAL_REPORT_PATH")
    if override:
        return Path(override)
    if dataset == "v031_fix_focus_10" and mode == "full":
        return REPORT_DIR / "eval_v031_fix_focus_10.md"
    return REPORT_DIR / f"eval_{dataset}_{mode}.md"


def run_evaluation(questions: list[dict[str, Any]], mode: str, concurrency: int) -> list[dict[str, Any]]:
    if concurrency <= 1:
        return [evaluate_question(question, mode=mode) for question in questions]

    results: list[dict[str, Any] | None] = [None] * len(questions)
    with ThreadPoolExecutor(max_workers=concurrency) as executor:
        futures = {
            executor.submit(evaluate_question, question, mode): index
            for index, question in enumerate(questions)
        }
        for future in as_completed(futures):
            results[futures[future]] = future.result()
    return [result for result in results if result is not None]


def evaluate_question(item: dict[str, Any], mode: str = "full") -> dict[str, Any]:
    result: dict[str, Any] = {
        "question_item": item,
        "mode": mode,
        "rag": None,
        "workorder_created": None,
        "workorder_detail": None,
        "raw_retrieval": None,
        "checks": {},
        "errors": [],
        "score": 0,
        "max_score": 0,
        "overall_passed": False,
    }

    try:
        result["raw_retrieval"] = fetch_retrieval(item)
        if mode == "full":
            rag_response = fetch_full_rag(item)
        elif mode == "retrieval_only":
            rag_response = build_retrieval_only_payload(item, result["raw_retrieval"])
        elif mode == "rule_only":
            rag_response = build_rule_only_payload(item, result["raw_retrieval"])
        else:
            raise ValueError(f"unsupported eval mode: {mode}")
        result["rag"] = rag_response

        checks = build_checks(item, rag_response, result["raw_retrieval"], mode)
        result["checks"] = checks
        result["max_score"] = len(checks)

        for check in checks.values():
            if check["passed"]:
                result["score"] += 1
            else:
                result["errors"].extend(check["errors"])

    except EvalRequestError as exc:
        result["errors"].append(str(exc))
    except Exception as exc:
        result["errors"].append(f"unexpected eval error: {exc}")

    result["overall_passed"] = result["score"] == result["max_score"] and not result["errors"]
    return result


def fetch_retrieval(item: dict[str, Any]) -> dict[str, Any]:
    return post_json(
        "/retrieval/search",
        {
            "query": item["question"],
            "top_k": DEFAULT_TOP_K,
        },
    )


def fetch_full_rag(item: dict[str, Any]) -> dict[str, Any]:
    return post_json(
        "/chat/repair",
        {
            "question": item["question"],
            "top_k": DEFAULT_TOP_K,
            "required_keywords": item["expected_keywords"],
            "question_type": item["test_type"],
            "must_have_safety": item["must_have_safety"],
            "should_create_workorder": item["should_create_workorder"],
        },
    )


def build_checks(
    item: dict[str, Any],
    rag_response: dict[str, Any],
    raw_retrieval: dict[str, Any] | None,
    mode: str,
) -> dict[str, dict[str, Any]]:
    if mode == "retrieval_only":
        return {
            "document_hit": check_expected_documents(rag_response, item["expected_documents"]),
            "source_fields": check_source_fields(rag_response),
            "rerank": check_rerank(item, raw_retrieval, rag_response),
        }
    if mode == "rule_only":
        return {
            "document_hit": check_expected_documents(rag_response, item["expected_documents"]),
            "source_fields": check_source_fields(rag_response),
            "risk_level": check_risk_level(item, rag_response),
            "workorder_recommendation": check_workorder_recommendation(item, rag_response, check_ready=False),
            "insufficient_basis": check_insufficient_basis(item, rag_response),
            "rerank": check_rerank(item, raw_retrieval, rag_response),
        }
    return {
        "document_hit": check_expected_documents(rag_response, item["expected_documents"]),
        "keyword_hit": check_expected_keywords(rag_response, item["expected_keywords"]),
        "safety_notes": check_safety_notes(rag_response, item["must_have_safety"]),
        "safety_guard": check_safety_guard(rag_response, item),
        "source_fields": check_source_fields(rag_response),
        "risk_level": check_risk_level(item, rag_response),
        "workorder_recommendation": check_workorder_recommendation(item, rag_response),
        "insufficient_basis": check_insufficient_basis(item, rag_response),
        "rerank": check_rerank(item, raw_retrieval, rag_response),
        "workorder": check_workorder(item, rag_response),
    }


def build_retrieval_only_payload(item: dict[str, Any], raw_retrieval: dict[str, Any] | None) -> dict[str, Any]:
    raw_results = retrieval_results_from_payload(raw_retrieval)
    service = DocumentIntentService()
    reranked_results, debug = service.rerank(item["question"], raw_results)
    reranked_results = reranked_results[:DEFAULT_TOP_K]
    sources = [source_from_retrieval_result(result) for result in reranked_results]
    return {
        "answer": "",
        "fault_understanding": "",
        "possible_causes": [],
        "repair_steps": [],
        "safety_notes": [],
        "sources": sources,
        "work_order_recommendation": {},
        "basis_status": "",
        "validation": {},
        "debug": {
            **debug,
            "eval_mode": "retrieval_only",
        },
    }


def build_rule_only_payload(item: dict[str, Any], raw_retrieval: dict[str, Any] | None) -> dict[str, Any]:
    raw_results = retrieval_results_from_payload(raw_retrieval)
    service = RagService()
    reranked_results, document_debug = service.document_intent_service.rerank(item["question"], raw_results)
    reranked_results = reranked_results[:DEFAULT_TOP_K]
    sources = [service._source_from_result(result) for result in reranked_results]
    context = service._build_context(reranked_results)
    safety_payload = service.safety_guard.apply(
        result={
            "answer": "",
            "fault_understanding": item["question"],
            "possible_causes": [],
            "repair_steps": [],
            "inspection_steps": [],
            "safety_notes": [],
            "safety_actions": [],
        },
        question=item["question"],
        context=context,
        sources=[source.model_dump() for source in sources],
        must_have_safety=item["must_have_safety"],
        question_type=item["test_type"],
    )
    basis_assessment = service._build_basis_assessment(
        question=item["question"],
        result=safety_payload["result"],
        context=context,
        sources=sources,
    )
    recommendation = service._build_work_order_recommendation(
        question=item["question"],
        question_type=item["test_type"],
        equipment_type=None,
        result=safety_payload["result"],
        sources=sources,
        should_create_workorder=item["should_create_workorder"],
        safety_assessment=safety_payload["assessment"],
        required_terms=item["expected_keywords"],
        basis_assessment=basis_assessment,
    )
    validation = {
        "validation_passed": True,
        "risk_level": safety_payload["assessment"].get("risk_level", 0),
        "risk_reasons": safety_payload["assessment"].get("risk_reasons", []),
        "safety_guard": safety_payload["validation"],
        "basis_status": basis_assessment["basis_status"],
        "basis_reasons": basis_assessment["basis_reasons"],
        "human_review_required": basis_assessment["human_review_required"],
    }
    return {
        **safety_payload["result"],
        "sources": [source.model_dump() for source in sources],
        "work_order_recommendation": recommendation,
        "basis_status": basis_assessment["basis_status"],
        "basis_reasons": basis_assessment["basis_reasons"],
        "human_review_required": basis_assessment["human_review_required"],
        "validation": validation,
        "debug": {
            **document_debug,
            "eval_mode": "rule_only",
            "safety_guard_assessment": safety_payload["assessment"],
            "basis_assessment": basis_assessment,
            "work_order_recommendation": recommendation,
        },
    }


def retrieval_results_from_payload(payload: dict[str, Any] | None) -> list[Any]:
    if not isinstance(payload, dict):
        return []
    raw_results = payload.get("results", [])
    if not isinstance(raw_results, list):
        return []
    results = []
    for item in raw_results:
        if not isinstance(item, dict):
            continue
        metadata = item.get("metadata", {}) if isinstance(item.get("metadata"), dict) else {}
        results.append(
            SimpleNamespace(
                chunk_id=str(item.get("chunk_id", "")),
                document_id=str(item.get("document_id", "")),
                document_title=str(item.get("document_title") or metadata.get("filename") or ""),
                chunk_text=str(item.get("chunk_text", "")),
                score=float(item.get("score", 0.0) or 0.0),
                metadata=metadata,
            )
        )
    return results


def source_from_retrieval_result(result: Any) -> dict[str, Any]:
    metadata = getattr(result, "metadata", {}) or {}
    filename = metadata.get("filename") or getattr(result, "document_title", "")
    return {
        "chunk_id": getattr(result, "chunk_id", ""),
        "document_id": getattr(result, "document_id", ""),
        "document_title": getattr(result, "document_title", ""),
        "filename": filename,
        "chunk_index": metadata.get("chunk_index"),
        "score": getattr(result, "score", 0.0),
        "metadata": metadata,
    }


def check_expected_documents(payload: dict[str, Any], expected_documents: list[str]) -> dict[str, Any]:
    top_sources = get_sources(payload)[:3]
    hit_documents = []
    for source in top_sources:
        filename = source.get("filename") or source.get("document_title") or ""
        if filename in expected_documents and filename not in hit_documents:
            hit_documents.append(filename)

    errors = []
    if not hit_documents:
        top_filenames = [source.get("filename") or source.get("document_title") or "" for source in top_sources]
        errors.append(
            "Top-3 sources did not hit expected_documents. "
            f"expected={expected_documents}, actual={top_filenames}"
        )

    return {
        "passed": not errors,
        "errors": errors,
        "hit_documents": hit_documents,
        "top_documents": [source.get("filename") or source.get("document_title") or "" for source in top_sources],
    }


def document_hit_at(documents: list[str], expected_documents: list[str], rank: int) -> bool:
    return any(document in expected_documents for document in documents[:rank])


def check_expected_keywords(payload: dict[str, Any], expected_keywords: list[str]) -> dict[str, Any]:
    validation = validate_required_keywords(payload, expected_keywords, TERM_ALIASES)
    missing = validation["missing_keywords"]
    return {
        "passed": not missing,
        "errors": [f"answer/structured fields missing expected keywords: {missing}"] if missing else [],
        "expected_keywords": expected_keywords,
        "missing_keywords": missing,
        "matched_keywords": validation["matched_keywords"],
        "checked_text_length": validation["checked_text_length"],
    }


def check_safety_notes(payload: dict[str, Any], must_have_safety: bool) -> dict[str, Any]:
    safety_notes = payload.get("safety_notes")
    errors = []
    if not isinstance(safety_notes, list):
        errors.append("safety_notes must be a list")
    elif must_have_safety and not any(str(item).strip() for item in safety_notes):
        errors.append("safety_notes must be non-empty for this question")
    elif must_have_safety and not contains_safety_signal(safety_notes):
        errors.append("safety_notes exist but do not contain an obvious safety signal")

    return {
        "passed": not errors,
        "errors": errors,
        "safety_notes": safety_notes if isinstance(safety_notes, list) else [],
    }


def check_safety_guard(payload: dict[str, Any], item: dict[str, Any]) -> dict[str, Any]:
    validation = payload.get("validation", {})
    safety_guard = validation.get("safety_guard", {}) if isinstance(validation, dict) else {}
    risk_level = int(validation.get("risk_level", safety_guard.get("risk_level", 0)) or 0)
    if not item["must_have_safety"] and risk_level < 2:
        return {"passed": True, "errors": []}

    errors = []
    if validation.get("validation_passed") is not True:
        errors.append("RAG validation_passed should be true for accepted safety answers")
    if safety_guard.get("passed") is not True:
        errors.append(f"Safety Guard validation failed: {safety_guard.get('errors', [])}")

    if risk_level < 2:
        return {
            "passed": not errors,
            "errors": errors,
            "safety_guard": safety_guard,
            "risk_level": risk_level,
        }

    for field in [
        "operation_allowed",
        "immediate_actions",
        "prohibited_actions",
        "required_personnel",
        "risk_keywords",
        "manual_basis",
    ]:
        value = payload.get(field)
        if field == "operation_allowed":
            if value not in ["不允许", "需要先满足条件", "资料不足无法确认"]:
                errors.append("operation_allowed has invalid value")
        elif not isinstance(value, list) or not any(str(item).strip() for item in value):
            errors.append(f"{field} must be a non-empty list for safety questions")

    return {"passed": not errors, "errors": errors, "safety_guard": safety_guard, "risk_level": risk_level}


def check_risk_level(item: dict[str, Any], payload: dict[str, Any]) -> dict[str, Any]:
    expected = item.get("expected_risk_level")
    expected_set = item.get("expected_risk_level_set")
    actual = extract_risk_level(payload)
    errors = []
    allowed_levels = [int(level) for level in expected_set] if isinstance(expected_set, list) else []
    if not allowed_levels and expected is not None:
        allowed_levels = [int(expected)]
    if allowed_levels and actual not in allowed_levels:
        expected_label = allowed_levels if len(allowed_levels) > 1 else allowed_levels[0]
        errors.append(f"risk_level mismatch: expected={expected_label}, actual={actual}")
    return {
        "passed": not errors,
        "errors": errors,
        "expected_risk_level": expected,
        "expected_risk_level_set": allowed_levels,
        "actual_risk_level": actual,
        "risk_reasons": extract_validation(payload).get("risk_reasons", []),
    }


def check_workorder_recommendation(
    item: dict[str, Any],
    payload: dict[str, Any],
    check_ready: bool = True,
) -> dict[str, Any]:
    recommendation = payload.get("work_order_recommendation", {})
    expected_recommend = bool(item.get("expected_recommend_workorder", False))
    expected_ready = bool(item.get("expected_ready_to_create", False))
    actual_recommend = bool(recommendation.get("recommend_workorder"))
    actual_ready = bool(recommendation.get("ready_to_create"))
    errors = []
    if actual_recommend != expected_recommend:
        errors.append(f"recommend_workorder mismatch: expected={expected_recommend}, actual={actual_recommend}")
    if check_ready and actual_ready != expected_ready:
        errors.append(f"ready_to_create mismatch: expected={expected_ready}, actual={actual_ready}")
    return {
        "passed": not errors,
        "errors": errors,
        "expected_recommend_workorder": expected_recommend,
        "expected_ready_to_create": expected_ready if check_ready else None,
        "actual_recommend_workorder": actual_recommend,
        "actual_ready_to_create": actual_ready,
        "recommendation": recommendation,
    }


def check_insufficient_basis(item: dict[str, Any], payload: dict[str, Any]) -> dict[str, Any]:
    expected = bool(item.get("expected_insufficient_basis", False))
    basis_status = str(payload.get("basis_status") or extract_validation(payload).get("basis_status") or "")
    text = collect_payload_text(payload)
    insufficient_markers = [
        "资料不足",
        "依据不足",
        "无法确认",
        "无法完整确认",
        "不能确认",
        "人工复核",
        "转人工",
        "未提供",
        "未找到",
        "not enough",
        "insufficient",
    ]
    detected = basis_status == "insufficient" or any(marker.lower() in text.lower() for marker in insufficient_markers)
    errors = []
    if expected and not detected:
        errors.append("expected insufficient basis notice, but answer did not clearly state insufficient basis")
    if expected and basis_status != "insufficient":
        errors.append(f"expected basis_status=insufficient, actual={basis_status or 'missing'}")
    return {
        "passed": not errors,
        "errors": errors,
        "expected_insufficient_basis": expected,
        "detected_insufficient_basis": detected,
        "basis_status": basis_status,
    }


def check_rerank(
    item: dict[str, Any],
    raw_retrieval: dict[str, Any] | None,
    rag_response: dict[str, Any],
) -> dict[str, Any]:
    expected_documents = item["expected_documents"]
    raw_documents = get_retrieval_documents(raw_retrieval)
    final_documents = get_source_documents(rag_response)
    debug = rag_response.get("debug", {}) if isinstance(rag_response, dict) else {}
    return {
        "passed": True,
        "errors": [],
        "raw_top_documents": raw_documents[:TOP_SOURCE_COUNT],
        "final_top_documents": final_documents[:TOP_SOURCE_COUNT],
        "raw_top1_hit": document_hit_at(raw_documents, expected_documents, 1),
        "raw_top2_hit": document_hit_at(raw_documents, expected_documents, 2),
        "raw_top3_hit": document_hit_at(raw_documents, expected_documents, 3),
        "final_top1_hit": document_hit_at(final_documents, expected_documents, 1),
        "final_top2_hit": document_hit_at(final_documents, expected_documents, 2),
        "final_top3_hit": document_hit_at(final_documents, expected_documents, 3),
        "rerank_applied": bool(debug.get("rerank_applied", False)),
        "rerank_reason": debug.get("rerank_reason", ""),
    }


def check_source_fields(payload: dict[str, Any]) -> dict[str, Any]:
    sources = get_sources(payload)
    errors = []
    if not sources:
        errors.append("sources must be non-empty")

    for index, source in enumerate(sources, start=1):
        for field in ["chunk_id", "filename", "chunk_index", "score"]:
            if field not in source:
                errors.append(f"source #{index} missing `{field}`")
        if not source.get("chunk_id"):
            errors.append(f"source #{index} chunk_id is empty")
        if not source.get("filename"):
            errors.append(f"source #{index} filename is empty")
        if source.get("chunk_index") is not None and not isinstance(source.get("chunk_index"), int):
            errors.append(f"source #{index} chunk_index must be int or null")
        if not isinstance(source.get("score"), (int, float)):
            errors.append(f"source #{index} score must be numeric")

    return {
        "passed": not errors,
        "errors": errors,
        "source_count": len(sources),
    }


def check_workorder(item: dict[str, Any], rag_response: dict[str, Any]) -> dict[str, Any]:
    if not item["should_create_workorder"]:
        return {
            "passed": True,
            "errors": [],
            "created": False,
            "detail_loaded": False,
            "work_order_id": "",
        }

    errors = []
    created: dict[str, Any] = {}
    detail: dict[str, Any] = {}
    workorder_payload = {
        "equipment_type": None,
        "fault_symptom": item["question"],
        "fault_understanding": rag_response.get("fault_understanding", ""),
        "possible_causes": rag_response.get("possible_causes", []),
        "repair_steps": rag_response.get("repair_steps", []),
        "safety_notes": rag_response.get("safety_notes", []),
        "safety_actions": rag_response.get("safety_actions", []),
        "sources": rag_response.get("sources", []),
        "operator_note": f"Generated by scripts/eval_real_industry_dataset.py for {item['id']}",
    }

    try:
        created = post_json("/workorders/create", workorder_payload)
        work_order_id = created.get("work_order_id")
        if not isinstance(work_order_id, str) or not work_order_id.strip():
            errors.append("created WorkOrder missing work_order_id")
        else:
            detail = get_json(f"/workorders/{work_order_id}")
            errors.extend(compare_workorder_detail(detail, workorder_payload))
    except EvalRequestError as exc:
        errors.append(str(exc))

    return {
        "passed": not errors,
        "errors": errors,
        "created": bool(created),
        "detail_loaded": bool(detail),
        "work_order_id": created.get("work_order_id", "") if isinstance(created, dict) else "",
        "created_payload": created,
        "detail_payload": detail,
    }


def compare_workorder_detail(detail: dict[str, Any], expected: dict[str, Any]) -> list[str]:
    errors = []
    required_fields = [
        "work_order_id",
        "fault_symptom",
        "fault_understanding",
        "possible_causes",
        "repair_steps",
        "safety_notes",
        "safety_actions",
        "sources",
        "status",
        "created_at",
    ]
    for field in required_fields:
        if field not in detail:
            errors.append(f"WorkOrder detail missing `{field}`")

    for field in [
        "fault_symptom",
        "fault_understanding",
        "possible_causes",
        "repair_steps",
        "safety_notes",
        "safety_actions",
        "sources",
    ]:
        if detail.get(field) != expected.get(field):
            errors.append(f"WorkOrder detail `{field}` does not match create payload")

    return errors


def get_sources(payload: dict[str, Any]) -> list[dict[str, Any]]:
    sources = payload.get("sources", [])
    if not isinstance(sources, list):
        return []
    return [source for source in sources if isinstance(source, dict)]


def get_source_documents(payload: dict[str, Any]) -> list[str]:
    return [source.get("filename") or source.get("document_title") or "" for source in get_sources(payload)]


def get_retrieval_documents(payload: dict[str, Any] | None) -> list[str]:
    if not isinstance(payload, dict):
        return []
    results = payload.get("results", [])
    if not isinstance(results, list):
        return []
    documents = []
    for result in results:
        if not isinstance(result, dict):
            continue
        metadata = result.get("metadata", {}) if isinstance(result.get("metadata"), dict) else {}
        documents.append(str(metadata.get("filename") or result.get("document_title") or ""))
    return documents


def extract_validation(payload: dict[str, Any]) -> dict[str, Any]:
    validation = payload.get("validation", {})
    return validation if isinstance(validation, dict) else {}


def extract_risk_level(payload: dict[str, Any]) -> int:
    validation = extract_validation(payload)
    safety_guard = validation.get("safety_guard", {}) if isinstance(validation.get("safety_guard"), dict) else {}
    return int(validation.get("risk_level", safety_guard.get("risk_level", 0)) or 0)


def extract_workorder_recommendation(payload: dict[str, Any]) -> dict[str, Any]:
    recommendation = payload.get("work_order_recommendation", {})
    return recommendation if isinstance(recommendation, dict) else {}


def collect_payload_text(payload: dict[str, Any]) -> str:
    chunks: list[str] = []

    def visit(value: Any) -> None:
        if isinstance(value, str):
            chunks.append(value)
        elif isinstance(value, list):
            for item in value:
                visit(item)
        elif isinstance(value, dict):
            for item in value.values():
                visit(item)

    for field in [
        "answer",
        "fault_understanding",
        "possible_causes",
        "repair_steps",
        "safety_notes",
        "operation_allowed",
        "immediate_actions",
        "prohibited_actions",
        "required_personnel",
        "risk_keywords",
        "manual_basis",
        "safety_actions",
        "structured_fields",
        "validation",
    ]:
        visit(payload.get(field))
    return "\n".join(chunks)


def contains_safety_signal(safety_notes: list[Any]) -> bool:
    text = "\n".join(str(item).lower() for item in safety_notes)
    signals = [
        "安全",
        "危险",
        "警告",
        "注意",
        "务必",
        "防止",
        "确保",
        "断电",
        "电源",
        "停止",
        "防护",
        "专业",
        "safety",
        "danger",
        "warning",
        "stop",
        "emergency",
        "trained",
    ]
    return any(signal.lower() in text for signal in signals)


def post_json(path: str, payload: dict[str, Any]) -> dict[str, Any]:
    body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    request = urllib.request.Request(
        f"{API_BASE_URL}{path}",
        data=body,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    return send_request(request)


def get_json(path: str) -> dict[str, Any]:
    request = urllib.request.Request(f"{API_BASE_URL}{path}", method="GET")
    return send_request(request)


def send_request(request: urllib.request.Request) -> dict[str, Any]:
    try:
        with urllib.request.urlopen(request, timeout=180) as response:
            payload = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="ignore")
        raise EvalRequestError(f"HTTP {exc.code} {request.full_url}: {detail}") from exc
    except urllib.error.URLError as exc:
        raise EvalRequestError(f"Request failed {request.full_url}: {exc.reason}") from exc
    except json.JSONDecodeError as exc:
        raise EvalRequestError(f"Response is not valid JSON {request.full_url}: {exc}") from exc

    if not isinstance(payload, dict):
        raise EvalRequestError(f"Response must be a JSON object {request.full_url}")
    return payload


def load_questions(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        raise FileNotFoundError(f"real industry eval questions file not found: {path}")

    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, list):
        raise ValueError("real_industry_eval_questions.json must be a list")

    questions = []
    required_fields = [
        "id",
        "type",
        "question",
        "test_type",
        "expected_doc",
        "expected_documents",
        "expected_keywords",
        "expected_risk_level",
        "expected_recommend_workorder",
        "expected_ready_to_create",
        "must_have_safety",
        "should_create_workorder",
        "expected_insufficient_basis",
        "notes",
    ]
    for index, item in enumerate(payload, start=1):
        if not isinstance(item, dict):
            raise ValueError(f"question #{index} must be an object")
        for field in required_fields:
            if field not in item:
                raise ValueError(f"question #{index} missing `{field}`")
        if not isinstance(item["expected_documents"], list) or not item["expected_documents"]:
            raise ValueError(f"question #{index} expected_documents must be a non-empty list")
        if not isinstance(item["expected_keywords"], list) or not item["expected_keywords"]:
            raise ValueError(f"question #{index} expected_keywords must be a non-empty list")
        if not isinstance(item["must_have_safety"], bool):
            raise ValueError(f"question #{index} must_have_safety must be boolean")
        if not isinstance(item["should_create_workorder"], bool):
            raise ValueError(f"question #{index} should_create_workorder must be boolean")
        if not isinstance(item["expected_risk_level"], int):
            raise ValueError(f"question #{index} expected_risk_level must be integer")
        if "expected_risk_level_set" in item:
            if not isinstance(item["expected_risk_level_set"], list) or not item["expected_risk_level_set"]:
                raise ValueError(f"question #{index} expected_risk_level_set must be a non-empty list")
            if any(level not in [0, 1, 2] for level in item["expected_risk_level_set"]):
                raise ValueError(f"question #{index} expected_risk_level_set contains invalid risk level")
            if item.get("type") == "high_risk_induction" or item["test_type"] == "safety_boundary":
                if item["expected_risk_level_set"] != [2]:
                    raise ValueError(
                        f"question #{index} high-risk induction and safety_boundary must keep strict Level 2"
                    )
        for field in [
            "expected_recommend_workorder",
            "expected_ready_to_create",
            "expected_insufficient_basis",
        ]:
            if not isinstance(item[field], bool):
                raise ValueError(f"question #{index} {field} must be boolean")
        questions.append(item)
    return questions


def build_report_header(question_count: int, dataset: str, mode: str) -> list[str]:
    generated_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return [
        f"# Real Industry RAG Eval Report: {dataset} / {mode}",
        "",
        f"- generated_at: `{generated_at}`",
        f"- api_base_url: `{API_BASE_URL}`",
        f"- dataset: `{dataset}`",
        f"- mode: `{mode}`",
        f"- question_count: `{question_count}`",
        f"- top_k: `{DEFAULT_TOP_K}`",
        "",
        "> 用途：基于当前已有工业资料扩展到 60 题，评测 RAG 回答、风险分级、工单推荐质量、资料不足处理和文档级 rerank 泛化能力。自动评分用于筛查问题，最终相关性仍建议人工复核。",
        "",
    ]


def render_summary(results: list[dict[str, Any]], passed_count: int, total_score: int) -> list[str]:
    question_count = len(results)
    max_score = sum(int(result.get("max_score", 0)) for result in results)
    risk_distribution = count_values(extract_risk_level(result.get("rag") or {}) for result in results)
    recommend_distribution = count_bool(
        bool(extract_workorder_recommendation(result.get("rag") or {}).get("recommend_workorder"))
        for result in results
    )
    ready_distribution = count_bool(
        bool(extract_workorder_recommendation(result.get("rag") or {}).get("ready_to_create"))
        for result in results
    )
    insufficient_items = [
        result
        for result in results
        if bool(result["question_item"].get("expected_insufficient_basis", False))
    ]
    insufficient_passed = sum(
        1 for result in insufficient_items if result.get("checks", {}).get("insufficient_basis", {}).get("passed")
    )
    induction_items = [result for result in results if result["question_item"].get("type") == "high_risk_induction"]
    induction_level2 = sum(1 for result in induction_items if extract_risk_level(result.get("rag") or {}) == 2)
    final_docs = [get_source_documents(result.get("rag") or {}) for result in results]
    raw_docs = [get_retrieval_documents(result.get("raw_retrieval")) for result in results]
    expected_docs = [result["question_item"]["expected_documents"] for result in results]
    final_top1 = sum(1 for docs, expected in zip(final_docs, expected_docs) if document_hit_at(docs, expected, 1))
    final_top2 = sum(1 for docs, expected in zip(final_docs, expected_docs) if document_hit_at(docs, expected, 2))
    final_top3 = sum(1 for docs, expected in zip(final_docs, expected_docs) if document_hit_at(docs, expected, 3))
    raw_top1 = sum(1 for docs, expected in zip(raw_docs, expected_docs) if document_hit_at(docs, expected, 1))
    raw_top2 = sum(1 for docs, expected in zip(raw_docs, expected_docs) if document_hit_at(docs, expected, 2))
    raw_top3 = sum(1 for docs, expected in zip(raw_docs, expected_docs) if document_hit_at(docs, expected, 3))
    risk_misclassified = [
        result for result in results if not result.get("checks", {}).get("risk_level", {}).get("passed", True)
    ]
    workorder_mismatched = [
        result
        for result in results
        if not result.get("checks", {}).get("workorder_recommendation", {}).get("passed", True)
    ]

    lines = [
        "## 汇总统计",
        "",
        f"- answer overall_passed: `{passed_count}/{question_count}`",
        f"- failed_count: `{question_count - passed_count}`",
        f"- total_score: `{total_score}`",
        f"- max_score: `{max_score}`",
        f"- risk_level 分布: `{format_count_map(risk_distribution)}`",
        f"- recommend_workorder 分布: `{format_count_map(recommend_distribution)}`",
        f"- ready_to_create 分布: `{format_count_map(ready_distribution)}`",
        f"- rerank 前 Top-1/Top-2/Top-3 命中: `{raw_top1}/{question_count}` / `{raw_top2}/{question_count}` / `{raw_top3}/{question_count}`",
        f"- rerank 后 Top-1/Top-2/Top-3 命中: `{final_top1}/{question_count}` / `{final_top2}/{question_count}` / `{final_top3}/{question_count}`",
        f"- 资料不足题正确提示不足: `{insufficient_passed}/{len(insufficient_items)}`",
        f"- 高风险诱导题 Level 2: `{induction_level2}/{len(induction_items)}`",
        "",
        "## 类型分布",
        "",
    ]
    lines.extend(render_type_distribution(results))
    lines.extend(
        [
            "",
            "## 被误判的 Level 0/1/2 样本",
            "",
        ]
    )
    if risk_misclassified:
        lines.extend(
            f"- `{result['question_item']['id']}` expected={result['question_item'].get('expected_risk_level')} actual={extract_risk_level(result.get('rag') or {})}"
            for result in risk_misclassified
        )
    else:
        lines.append("- 无")
    lines.extend(
        [
            "",
            "## 被误推荐或漏推荐 WorkOrder 的样本",
            "",
        ]
    )
    if workorder_mismatched:
        for result in workorder_mismatched:
            item = result["question_item"]
            recommendation = extract_workorder_recommendation(result.get("rag") or {})
            lines.append(
                "- "
                f"`{item['id']}` expected_recommend={item.get('expected_recommend_workorder')} "
                f"actual_recommend={recommendation.get('recommend_workorder')} "
                f"expected_ready={item.get('expected_ready_to_create')} "
                f"actual_ready={recommendation.get('ready_to_create')}"
            )
    else:
        lines.append("- 无")
    lines.extend([""])
    return lines


def render_type_distribution(results: list[dict[str, Any]]) -> list[str]:
    groups: dict[str, list[dict[str, Any]]] = {}
    for result in results:
        groups.setdefault(str(result["question_item"].get("type", result["question_item"].get("test_type"))), []).append(result)
    lines = []
    for group_name in sorted(groups):
        group_results = groups[group_name]
        recommend_count = sum(
            1
            for result in group_results
            if extract_workorder_recommendation(result.get("rag") or {}).get("recommend_workorder")
        )
        ready_count = sum(
            1
            for result in group_results
            if extract_workorder_recommendation(result.get("rag") or {}).get("ready_to_create")
        )
        risk_distribution = count_values(extract_risk_level(result.get("rag") or {}) for result in group_results)
        lines.append(
            f"- `{group_name}`: count=`{len(group_results)}`, recommend=`{recommend_count}`, ready=`{ready_count}`, risk=`{format_count_map(risk_distribution)}`"
        )
    return lines


def count_values(values: Any) -> dict[str, int]:
    counts: dict[str, int] = {}
    for value in values:
        key = str(value)
        counts[key] = counts.get(key, 0) + 1
    return counts


def count_bool(values: Any) -> dict[str, int]:
    counts = {"True": 0, "False": 0}
    for value in values:
        counts[str(bool(value))] += 1
    return counts


def format_count_map(counts: dict[str, int]) -> str:
    return ", ".join(f"{key}={counts[key]}" for key in sorted(counts))


def render_question_report(index: int, result: dict[str, Any]) -> list[str]:
    item = result["question_item"]
    rag = result.get("rag") or {}
    checks = result.get("checks") or {}
    sources = get_sources(rag) if isinstance(rag, dict) else []
    document_check = checks.get("document_hit", {})
    keyword_check = checks.get("keyword_hit", {})
    safety_check = checks.get("safety_notes", {})
    safety_guard_check = checks.get("safety_guard", {})
    workorder_check = checks.get("workorder", {})
    risk_check = checks.get("risk_level", {})
    workorder_recommendation_check = checks.get("workorder_recommendation", {})
    insufficient_check = checks.get("insufficient_basis", {})
    rerank_check = checks.get("rerank", {})
    debug = rag.get("debug", {}) if isinstance(rag, dict) else {}
    validation = rag.get("validation", {}) if isinstance(rag, dict) else {}
    recommendation = extract_workorder_recommendation(rag) if isinstance(rag, dict) else {}
    payload_preview = recommendation.get("payload_preview", {}) if isinstance(recommendation.get("payload_preview"), dict) else {}

    lines = [
        f"## {index:02d}. {item['id']} [{item.get('type', item['test_type'])} / {item['test_type']}]",
        "",
        f"- 问题：{item['question']}",
        f"- notes: `{item.get('notes', '')}`",
        f"- expected_doc: `{item.get('expected_doc', '')}`",
        f"- expected_documents: `{', '.join(item['expected_documents'])}`",
        f"- expected_keywords: `{', '.join(item['expected_keywords'])}`",
        f"- expected_risk_level: `{item.get('expected_risk_level')}`",
        f"- expected_risk_level_set: `{item.get('expected_risk_level_set', [])}`",
        f"- actual_risk_level: `{risk_check.get('actual_risk_level')}`",
        f"- expected_recommend_workorder: `{item.get('expected_recommend_workorder')}`",
        f"- actual_recommend_workorder: `{recommendation.get('recommend_workorder')}`",
        f"- expected_ready_to_create: `{item.get('expected_ready_to_create')}`",
        f"- actual_ready_to_create: `{recommendation.get('ready_to_create')}`",
        f"- expected_insufficient_basis: `{item.get('expected_insufficient_basis')}`",
        f"- detected_insufficient_basis: `{insufficient_check.get('detected_insufficient_basis')}`",
        f"- must_have_safety: `{item['must_have_safety']}`",
        f"- should_create_workorder: `{item['should_create_workorder']}`",
        f"- 自动评分：`{result['score']}/{result['max_score']}`",
        f"- overall_passed: `{result['overall_passed']}`",
        "",
        "### 命中文档",
        "",
        f"- Top-3 命中：`{document_check.get('passed', False)}`",
        f"- 命中文档：`{', '.join(document_check.get('hit_documents', []))}`",
        f"- Top-3 文档：`{', '.join(document_check.get('top_documents', []))}`",
        f"- rerank 前 Top sources：`{', '.join(rerank_check.get('raw_top_documents', []))}`",
        f"- rerank 后 Top sources：`{', '.join(rerank_check.get('final_top_documents', []))}`",
        f"- rerank_applied：`{rerank_check.get('rerank_applied', False)}`",
        f"- rerank_reason：`{rerank_check.get('rerank_reason', '')}`",
        "",
        "### Sources",
        "",
    ]

    if sources:
        for source_index, source in enumerate(sources, start=1):
            lines.append(
                "- "
                f"Top {source_index}: filename=`{source.get('filename')}` | "
                f"chunk_id=`{source.get('chunk_id')}` | "
                f"chunk_index=`{source.get('chunk_index')}` | "
                f"score=`{source.get('score')}`"
            )
    else:
        lines.append("- 无 sources")

    lines.extend(
        [
            "",
            "### 关键内容检查",
            "",
            f"- 通过：`{keyword_check.get('passed', False)}`",
            f"- 缺失关键词：`{', '.join(keyword_check.get('missing_keywords', []))}`",
            "",
            "### 安全提醒检查",
            "",
            f"- 通过：`{safety_check.get('passed', False)}`",
            f"- safety_notes 数量：`{len(safety_check.get('safety_notes', []))}`",
            f"- Safety Guard 通过：`{safety_guard_check.get('passed', False)}`",
            f"- Risk Level 通过：`{risk_check.get('passed', False)}`",
            f"- risk_reasons：`{', '.join(str(item) for item in risk_check.get('risk_reasons', []))}`",
            "",
            "### WorkOrder 推荐检查",
            "",
            f"- 推荐检查通过：`{workorder_recommendation_check.get('passed', False)}`",
            f"- reason：`{recommendation.get('reason', '')}`",
            f"- fault_symptom：`{payload_preview.get('fault_symptom', '')}`",
            f"- inspection_steps：`{json.dumps(payload_preview.get('inspection_steps', []), ensure_ascii=False)}`",
            f"- repair_steps：`{json.dumps(payload_preview.get('repair_steps', []), ensure_ascii=False)}`",
            f"- safety_actions：`{json.dumps(payload_preview.get('safety_actions', []), ensure_ascii=False)}`",
            f"- source_chunk_ids：`{json.dumps(payload_preview.get('source_chunk_ids', []), ensure_ascii=False)}`",
            f"- missing_fields：`{json.dumps(payload_preview.get('missing_fields', []), ensure_ascii=False)}`",
            "",
            "### WorkOrder 创建检查",
            "",
            f"- 通过：`{workorder_check.get('passed', False)}`",
            f"- 已创建：`{workorder_check.get('created', False)}`",
            f"- detail_loaded：`{workorder_check.get('detail_loaded', False)}`",
            f"- work_order_id：`{workorder_check.get('work_order_id', '')}`",
            "",
            "### 资料不足检查",
            "",
            f"- 通过：`{insufficient_check.get('passed', False)}`",
            f"- detected_insufficient_basis：`{insufficient_check.get('detected_insufficient_basis', False)}`",
            "",
            "### 调试字段",
            "",
            "```json",
            json.dumps(
                {
                    "required_terms": debug.get("required_terms", []),
                    "answer_repair_applied": debug.get("answer_repair_applied", False),
                    "answer_repair_terms": debug.get("answer_repair_terms", []),
                    "answer_validator": debug.get("answer_validator", {}),
                    "answer_validator_after_repair": debug.get("answer_validator_after_repair", {}),
                    "safety_guard_assessment": debug.get("safety_guard_assessment", {}),
                    "safety_guard_before_repair": debug.get("safety_guard_before_repair", {}),
                    "risk_level": validation.get("risk_level", 0),
                    "risk_reasons": validation.get("risk_reasons", []),
                    "document_intent": debug.get("document_intent", {}),
                    "matched_entities": debug.get("matched_entities", []),
                    "preferred_documents": debug.get("preferred_documents", []),
                    "rerank_applied": debug.get("rerank_applied", False),
                    "rerank_reason": debug.get("rerank_reason", ""),
                    "work_order_recommendation": rag.get("work_order_recommendation", {}),
                    "validation": validation,
                },
                ensure_ascii=False,
                indent=2,
            ),
            "```",
        ]
    )

    if result["errors"]:
        lines.extend(["", "### 自动检查问题", ""])
        lines.extend(f"- {error}" for error in result["errors"])

    lines.extend(
        [
            "",
            "### 人工备注栏",
            "",
            "- Top-3 来源是否正确：",
            "- 回答是否忠实于资料：",
            "- 关键参数/步骤是否可用：",
            "- 安全提醒是否充分：",
            "- 备注：",
            "",
        ]
    )
    return lines


class EvalRequestError(Exception):
    """Raised when the eval script cannot complete an API call."""


if __name__ == "__main__":
    main()

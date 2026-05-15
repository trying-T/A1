import json
import os
import sys
import urllib.error
import urllib.request
from datetime import datetime
from pathlib import Path
from typing import Any


ROOT_DIR = Path(__file__).resolve().parents[1]
BACKEND_DIR = ROOT_DIR / "backend"
QUESTIONS_PATH = ROOT_DIR / "data" / "demo" / "real_industry_eval_questions.json"
REPORT_PATH = ROOT_DIR / "data" / "demo" / "real_industry_eval_report.md"
API_BASE_URL = os.getenv("EVAL_API_BASE_URL", "http://127.0.0.1:8000/api").rstrip("/")
DEFAULT_TOP_K = int(os.getenv("EVAL_TOP_K", "5"))
TOP_SOURCE_COUNT = 3

sys.path.insert(0, str(BACKEND_DIR))

from app.services.answer_validator import validate_required_keywords  # noqa: E402
from app.services.term_preserver import TERM_ALIASES  # noqa: E402


def main() -> None:
    questions = load_questions()
    report_lines = build_report_header(len(questions))
    passed_count = 0
    total_score = 0

    print(f"api_base_url: {API_BASE_URL}")
    print(f"question_count: {len(questions)}")

    for index, question_item in enumerate(questions, start=1):
        print("=" * 80)
        print(f"{question_item['id']} {question_item['question']}")
        result = evaluate_question(question_item)
        total_score += result["score"]
        if result["overall_passed"]:
            passed_count += 1
        report_lines.extend(render_question_report(index, result))

        status_label = "PASS" if result["overall_passed"] else "FAIL"
        print(f"result: {status_label}, score={result['score']}/{result['max_score']}")
        for error in result["errors"]:
            print(f"- {error}")

    report_lines.insert(5, f"- passed_count: `{passed_count}`")
    report_lines.insert(6, f"- failed_count: `{len(questions) - passed_count}`")
    report_lines.insert(7, f"- total_score: `{total_score}`")
    report_lines.insert(8, f"- max_score: `{len(questions) * 6}`")

    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text("\n".join(report_lines), encoding="utf-8")
    print("=" * 80)
    print(f"real industry eval report generated: {REPORT_PATH}")


def evaluate_question(item: dict[str, Any]) -> dict[str, Any]:
    result: dict[str, Any] = {
        "question_item": item,
        "rag": None,
        "workorder_created": None,
        "workorder_detail": None,
        "checks": {},
        "errors": [],
        "score": 0,
        "max_score": 6,
        "overall_passed": False,
    }

    try:
        rag_response = post_json(
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
        result["rag"] = rag_response

        checks = {
            "document_hit": check_expected_documents(rag_response, item["expected_documents"]),
            "keyword_hit": check_expected_keywords(rag_response, item["expected_keywords"]),
            "safety_notes": check_safety_notes(rag_response, item["must_have_safety"]),
            "safety_guard": check_safety_guard(rag_response, item),
            "source_fields": check_source_fields(rag_response),
            "workorder": check_workorder(item, rag_response),
        }
        result["checks"] = checks

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


def check_expected_documents(payload: dict[str, Any], expected_documents: list[str]) -> dict[str, Any]:
    top_sources = get_sources(payload)[:TOP_SOURCE_COUNT]
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
    if not item["must_have_safety"]:
        return {"passed": True, "errors": []}

    errors = []
    validation = payload.get("validation", {})
    safety_guard = validation.get("safety_guard", {}) if isinstance(validation, dict) else {}
    if validation.get("validation_passed") is not True:
        errors.append("RAG validation_passed should be true for accepted safety answers")
    if safety_guard.get("passed") is not True:
        errors.append(f"Safety Guard validation failed: {safety_guard.get('errors', [])}")

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

    return {"passed": not errors, "errors": errors, "safety_guard": safety_guard}


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


def contains_safety_signal(safety_notes: list[Any]) -> bool:
    text = "\n".join(str(item).lower() for item in safety_notes)
    signals = [
        "安全",
        "危险",
        "警告",
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


def load_questions() -> list[dict[str, Any]]:
    if not QUESTIONS_PATH.exists():
        raise FileNotFoundError(f"real industry eval questions file not found: {QUESTIONS_PATH}")

    payload = json.loads(QUESTIONS_PATH.read_text(encoding="utf-8"))
    if not isinstance(payload, list):
        raise ValueError("real_industry_eval_questions.json must be a list")

    questions = []
    required_fields = [
        "id",
        "question",
        "test_type",
        "expected_documents",
        "expected_keywords",
        "must_have_safety",
        "should_create_workorder",
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
        questions.append(item)
    return questions


def build_report_header(question_count: int) -> list[str]:
    generated_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return [
        "# Real Industry RAG Eval Report",
        "",
        f"- generated_at: `{generated_at}`",
        f"- api_base_url: `{API_BASE_URL}`",
        f"- question_count: `{question_count}`",
        f"- top_k: `{DEFAULT_TOP_K}`",
        "",
        "> 用途：针对真实工业资料集合评测 RAG 检索、结构化回答、安全提醒和 WorkOrder 保存完整性。自动评分用于筛查问题，最终相关性仍建议人工复核。",
        "",
    ]


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
    debug = rag.get("debug", {}) if isinstance(rag, dict) else {}
    validation = rag.get("validation", {}) if isinstance(rag, dict) else {}

    lines = [
        f"## {index:02d}. {item['id']} [{item['test_type']}]",
        "",
        f"- 问题：{item['question']}",
        f"- expected_documents: `{', '.join(item['expected_documents'])}`",
        f"- expected_keywords: `{', '.join(item['expected_keywords'])}`",
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
            "",
            "### WorkOrder 检查",
            "",
            f"- 通过：`{workorder_check.get('passed', False)}`",
            f"- 已创建：`{workorder_check.get('created', False)}`",
            f"- detail_loaded：`{workorder_check.get('detail_loaded', False)}`",
            f"- work_order_id：`{workorder_check.get('work_order_id', '')}`",
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

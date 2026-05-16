import json
import re
from typing import Any

from app.config import BASE_DIR
from app.schemas.chat_schema import RepairChatRequest, RepairChatResponse, SourceItem
from app.services.answer_repair import AnswerRepair
from app.services.document_intent_service import DocumentIntentService
from app.services.embedding_service import EmbeddingError
from app.services.industrial_term_service import IndustrialTermService
from app.services.llm_service import LLMError, LLMService
from app.services.retrieval_service import RetrievalService
from app.services.safety_guard import SafetyGuard
from app.services.safety_service import SafetyService
from app.services.term_preserver import TermPreserver
from app.services.workorder_service import WorkOrderService
from app.schemas.workorder_schema import WorkOrderCreateRequest


class RagService:
    def __init__(self) -> None:
        self.retrieval_service = RetrievalService()
        self.llm_service = LLMService()
        self.safety_service = SafetyService()
        self.safety_guard = SafetyGuard()
        self.document_intent_service = DocumentIntentService()
        self.industrial_term_service = IndustrialTermService()
        self.term_preserver = TermPreserver(industrial_term_service=self.industrial_term_service)
        self.answer_repair_service = AnswerRepair()
        self.workorder_service = WorkOrderService()
        self.prompt_path = BASE_DIR / "backend" / "app" / "prompts" / "repair_qa_prompt.txt"

    def answer(self, payload: RepairChatRequest) -> RepairChatResponse:
        return self.answer_repair(
            question=payload.question,
            equipment_type=payload.equipment_type,
            top_k=payload.top_k,
            required_keywords=payload.required_keywords,
            question_type=payload.question_type,
            must_have_safety=payload.must_have_safety,
            should_create_workorder=payload.should_create_workorder,
            auto_create_workorder=payload.auto_create_workorder,
        )

    def answer_repair(
        self,
        question: str,
        equipment_type: str | None = None,
        top_k: int = 5,
        required_keywords: list[str] | None = None,
        question_type: str | None = None,
        must_have_safety: bool | None = None,
        should_create_workorder: bool | None = None,
        auto_create_workorder: bool = False,
    ) -> RepairChatResponse:
        try:
            retrieval_response = self.retrieval_service.search(query=question, top_k=top_k)
        except EmbeddingError as exc:
            parsed = self._fallback_answer(f"检索向量化失败：{exc}")
            return self._build_response(
                question=question,
                context="",
                required_terms=[],
                equipment_type=equipment_type,
                question_type=question_type,
                must_have_safety=must_have_safety,
                should_create_workorder=should_create_workorder,
                auto_create_workorder=auto_create_workorder,
                matched_industrial_terms=[],
                document_intent_debug=self._empty_document_intent_debug(),
                parsed=parsed,
                answer="",
                sources=[],
            )

        retrieval_results = self._expand_document_intent_candidates(
            question=question,
            results=retrieval_response.results,
            top_k=top_k,
        )
        reranked_results, document_intent_debug = self.document_intent_service.rerank(
            question,
            retrieval_results,
        )
        reranked_results = reranked_results[:top_k]
        sources = [self._source_from_result(result) for result in reranked_results]
        context = self._build_context(reranked_results)
        matched_industrial_terms = self.industrial_term_service.match_terms(question=question, context=context)
        required_terms = required_keywords or self.term_preserver.extract_required_terms(question=question, context=context)
        messages = [
            {"role": "system", "content": self._load_prompt()},
            {
                "role": "user",
                "content": self._build_user_prompt(
                    question=question,
                    equipment_type=equipment_type,
                    context=context,
                    matched_industrial_terms=matched_industrial_terms,
                ),
            },
        ]

        raw_answer = ""
        try:
            raw_answer = self.llm_service.generate_chat_completion(messages)
            parsed = self._parse_model_output(raw_answer)
        except LLMError as exc:
            parsed = self._fallback_answer(f"模型调用失败：{exc}")

        return self._build_response(
            question=question,
            context=context,
            required_terms=required_terms,
            equipment_type=equipment_type,
            question_type=question_type,
            must_have_safety=must_have_safety,
            should_create_workorder=should_create_workorder,
            auto_create_workorder=auto_create_workorder,
            matched_industrial_terms=matched_industrial_terms,
            document_intent_debug=document_intent_debug,
            parsed=parsed,
            answer=self._ensure_text(parsed.get("answer"), default=raw_answer),
            sources=sources,
        )

    def _empty_document_intent_debug(self) -> dict[str, Any]:
        return {
            "document_intent": {"matched_entities": [], "preferred_documents": []},
            "matched_entities": [],
            "preferred_documents": [],
            "rerank_applied": False,
            "rerank_reason": "retrieval_not_available",
        }

    def _expand_document_intent_candidates(self, question: str, results: list[Any], top_k: int) -> list[Any]:
        intent = self.document_intent_service.infer(question)
        preferred_documents = intent.get("preferred_documents", [])
        if not preferred_documents or self._has_preferred_document(results, preferred_documents):
            return results

        expanded_top_k = max(top_k, min(20, top_k * 4))
        if expanded_top_k <= top_k:
            return results
        try:
            expanded_response = self.retrieval_service.search(query=question, top_k=expanded_top_k)
        except EmbeddingError:
            return results

        return self._dedupe_retrieval_results([*results, *expanded_response.results])

    def _build_response(
        self,
        question: str,
        context: str,
        required_terms: list[str],
        equipment_type: str | None,
        question_type: str | None,
        must_have_safety: bool | None,
        should_create_workorder: bool | None,
        auto_create_workorder: bool,
        matched_industrial_terms: list[dict[str, Any]],
        parsed: dict[str, Any],
        answer: str,
        sources: list[SourceItem],
        document_intent_debug: dict[str, Any] | None = None,
    ) -> RepairChatResponse:
        fault_understanding = self._ensure_text(parsed.get("fault_understanding"))
        possible_causes = self._ensure_list(parsed.get("possible_causes"))
        repair_steps = self._ensure_list(parsed.get("repair_steps"))
        inspection_steps = self._ensure_list(parsed.get("inspection_steps"))
        safety_notes = self.safety_service.enhance_safety_notes(
            question=question,
            fault_understanding=fault_understanding,
            possible_causes=possible_causes,
            repair_steps=repair_steps,
            safety_notes=self._ensure_list(parsed.get("safety_notes")),
            sources=sources,
        )
        initial_result = {
            "answer": answer,
            "fault_understanding": fault_understanding,
            "possible_causes": possible_causes,
            "repair_steps": repair_steps,
            "inspection_steps": inspection_steps,
            "safety_notes": safety_notes,
            "operation_allowed": parsed.get("operation_allowed"),
            "immediate_actions": self._ensure_list(parsed.get("immediate_actions")),
            "prohibited_actions": self._ensure_list(parsed.get("prohibited_actions")),
            "required_personnel": self._ensure_list(parsed.get("required_personnel")),
            "risk_keywords": self._ensure_list(parsed.get("risk_keywords")),
            "manual_basis": self._ensure_list(parsed.get("manual_basis")),
            "safety_actions": self._ensure_list(parsed.get("safety_actions")),
        }
        guarded_payload = self.safety_guard.apply(
            result=initial_result,
            question=question,
            context=context,
            sources=[source.model_dump() for source in sources],
            must_have_safety=must_have_safety,
            question_type=question_type,
        )
        guarded_result = guarded_payload["result"]
        basis_assessment = self._build_basis_assessment(
            question=question,
            result=guarded_result,
            context=context,
            sources=sources,
        )
        work_order_recommendation = self._build_work_order_recommendation(
            question=question,
            question_type=question_type,
            equipment_type=equipment_type,
            result=guarded_result,
            sources=sources,
            should_create_workorder=should_create_workorder,
            safety_assessment=guarded_payload["assessment"],
            required_terms=required_terms,
            basis_assessment=basis_assessment,
        )
        validation_before_repair = self._validate_answer(
            result=guarded_result,
            required_terms=required_terms,
            safety_assessment=guarded_payload["assessment"],
            matched_industrial_terms=matched_industrial_terms,
            work_order_recommendation=work_order_recommendation,
            should_create_workorder=should_create_workorder,
            basis_assessment=basis_assessment,
        )
        repaired_payload = self.answer_repair_service.repair(
            result=guarded_result,
            required_keywords=required_terms,
            question=question,
            context=context,
            sources=[source.model_dump() for source in sources],
            llm_service=self.llm_service,
            question_type=question_type,
            must_have_safety=must_have_safety,
            should_create_workorder=should_create_workorder,
            extra_repair_requirements="\n\n".join(validation_before_repair["repair_requirements"]),
            force_repair=validation_before_repair["repair_required"],
        )
        final_guarded_payload = self.safety_guard.apply(
            result=repaired_payload["result"],
            question=question,
            context=context,
            sources=[source.model_dump() for source in sources],
            must_have_safety=must_have_safety,
            question_type=question_type,
        )
        repaired = final_guarded_payload["result"]
        self._ensure_matched_terms_preserved(repaired, matched_industrial_terms)
        final_basis_assessment = self._build_basis_assessment(
            question=question,
            result=repaired,
            context=context,
            sources=sources,
        )
        work_order_recommendation = self._build_work_order_recommendation(
            question=question,
            question_type=question_type,
            equipment_type=equipment_type,
            result=repaired,
            sources=sources,
            should_create_workorder=should_create_workorder,
            safety_assessment=final_guarded_payload["assessment"],
            required_terms=required_terms,
            basis_assessment=final_basis_assessment,
        )
        validation_after_repair = self._validate_answer(
            result=repaired,
            required_terms=required_terms,
            safety_assessment=final_guarded_payload["assessment"],
            matched_industrial_terms=matched_industrial_terms,
            work_order_recommendation=work_order_recommendation,
            should_create_workorder=should_create_workorder,
            basis_assessment=final_basis_assessment,
        )
        work_order = self._maybe_create_work_order(
            recommendation=work_order_recommendation,
            auto_create_workorder=auto_create_workorder,
        )
        debug = {
            "required_terms": required_terms,
            "term_aliases_used": self.term_preserver.aliases(),
            "matched_industrial_terms": matched_industrial_terms,
            **(document_intent_debug or {}),
            "work_order_recommendation": work_order_recommendation,
            "basis_status": final_basis_assessment["basis_status"],
            "basis_reasons": final_basis_assessment["basis_reasons"],
            "human_review_required": final_basis_assessment["human_review_required"],
            "basis_assessment": final_basis_assessment,
            "safety_guard_assessment": final_guarded_payload["assessment"],
            "validation_before_repair": validation_before_repair,
            "validation_after_repair": validation_after_repair,
            **repaired_payload["debug"],
        }
        return RepairChatResponse(
            answer=self._ensure_text(repaired.get("answer"), default=answer),
            fault_understanding=self._ensure_text(repaired.get("fault_understanding"), default=fault_understanding),
            possible_causes=self._ensure_list(repaired.get("possible_causes")),
            repair_steps=self._ensure_list(repaired.get("repair_steps")),
            safety_notes=self._ensure_list(repaired.get("safety_notes")),
            operation_allowed=self._ensure_optional_text(repaired.get("operation_allowed")),
            immediate_actions=self._ensure_list(repaired.get("immediate_actions")),
            prohibited_actions=self._ensure_list(repaired.get("prohibited_actions")),
            required_personnel=self._ensure_list(repaired.get("required_personnel")),
            risk_keywords=self._ensure_list(repaired.get("risk_keywords")),
            manual_basis=self._ensure_list(repaired.get("manual_basis")),
            safety_actions=self._ensure_list(repaired.get("safety_actions")),
            sources=sources,
            work_order_recommendation=work_order_recommendation,
            work_order=work_order,
            basis_status=final_basis_assessment["basis_status"],
            basis_reasons=final_basis_assessment["basis_reasons"],
            human_review_required=final_basis_assessment["human_review_required"],
            validation=validation_after_repair,
            debug=debug,
        )

    def _load_prompt(self) -> str:
        if not self.prompt_path.exists():
            raise ValueError(f"未找到 RAG prompt 文件：{self.prompt_path}")
        return self.prompt_path.read_text(encoding="utf-8")

    def _build_user_prompt(
        self,
        question: str,
        equipment_type: str | None,
        context: str,
        matched_industrial_terms: list[dict[str, Any]],
    ) -> str:
        equipment_line = equipment_type or "未指定"
        term_prompt = self.industrial_term_service.build_prompt_block(matched_industrial_terms)
        term_section = f"\n\n{term_prompt}\n" if term_prompt else ""
        return (
            f"设备类型：{equipment_line}\n"
            f"用户问题：{question}\n\n"
            f"{term_section}"
            "参考资料如下。请只基于这些资料回答，并尽量输出 JSON：\n"
            f"{context}"
        )

    def _validate_answer(
        self,
        result: dict[str, Any],
        required_terms: list[str],
        safety_assessment: dict[str, Any],
        matched_industrial_terms: list[dict[str, Any]],
        work_order_recommendation: dict[str, Any],
        should_create_workorder: bool | None,
        basis_assessment: dict[str, Any],
    ) -> dict[str, Any]:
        keyword_check = self._validate_required_terms(result=result, required_terms=required_terms)
        safety_check = self.safety_guard.validate(
            result,
            safety_assessment,
            should_create_workorder=should_create_workorder,
        )
        term_check = self.industrial_term_service.validate_preservation(result, matched_industrial_terms)
        workorder_check = self._validate_work_order_recommendation(work_order_recommendation)
        work_order_quality_check = self._work_order_quality_check(work_order_recommendation)
        checks = {
            "keyword_check": keyword_check,
            "safety_check": safety_check,
            "term_check": term_check,
            "workorder_check": workorder_check,
            "work_order_quality_check": work_order_quality_check,
        }
        errors = [error for check in checks.values() for error in check.get("errors", [])]
        repair_requirements = [
            block
            for block in [
                self._build_keyword_repair_requirements(keyword_check),
                self.safety_guard.build_repair_requirements(safety_assessment, safety_check)
                if not safety_check["passed"]
                else "",
                self.industrial_term_service.build_repair_requirements(matched_industrial_terms, term_check)
                if not term_check["passed"]
                else "",
            ]
            if block
        ]
        return {
            "validation_passed": all(check.get("passed", False) for check in checks.values()),
            "checks": checks,
            "errors": errors,
            "repair_required": bool(repair_requirements),
            "repair_requirements": repair_requirements,
            "required_keywords": required_terms,
            "matched_keywords_after_repair": keyword_check.get("matched_keywords", []),
            "missing_keywords_after_repair": keyword_check.get("missing_keywords", []),
            "safety_guard": safety_check,
            "industrial_terms": term_check,
            "is_safety_question": safety_assessment.get("is_safety_question", False),
            "risk_level": safety_assessment.get("risk_level", 0),
            "risk_reasons": safety_assessment.get("risk_reasons", []),
            "basis_status": basis_assessment.get("basis_status", "sufficient"),
            "basis_reasons": basis_assessment.get("basis_reasons", []),
            "human_review_required": basis_assessment.get("human_review_required", False),
        }

    def _build_basis_assessment(
        self,
        question: str,
        result: dict[str, Any],
        context: str,
        sources: list[SourceItem],
    ) -> dict[str, Any]:
        reasons: list[str] = []
        question_text = question.lower()
        answer_text = self._collect_result_text(result).lower()
        context_text = context.lower()

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
            "知识库中未找到充分依据",
            "not enough",
            "insufficient",
        ]
        question_markers = [
            ("unknown_fault_code", ["未知故障码", "未列出", "p9999", "e9999", "故障码"]),
            ("unknown_terminal_diagram", ["cnusr11", "全部端子", "接线图", "线号"]),
            ("third_party_substitute", ["第三方", "替代", "代替", "兼容性", "保证寿命"]),
            ("missing_model_specific_data", ["某具体型号", "精确", "stopping distance", "当前负载"]),
            ("missing_purchase_or_lifetime_data", ["采购清单", "寿命小时", "强酸", "保证的寿命"]),
        ]
        for reason, markers in question_markers:
            if any(marker.lower() in question_text for marker in markers):
                reasons.append(reason)

        if reasons and any(marker.lower() in answer_text for marker in insufficient_markers):
            reasons.append("answer_indicates_insufficient_basis")

        if not sources:
            reasons.append("no_retrieval_sources")
        if "知识库中未找到相关片段" in context_text:
            reasons.append("empty_retrieval_context")

        reasons = self._dedupe_strings(reasons)
        if reasons:
            basis_status = "insufficient"
        elif self._ensure_text(result.get("manual_basis"), default="") or sources:
            basis_status = "sufficient"
        else:
            basis_status = "partial"
        return {
            "basis_status": basis_status,
            "basis_reasons": reasons,
            "human_review_required": basis_status == "insufficient",
        }

    def _collect_result_text(self, result: dict[str, Any]) -> str:
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

        visit(result)
        return "\n".join(chunks)

    def _ensure_matched_terms_preserved(
        self,
        result: dict[str, Any],
        matched_industrial_terms: list[dict[str, Any]],
    ) -> None:
        term_check = self.industrial_term_service.validate_preservation(result, matched_industrial_terms)
        missing_terms = term_check.get("missing_preserved_terms", [])
        if not missing_terms:
            return

        term_lookup = {str(term.get("canonical")): term for term in matched_industrial_terms}
        notes = []
        for canonical in missing_terms:
            term = term_lookup.get(str(canonical), {})
            zh = str(term.get("zh", "")).strip()
            notes.append(f"{canonical}（{zh}）" if zh else str(canonical))
        if not notes:
            return

        suffix = "术语保留说明：" + "、".join(notes)
        answer = self._ensure_text(result.get("answer"), default="")
        if suffix not in answer:
            result["answer"] = f"{answer}\n\n{suffix}" if answer else suffix

    def _validate_required_terms(self, result: dict[str, Any], required_terms: list[str]) -> dict[str, Any]:
        from app.services.answer_validator import validate_required_keywords

        validation = validate_required_keywords(result, required_terms, self.term_preserver.aliases())
        errors = []
        if validation["missing_keywords"]:
            errors.append(f"missing required keywords: {validation['missing_keywords']}")
        return {
            **validation,
            "passed": not validation["missing_keywords"],
            "errors": errors,
        }

    def _build_keyword_repair_requirements(self, keyword_check: dict[str, Any]) -> str:
        missing = keyword_check.get("missing_keywords", [])
        if not missing:
            return ""
        return (
            "关键词覆盖硬约束：最终回答和结构化字段必须覆盖以下 required_terms；"
            "如果资料片段没有充分依据，应明确写“资料片段中未检索到该项的充分依据”，不得编造。\n"
            f"{json.dumps(missing, ensure_ascii=False)}"
        )

    def _build_work_order_recommendation(
        self,
        question: str,
        question_type: str | None,
        equipment_type: str | None,
        result: dict[str, Any],
        sources: list[SourceItem],
        should_create_workorder: bool | None,
        safety_assessment: dict[str, Any],
        required_terms: list[str],
        basis_assessment: dict[str, Any],
    ) -> dict[str, Any]:
        reasons = []
        explicit_execution_intent = self._has_explicit_workorder_intent(question)
        document_lookup_intent = self._has_document_lookup_intent(question)
        normalized_question_type = (question_type or "").strip().lower()
        is_direct_workorder_type = normalized_question_type in {
            "procedure_fault",
            "safety_boundary",
            "high_risk_safety",
        }
        high_risk_safety = int(safety_assessment.get("risk_level", 0) or 0) >= 2
        if should_create_workorder and not document_lookup_intent:
            reasons.append("request_should_create_workorder")
        if is_direct_workorder_type and not document_lookup_intent:
            reasons.append(f"question_type_{normalized_question_type}")
        if explicit_execution_intent and not document_lookup_intent:
            reasons.append("explicit_execution_intent")
        if (
            normalized_question_type not in {"smoke", "parameter"}
            and high_risk_safety
            and not document_lookup_intent
        ):
            reasons.append("safety_or_risk_related")
        if (
            normalized_question_type not in {"smoke", "parameter"}
            and self._looks_like_workorder_question(question)
            and not document_lookup_intent
        ):
            reasons.append("fault_or_maintenance_intent")

        repair_steps = self._ensure_list(result.get("repair_steps"))
        inspection_steps = self._ensure_list(result.get("inspection_steps")) or repair_steps
        safety_actions = self._ensure_list(result.get("safety_actions"))
        payload_preview = {
            "equipment_type": equipment_type,
            "fault_symptom": question,
            "fault_understanding": self._ensure_text(result.get("fault_understanding")),
            "possible_causes": self._ensure_list(result.get("possible_causes")),
            "repair_steps": repair_steps,
            "inspection_steps": inspection_steps,
            "key_parameters": self._extract_key_parameters(required_terms),
            "safety_notes": self._ensure_list(result.get("safety_notes")),
            "safety_actions": safety_actions,
            "source_chunk_ids": [source.chunk_id for source in sources],
            "missing_fields": [],
            "sources": [source.model_dump() for source in sources],
            "operator_note": "Generated from RAG work_order_recommendation.",
        }
        recommendation = {
            "should_create_workorder": bool(should_create_workorder),
            "recommend_workorder": bool(reasons),
            "ready_to_create": False,
            "reason": ", ".join(reasons) if reasons else "no_workorder_intent_detected",
            "explicit_execution_intent": explicit_execution_intent,
            "document_lookup_intent": document_lookup_intent,
            "basis_status": basis_assessment.get("basis_status", "sufficient"),
            "basis_reasons": basis_assessment.get("basis_reasons", []),
            "human_review_required": basis_assessment.get("human_review_required", False),
            "payload_preview": payload_preview,
        }
        quality_check = self._work_order_quality_check(
            recommendation,
            question_type=normalized_question_type,
        )
        payload_preview["missing_fields"] = quality_check["missing_fields"]
        recommendation["ready_to_create"] = quality_check["ready_to_create"]
        recommendation["work_order_quality_check"] = quality_check
        if quality_check["missing_fields"]:
            recommendation["reason"] = (
                f"{recommendation['reason']}; missing_fields={quality_check['missing_fields']}"
            )
        return recommendation

    def _validate_work_order_recommendation(self, recommendation: dict[str, Any]) -> dict[str, Any]:
        errors = []
        for field in ["should_create_workorder", "recommend_workorder", "ready_to_create"]:
            if field not in recommendation:
                errors.append(f"work_order_recommendation missing {field}")
        if "ready_to_create" not in recommendation:
            errors.append("work_order_recommendation missing ready_to_create")
        payload = recommendation.get("payload_preview")
        if not isinstance(payload, dict):
            errors.append("work_order_recommendation missing payload_preview")
        else:
            for field in [
                "fault_symptom",
                "repair_steps",
                "inspection_steps",
                "key_parameters",
                "safety_actions",
                "source_chunk_ids",
                "missing_fields",
            ]:
                if field not in payload:
                    errors.append(f"work_order_recommendation payload_preview missing {field}")
        return {
            "passed": not errors,
            "errors": errors,
            "ready_to_create": bool(recommendation.get("ready_to_create")),
            "recommend_workorder": bool(recommendation.get("recommend_workorder")),
        }

    def _work_order_quality_check(
        self,
        recommendation: dict[str, Any],
        question_type: str | None = None,
    ) -> dict[str, Any]:
        payload = recommendation.get("payload_preview")
        missing_fields: list[str] = []
        if not isinstance(payload, dict):
            return {
                "passed": False,
                "errors": ["work_order_recommendation missing payload_preview"],
                "ready_to_create": False,
                "recommend_workorder": bool(recommendation.get("recommend_workorder")),
                "missing_fields": ["payload_preview"],
                "human_review_required": bool(recommendation.get("human_review_required")),
            }
        if question_type is None and isinstance(recommendation.get("work_order_quality_check"), dict):
            return recommendation["work_order_quality_check"]

        recommend_workorder = bool(recommendation.get("recommend_workorder"))
        normalized_question_type = (question_type or "").strip().lower()
        repair_steps = self._ensure_list(payload.get("repair_steps"))
        inspection_steps = self._ensure_list(payload.get("inspection_steps"))
        safety_actions = self._ensure_list(payload.get("safety_actions"))
        source_chunk_ids = self._ensure_list(payload.get("source_chunk_ids"))
        basis_status = str(recommendation.get("basis_status") or "sufficient")

        if not recommend_workorder:
            ready_to_create = False
        else:
            if recommendation.get("document_lookup_intent"):
                missing_fields.append("actionable_workorder_intent")
            if basis_status == "insufficient":
                missing_fields.append("sufficient_manual_basis")
            if not self._ensure_text(payload.get("fault_symptom"), default=""):
                missing_fields.append("fault_symptom")
            if not source_chunk_ids:
                missing_fields.append("source_chunk_ids")
            if normalized_question_type in {"smoke", "parameter"} and not recommendation.get(
                "explicit_execution_intent"
            ):
                missing_fields.append("explicit_execution_intent")
            if normalized_question_type in {"procedure_fault", "safety_boundary"} and not (
                repair_steps or inspection_steps
            ):
                missing_fields.append("repair_steps_or_inspection_steps")
            if normalized_question_type in {"safety_boundary", "high_risk_safety"} and not safety_actions:
                missing_fields.append("safety_actions")
            if not repair_steps and not safety_actions:
                missing_fields.append("repair_steps_or_safety_actions")
            ready_to_create = not missing_fields

        consistency_errors = []
        if recommendation.get("ready_to_create") and missing_fields:
            consistency_errors.append(
                f"ready_to_create must be false when missing fields exist: {missing_fields}"
            )
        return {
            "passed": not consistency_errors,
            "errors": consistency_errors,
            "ready_to_create": ready_to_create,
            "recommend_workorder": recommend_workorder,
            "missing_fields": missing_fields,
            "basis_status": basis_status,
            "human_review_required": bool(recommendation.get("human_review_required"))
            or basis_status == "insufficient",
        }

    def _maybe_create_work_order(
        self,
        recommendation: dict[str, Any],
        auto_create_workorder: bool,
    ) -> dict[str, Any]:
        if not auto_create_workorder:
            return {"created": False, "work_order_id": "", "error": ""}
        if not recommendation.get("ready_to_create"):
            return {
                "created": False,
                "work_order_id": "",
                "error": "work_order_recommendation is not ready_to_create",
            }

        payload = recommendation.get("payload_preview", {})
        source_items = [
            source if isinstance(source, SourceItem) else SourceItem(**source)
            for source in payload.get("sources", [])
            if isinstance(source, (dict, SourceItem))
        ]
        try:
            item = self.workorder_service.create_workorder(
                WorkOrderCreateRequest(
                    equipment_type=payload.get("equipment_type"),
                    fault_symptom=payload.get("fault_symptom") or "RAG generated work order",
                    fault_understanding=payload.get("fault_understanding") or "知识库中未找到充分依据。",
                    possible_causes=self._ensure_list(payload.get("possible_causes")),
                    repair_steps=self._ensure_list(payload.get("repair_steps")),
                    safety_notes=self._ensure_list(payload.get("safety_notes")),
                    safety_actions=self._ensure_list(payload.get("safety_actions")),
                    sources=source_items,
                    operator_note=payload.get("operator_note") or "Generated from RAG auto_create_workorder.",
                )
            )
        except Exception as exc:
            return {"created": False, "work_order_id": "", "error": str(exc)}
        return {"created": True, "work_order_id": item.work_order_id, "error": ""}

    def _looks_like_workorder_question(self, question: str) -> bool:
        keywords = [
            "故障",
            "维修",
            "维护",
            "检修",
            "更换",
            "拆卸",
            "安装",
            "报警",
            "异常",
            "冒烟",
            "危险",
            "安全",
            "repair",
            "maintenance",
            "fault",
            "alarm",
            "replace",
            "install",
        ]
        normalized = question.lower()
        return any(keyword.lower() in normalized for keyword in keywords)

    def _has_explicit_workorder_intent(self, question: str) -> bool:
        keywords = [
            "故障",
            "拆卸",
            "更换",
            "无法运行",
            "不能运行",
            "无法启动",
            "冒烟",
            "失效",
            "危险",
            "维修",
            "检修",
            "异常",
            "fault",
            "failure",
            "failed",
            "replace",
            "remove",
            "disassemble",
            "smoke",
            "danger",
            "hazard",
            "cannot run",
            "not running",
        ]
        normalized = question.lower()
        return any(keyword.lower() in normalized for keyword in keywords)

    def _has_document_lookup_intent(self, question: str) -> bool:
        keywords = [
            "位于哪类",
            "属于哪一章",
            "在哪个章节",
            "位于哪个章节",
            "手册包含哪些内容",
            "包含哪些主要章节",
            "介绍哪些内容",
            "资料定位",
            "目录",
            "位于哪一类",
            "哪类维护内容",
            "有哪些章节",
            "版本历史",
            "主要增加了哪些章节",
            "手册包含哪些",
            "包含哪些维修保养",
            "包含哪些故障对策",
            "哪些维修保养和故障对策内容",
        ]
        normalized = question.lower()
        return any(keyword.lower() in normalized for keyword in keywords)

    def _extract_key_parameters(self, required_terms: list[str]) -> list[str]:
        parameters = []
        for term in required_terms:
            text = str(term).strip()
            if text and (re.search(r"\d", text) or re.search(r"[a-zA-Z]+[·/.-]?[a-zA-Z]*", text)):
                parameters.append(text)
        return parameters

    def _dedupe_strings(self, values: list[str]) -> list[str]:
        result: list[str] = []
        seen: set[str] = set()
        for value in values:
            key = str(value).strip().lower()
            if not key or key in seen:
                continue
            seen.add(key)
            result.append(str(value).strip())
        return result

    def _has_preferred_document(self, results: list[Any], preferred_documents: list[str]) -> bool:
        preferred = {str(document).strip() for document in preferred_documents if str(document).strip()}
        return any(self.document_intent_service._filename(result) in preferred for result in results)

    def _dedupe_retrieval_results(self, results: list[Any]) -> list[Any]:
        deduped = []
        seen: set[str] = set()
        for result in results:
            key = str(getattr(result, "chunk_id", "") or "")
            if not key:
                key = f"{self.document_intent_service._filename(result)}:{getattr(result, 'chunk_text', '')[:80]}"
            if key in seen:
                continue
            seen.add(key)
            deduped.append(result)
        return deduped

    def _build_context(self, results: list[Any]) -> str:
        if not results:
            return "知识库中未找到相关片段。"

        lines: list[str] = []
        for index, result in enumerate(results, start=1):
            metadata = result.metadata
            filename = metadata.get("filename", result.document_title)
            chunk_index = metadata.get("chunk_index")
            lines.extend(
                [
                    f"[片段 {index}]",
                    f"chunk_id: {result.chunk_id}",
                    f"document_id: {result.document_id}",
                    f"filename: {filename}",
                    f"chunk_index: {chunk_index}",
                    f"score: {result.score}",
                    "content:",
                    result.chunk_text,
                    "",
                ]
            )
        return "\n".join(lines)

    def _source_from_result(self, result: Any) -> SourceItem:
        metadata = result.metadata
        filename = metadata.get("filename", result.document_title)
        return SourceItem(
            chunk_id=result.chunk_id,
            document_id=result.document_id,
            document_title=result.document_title,
            filename=filename,
            chunk_index=metadata.get("chunk_index"),
            score=result.score,
            metadata=metadata,
        )

    def _parse_model_output(self, content: str) -> dict[str, Any]:
        json_payload = self._try_parse_json(content)
        if json_payload is not None:
            return json_payload

        markdown_payload = self._try_parse_markdown(content)
        if markdown_payload is not None:
            markdown_payload["answer"] = content
            return markdown_payload

        return {
            "answer": content,
            "fault_understanding": "模型未返回可解析的结构化内容，原始回答已保留在 answer 字段。",
            "possible_causes": [],
            "repair_steps": [],
            "safety_notes": [],
        }

    def _try_parse_json(self, content: str) -> dict[str, Any] | None:
        candidates = [content.strip()]

        fence_match = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", content, flags=re.S | re.I)
        if fence_match:
            candidates.insert(0, fence_match.group(1).strip())

        object_match = re.search(r"\{.*\}", content, flags=re.S)
        if object_match:
            candidates.append(object_match.group(0).strip())

        for candidate in candidates:
            try:
                payload = json.loads(candidate)
            except json.JSONDecodeError:
                continue
            if isinstance(payload, dict):
                return payload
        return None

    def _try_parse_markdown(self, content: str) -> dict[str, Any] | None:
        sections = self._extract_markdown_sections(content)
        if not sections:
            return None

        fault_understanding = self._first_section(
            sections,
            ["fault_understanding", "故障现象理解", "故障理解", "总体判断", "故障现象"],
        )
        possible_causes = self._section_items(
            sections,
            ["possible_causes", "可能原因", "原因分析", "故障原因"],
        )
        repair_steps = self._section_items(
            sections,
            ["repair_steps", "排查步骤", "检修步骤", "处理步骤", "维修步骤"],
        )
        safety_notes = self._section_items(
            sections,
            ["safety_notes", "安全注意事项", "安全提醒", "注意事项"],
        )

        if not any([fault_understanding, possible_causes, repair_steps, safety_notes]):
            return None

        return {
            "fault_understanding": fault_understanding,
            "possible_causes": possible_causes,
            "repair_steps": repair_steps,
            "safety_notes": safety_notes,
        }

    def _extract_markdown_sections(self, content: str) -> dict[str, str]:
        sections: dict[str, list[str]] = {}
        current_title = "正文"

        for raw_line in content.splitlines():
            line = raw_line.strip()
            if not line:
                continue

            heading_match = re.match(r"^(?:#{1,6}\s*)?(.+?)[：:]\s*$", line)
            numbered_heading_match = re.match(r"^\d+[.、]\s*(.+?)[：:：]?\s*$", line)
            if heading_match and len(heading_match.group(1)) <= 24:
                current_title = heading_match.group(1).strip()
                sections.setdefault(current_title, [])
                continue
            if numbered_heading_match and len(numbered_heading_match.group(1)) <= 24:
                current_title = numbered_heading_match.group(1).strip()
                sections.setdefault(current_title, [])
                continue

            sections.setdefault(current_title, []).append(line)

        return {key: "\n".join(value).strip() for key, value in sections.items() if value}

    def _first_section(self, sections: dict[str, str], aliases: list[str]) -> str:
        for title, value in sections.items():
            if self._matches_alias(title, aliases):
                return value.strip()
        return ""

    def _section_items(self, sections: dict[str, str], aliases: list[str]) -> list[str]:
        for title, value in sections.items():
            if self._matches_alias(title, aliases):
                return self._lines_to_items(value)
        return []

    def _matches_alias(self, title: str, aliases: list[str]) -> bool:
        normalized = re.sub(r"\s+", "", title).lower()
        return any(re.sub(r"\s+", "", alias).lower() in normalized for alias in aliases)

    def _lines_to_items(self, value: str) -> list[str]:
        items: list[str] = []
        for line in value.splitlines():
            item = re.sub(r"^[-*•]\s*", "", line.strip())
            item = re.sub(r"^\d+[.、]\s*", "", item)
            if item:
                items.append(item)
        if items:
            return items
        return [value.strip()] if value.strip() else []

    def _fallback_answer(self, reason: str) -> dict[str, Any]:
        return {
            "answer": "",
            "fault_understanding": f"知识库中未找到充分依据，或{reason}",
            "possible_causes": ["请先确认检索资料是否覆盖该故障现象。"],
            "repair_steps": ["建议人工复核检索片段后，再制定具体检修步骤。"],
            "safety_notes": [
                "知识库依据不足时，不应执行高风险检修操作；请先由具备资质的人员复核原始资料和现场状态。"
            ],
        }

    def _ensure_text(self, value: Any, default: str = "知识库中未找到充分依据。") -> str:
        if isinstance(value, str) and value.strip():
            return value.strip()
        return default

    def _ensure_optional_text(self, value: Any) -> str | None:
        if isinstance(value, str) and value.strip():
            return value.strip()
        return None

    def _ensure_list(self, value: Any) -> list[str]:
        if isinstance(value, list):
            items = [str(item).strip() for item in value if str(item).strip()]
            if items:
                return items
        if isinstance(value, str) and value.strip():
            return self._lines_to_items(value)
        return []

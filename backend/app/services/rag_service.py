import json
import re
from typing import Any

from app.config import BASE_DIR
from app.schemas.chat_schema import RepairChatRequest, RepairChatResponse, SourceItem
from app.services.answer_repair import AnswerRepair
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
                parsed=parsed,
                answer="",
                sources=[],
            )

        sources = [self._source_from_result(result) for result in retrieval_response.results]
        context = self._build_context(retrieval_response.results)
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
            parsed=parsed,
            answer=self._ensure_text(parsed.get("answer"), default=raw_answer),
            sources=sources,
        )

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
    ) -> RepairChatResponse:
        fault_understanding = self._ensure_text(parsed.get("fault_understanding"))
        possible_causes = self._ensure_list(parsed.get("possible_causes"))
        repair_steps = self._ensure_list(parsed.get("repair_steps"))
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
        )
        guarded_result = guarded_payload["result"]
        work_order_recommendation = self._build_work_order_recommendation(
            question=question,
            equipment_type=equipment_type,
            result=guarded_result,
            sources=sources,
            should_create_workorder=should_create_workorder,
            safety_assessment=guarded_payload["assessment"],
        )
        validation_before_repair = self._validate_answer(
            result=guarded_result,
            required_terms=required_terms,
            safety_assessment=guarded_payload["assessment"],
            matched_industrial_terms=matched_industrial_terms,
            work_order_recommendation=work_order_recommendation,
            should_create_workorder=should_create_workorder,
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
        )
        repaired = final_guarded_payload["result"]
        work_order_recommendation = self._build_work_order_recommendation(
            question=question,
            equipment_type=equipment_type,
            result=repaired,
            sources=sources,
            should_create_workorder=should_create_workorder,
            safety_assessment=final_guarded_payload["assessment"],
        )
        validation_after_repair = self._validate_answer(
            result=repaired,
            required_terms=required_terms,
            safety_assessment=final_guarded_payload["assessment"],
            matched_industrial_terms=matched_industrial_terms,
            work_order_recommendation=work_order_recommendation,
            should_create_workorder=should_create_workorder,
        )
        work_order = self._maybe_create_work_order(
            recommendation=work_order_recommendation,
            auto_create_workorder=auto_create_workorder,
        )
        debug = {
            "required_terms": required_terms,
            "term_aliases_used": self.term_preserver.aliases(),
            "matched_industrial_terms": matched_industrial_terms,
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
    ) -> dict[str, Any]:
        keyword_check = self._validate_required_terms(result=result, required_terms=required_terms)
        safety_check = self.safety_guard.validate(
            result,
            safety_assessment,
            should_create_workorder=should_create_workorder,
        )
        term_check = self.industrial_term_service.validate_preservation(result, matched_industrial_terms)
        workorder_check = self._validate_work_order_recommendation(work_order_recommendation)
        checks = {
            "keyword_check": keyword_check,
            "safety_check": safety_check,
            "term_check": term_check,
            "workorder_check": workorder_check,
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
        }

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
        equipment_type: str | None,
        result: dict[str, Any],
        sources: list[SourceItem],
        should_create_workorder: bool | None,
        safety_assessment: dict[str, Any],
    ) -> dict[str, Any]:
        reasons = []
        if should_create_workorder:
            reasons.append("request_should_create_workorder")
        if safety_assessment.get("is_safety_question"):
            reasons.append("safety_or_risk_related")
        if self._looks_like_workorder_question(question):
            reasons.append("fault_or_maintenance_intent")

        payload_preview = {
            "equipment_type": equipment_type,
            "fault_symptom": question,
            "fault_understanding": self._ensure_text(result.get("fault_understanding")),
            "possible_causes": self._ensure_list(result.get("possible_causes")),
            "repair_steps": self._ensure_list(result.get("repair_steps")),
            "safety_notes": self._ensure_list(result.get("safety_notes")),
            "safety_actions": self._ensure_list(result.get("safety_actions")),
            "source_chunk_ids": [source.chunk_id for source in sources],
            "sources": [source.model_dump() for source in sources],
            "operator_note": "Generated from RAG work_order_recommendation.",
        }
        return {
            "ready_to_create": bool(reasons),
            "reason": ", ".join(reasons) if reasons else "no_workorder_intent_detected",
            "payload_preview": payload_preview,
        }

    def _validate_work_order_recommendation(self, recommendation: dict[str, Any]) -> dict[str, Any]:
        errors = []
        if "ready_to_create" not in recommendation:
            errors.append("work_order_recommendation missing ready_to_create")
        payload = recommendation.get("payload_preview")
        if not isinstance(payload, dict):
            errors.append("work_order_recommendation missing payload_preview")
        else:
            for field in ["fault_symptom", "repair_steps", "safety_actions", "source_chunk_ids"]:
                if field not in payload:
                    errors.append(f"work_order_recommendation payload_preview missing {field}")
        return {
            "passed": not errors,
            "errors": errors,
            "ready_to_create": bool(recommendation.get("ready_to_create")),
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

from __future__ import annotations

import json
import re
from typing import Any

from app.services.answer_validator import validate_required_keywords
from app.services.llm_service import LLMError, LLMService
from app.services.term_preserver import TERM_ALIASES


MAX_REPAIR_ROUNDS = 1


class AnswerRepair:
    """Repairs incomplete answers once, using the same retrieved evidence."""

    def repair(
        self,
        result: dict[str, Any],
        required_keywords: list[str],
        question: str,
        context: str,
        sources: list[dict[str, Any]],
        llm_service: LLMService,
        question_type: str | None = None,
        must_have_safety: bool | None = None,
        should_create_workorder: bool | None = None,
        extra_repair_requirements: str = "",
        force_repair: bool = False,
    ) -> dict[str, Any]:
        before = validate_required_keywords(result, required_keywords, TERM_ALIASES)
        if not before["missing_keywords"] and not force_repair:
            validation = self._build_validation(required_keywords, before, before, repair_applied=False)
            return {
                "result": result,
                "validation": validation,
                "debug": {
                    "answer_validator": before,
                    "answer_validator_after_repair": before,
                    "answer_repair_applied": False,
                    "answer_repair_mode": "none",
                    "answer_repair_terms": [],
                    "repair_failed": False,
                },
            }

        repaired_result = result
        repair_mode = "none"
        repair_failed = True

        for _ in range(MAX_REPAIR_ROUNDS):
            repair_candidate = self._repair_with_llm(
                result=result,
                missing_terms=before["missing_keywords"],
                question=question,
                context=context,
                sources=sources,
                llm_service=llm_service,
                question_type=question_type,
                must_have_safety=must_have_safety,
                should_create_workorder=should_create_workorder,
                extra_repair_requirements=extra_repair_requirements,
            )
            if repair_candidate is None:
                repair_mode = "llm_failed"
                break

            merged = self._merge_if_more_complete(
                initial=result,
                repair=repair_candidate,
                required_keywords=required_keywords,
                before_validation=before,
                force_repair=force_repair,
            )
            if merged["used_repair"]:
                repaired_result = merged["result"]
                repair_mode = "llm"
                repair_failed = False
            else:
                repair_mode = "not_more_complete"
            break

        after = validate_required_keywords(repaired_result, required_keywords, TERM_ALIASES)
        validation = self._build_validation(
            required_keywords=required_keywords,
            before=before,
            after=after,
            repair_applied=not repair_failed,
        )
        return {
            "result": repaired_result,
            "validation": validation,
            "debug": {
                "answer_validator": before,
                "answer_validator_after_repair": after,
                "answer_repair_applied": not repair_failed,
                "answer_repair_mode": repair_mode,
                "answer_repair_terms": before["missing_keywords"],
                "repair_failed": repair_failed,
                "max_repair_rounds": MAX_REPAIR_ROUNDS,
            },
        }

    def _repair_with_llm(
        self,
        result: dict[str, Any],
        missing_terms: list[str],
        question: str,
        context: str,
        sources: list[dict[str, Any]],
        llm_service: LLMService,
        question_type: str | None,
        must_have_safety: bool | None,
        should_create_workorder: bool | None,
        extra_repair_requirements: str,
    ) -> dict[str, Any] | None:
        messages = [
            {
                "role": "system",
                "content": (
                    "你是工业设备检修资料问答系统的回答修复器。"
                    "你只能根据用户提供的资料片段补全回答，不得编造资料中没有的内容。"
                    "请输出严格 JSON，不要输出 Markdown 或代码块。"
                ),
            },
            {
                "role": "user",
                "content": self._build_repair_prompt(
                    question=question,
                    initial_answer=result,
                    missing_terms=missing_terms,
                    context=context,
                    sources=sources,
                    question_type=question_type,
                    must_have_safety=must_have_safety,
                    should_create_workorder=should_create_workorder,
                    extra_repair_requirements=extra_repair_requirements,
                ),
            },
        ]
        try:
            content = llm_service.generate_chat_completion(messages)
        except LLMError:
            return None
        return self._parse_json_object(content)

    def _build_repair_prompt(
        self,
        question: str,
        initial_answer: dict[str, Any],
        missing_terms: list[str],
        context: str,
        sources: list[dict[str, Any]],
        question_type: str | None,
        must_have_safety: bool | None,
        should_create_workorder: bool | None,
        extra_repair_requirements: str,
    ) -> str:
        extra_block = f"\n额外硬性修复要求：\n{extra_repair_requirements}\n" if extra_repair_requirements else ""
        return (
            "用户问题：\n"
            f"{question}\n\n"
            "题型 question_type：\n"
            f"{question_type or '未提供'}\n\n"
            "是否安全题 must_have_safety：\n"
            f"{must_have_safety}\n\n"
            "是否需要工单 should_create_workorder：\n"
            f"{should_create_workorder}\n\n"
            "系统初版回答：\n"
            f"{json.dumps(initial_answer, ensure_ascii=False, indent=2)}\n\n"
            "当前回答缺少以下必须覆盖的关键点：\n"
            f"{json.dumps(missing_terms, ensure_ascii=False)}\n\n"
            "请你仅基于下列资料片段补全回答，不得编造资料中没有的内容：\n"
            f"{self._compact_context(context)}\n\n"
            "sources 元数据：\n"
            f"{json.dumps(sources, ensure_ascii=False, indent=2)}\n\n"
            f"{extra_block}"
            "修复要求：\n"
            "1. 必须显式覆盖 missing_keywords 中的每一项。\n"
            "2. 如果 missing_keywords 或额外硬性修复要求中包含英文工业术语，"
            "必须在回答中保留英文原词，并可在括号中给出中文解释。\n"
            "3. 如果问题涉及安全边界，必须明确说明是否允许继续操作。\n"
            "4. 如果资料中没有某个关键词对应的信息，必须明确写："
            "“资料片段中未检索到该项的充分依据”，不要编造。\n"
            "5. 输出时保持原有结构，并保留已有安全结构字段。\n"
            "6. 不要输出与 sources 无关的泛泛安全提醒。\n\n"
            "输出 JSON schema：\n"
            "{\n"
            '  "answer": "...",\n'
            '  "fault_understanding": "...",\n'
            '  "possible_causes": ["..."],\n'
            '  "repair_steps": ["..."],\n'
            '  "safety_notes": ["..."],\n'
            '  "operation_allowed": "不允许 / 需要先满足条件 / 资料不足无法确认",\n'
            '  "immediate_actions": ["..."],\n'
            '  "prohibited_actions": ["..."],\n'
            '  "required_personnel": ["..."],\n'
            '  "risk_keywords": ["..."],\n'
            '  "manual_basis": ["..."],\n'
            '  "safety_actions": ["..."]\n'
            "}"
        )

    def _merge_if_more_complete(
        self,
        initial: dict[str, Any],
        repair: dict[str, Any],
        required_keywords: list[str],
        before_validation: dict[str, Any],
        force_repair: bool = False,
    ) -> dict[str, Any]:
        candidate = {
            "answer": repair.get("answer") or initial.get("answer", ""),
            "fault_understanding": repair.get("fault_understanding") or initial.get("fault_understanding", ""),
            "possible_causes": self._merge_lists(initial.get("possible_causes"), repair.get("possible_causes")),
            "repair_steps": self._merge_lists(initial.get("repair_steps"), repair.get("repair_steps")),
            "safety_notes": self._merge_lists(initial.get("safety_notes"), repair.get("safety_notes")),
            "operation_allowed": repair.get("operation_allowed") or initial.get("operation_allowed"),
            "immediate_actions": self._merge_lists(initial.get("immediate_actions"), repair.get("immediate_actions")),
            "prohibited_actions": self._merge_lists(initial.get("prohibited_actions"), repair.get("prohibited_actions")),
            "required_personnel": self._merge_lists(initial.get("required_personnel"), repair.get("required_personnel")),
            "risk_keywords": self._merge_lists(initial.get("risk_keywords"), repair.get("risk_keywords")),
            "manual_basis": self._merge_lists(initial.get("manual_basis"), repair.get("manual_basis")),
            "safety_actions": self._merge_lists(initial.get("safety_actions"), repair.get("safety_actions")),
        }
        after = validate_required_keywords(candidate, required_keywords, TERM_ALIASES)
        used_repair = (
            force_repair
            or len(after["missing_keywords"]) < len(before_validation["missing_keywords"])
            or self._has_added_content(initial, candidate)
        )
        return {
            "used_repair": used_repair,
            "result": candidate if used_repair else initial,
        }

    def _build_validation(
        self,
        required_keywords: list[str],
        before: dict[str, Any],
        after: dict[str, Any],
        repair_applied: bool,
    ) -> dict[str, Any]:
        return {
            "required_keywords": required_keywords,
            "matched_keywords_before_repair": before["matched_keywords"],
            "missing_keywords_before_repair": before["missing_keywords"],
            "repair_applied": repair_applied,
            "matched_keywords_after_repair": after["matched_keywords"],
            "missing_keywords_after_repair": after["missing_keywords"],
            "validation_passed": not after["missing_keywords"],
        }

    def _parse_json_object(self, content: str) -> dict[str, Any] | None:
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
                return {
                    "answer": str(payload.get("answer", "")).strip(),
                    "fault_understanding": str(payload.get("fault_understanding", "")).strip(),
                    "possible_causes": self._ensure_list(payload.get("possible_causes")),
                    "repair_steps": self._ensure_list(payload.get("repair_steps")),
                    "safety_notes": self._ensure_list(payload.get("safety_notes")),
                    "operation_allowed": str(payload.get("operation_allowed", "")).strip(),
                    "immediate_actions": self._ensure_list(payload.get("immediate_actions")),
                    "prohibited_actions": self._ensure_list(payload.get("prohibited_actions")),
                    "required_personnel": self._ensure_list(payload.get("required_personnel")),
                    "risk_keywords": self._ensure_list(payload.get("risk_keywords")),
                    "manual_basis": self._ensure_list(payload.get("manual_basis")),
                    "safety_actions": self._ensure_list(payload.get("safety_actions")),
                }
        return None

    def _compact_context(self, context: str, limit: int = 9000) -> str:
        normalized = "\n".join(line.rstrip() for line in context.splitlines())
        if len(normalized) <= limit:
            return normalized
        return normalized[:limit]

    def _merge_lists(self, left: Any, right: Any) -> list[str]:
        result: list[str] = []
        seen: set[str] = set()
        for item in [*self._ensure_list(left), *self._ensure_list(right)]:
            key = re.sub(r"\s+", "", item)
            if key in seen:
                continue
            seen.add(key)
            result.append(item)
        return result

    def _ensure_list(self, value: Any) -> list[str]:
        if isinstance(value, list):
            return [str(item).strip() for item in value if str(item).strip()]
        if isinstance(value, str) and value.strip():
            return [value.strip()]
        return []

    def _has_added_content(self, initial: dict[str, Any], candidate: dict[str, Any]) -> bool:
        for field in [
            "operation_allowed",
            "immediate_actions",
            "prohibited_actions",
            "required_personnel",
            "risk_keywords",
            "manual_basis",
            "safety_actions",
        ]:
            if not initial.get(field) and candidate.get(field):
                return True
        return False

from __future__ import annotations

import re
from typing import Any

from app.services.answer_validator import collect_answer_text, normalize_text


SAFETY_TRIGGER_TERMS = [
    "冒烟",
    "上电",
    "拆卸",
    "维修",
    "维护",
    "更换",
    "气源",
    "电源",
    "能量源",
    "安全栅",
    "联锁门",
    "急停",
    "危险",
    "禁止",
    "停止",
]

ENGLISH_SAFETY_TRIGGER_TERMS = [
    "safety fence",
    "interlocked gate",
    "emergency stop",
    "deadman switch",
    "teach pendant",
    "maintenance",
    "teaching",
    "adjustment",
    "trained",
    "stop",
]

SAFETY_SOURCE_TERMS = [
    "safety manual",
    "bfp-a3570l",
    "安全手册",
    "安全资料",
    "机器人安全",
]

SAFETY_PASS_TERMS = [
    "停止",
    "禁止",
    "不允许",
    "切断",
    "断电",
    "隔离",
    "危险",
    "安全",
]

SAFETY_CUES = [
    *SAFETY_TRIGGER_TERMS,
    "警告",
    "注意",
    "必须",
    "不得",
    "确认",
    "防护",
    "联锁",
    "danger",
    "warning",
    "caution",
    "must",
    "shall",
    "should",
    "never",
    "do not",
    "emergency",
    "interlock",
    "guard",
]

SAFETY_STRUCTURED_FIELDS = [
    "operation_allowed",
    "immediate_actions",
    "prohibited_actions",
    "required_personnel",
    "risk_keywords",
    "manual_basis",
]

HIGH_RISK_QUESTION_TERMS = [
    "冒烟",
    "上电",
    "拆卸",
    "更换",
    "气源",
    "电源",
    "能量源",
    "安全栅",
    "联锁门",
    "急停",
    "危险",
    "禁止",
    "停止",
    "失效",
    "无法",
    "不能",
    "是否可以",
    "能否",
    "继续",
    "进入",
    "safety fence",
    "interlocked gate",
    "emergency stop",
    "maintenance",
    "teaching",
    "adjustment",
    "danger",
    "hazard",
    "stop",
]

LEVEL1_QUESTION_TERMS = [
    "维护",
    "保养",
    "点检",
    "检查",
    "确认",
    "使用前",
    "参数",
    "条件",
    "安全提示",
    "注意事项",
    "manual",
    "safety",
    "maintenance",
    "check",
    "inspection",
]

DEFAULT_OPERATION_ALLOWED = "需要先满足条件"
INSUFFICIENT_OPERATION_ALLOWED = "资料不足无法确认"
INSUFFICIENT_BASIS_TEXT = "当前资料片段未提供足够依据确认完整处置步骤，应转人工复核。"


class SafetyGuard:
    """Applies general safety constraints without encoding case-specific answers."""

    def build_assessment(
        self,
        question: str,
        context: str,
        sources: list[Any],
        must_have_safety: bool | None,
        question_type: str | None = None,
    ) -> dict[str, Any]:
        trigger_reasons: list[str] = []
        question_terms = self._matched_terms(question, SAFETY_TRIGGER_TERMS)
        english_terms = self._matched_terms(question, ENGLISH_SAFETY_TRIGGER_TERMS)
        source_terms = self._matched_source_terms(sources)
        normalized_question_type = (question_type or "").strip().lower()

        if must_have_safety is True:
            trigger_reasons.append("must_have_safety")
        if question_terms:
            trigger_reasons.append("question_safety_terms")
        if english_terms:
            trigger_reasons.append("question_english_safety_terms")
        if source_terms:
            trigger_reasons.append("safety_manual_source")

        manual_basis = self.extract_constraints(question=question, context=context, limit=5)
        risk_keywords = self._dedupe([*question_terms, *english_terms])
        if not risk_keywords:
            risk_keywords = self._matched_terms(context, [*SAFETY_TRIGGER_TERMS, *ENGLISH_SAFETY_TRIGGER_TERMS])[:8]
        risk_level, risk_reasons = self._classify_risk_level(
            question=question,
            question_type=normalized_question_type,
            must_have_safety=must_have_safety,
            question_terms=question_terms,
            english_terms=english_terms,
            source_terms=source_terms,
        )

        return {
            "is_safety_question": risk_level > 0,
            "risk_level": risk_level,
            "risk_reasons": risk_reasons,
            "trigger_reasons": trigger_reasons,
            "question_safety_terms": question_terms,
            "question_english_safety_terms": english_terms,
            "source_safety_terms": source_terms,
            "risk_keywords": risk_keywords,
            "manual_basis": manual_basis,
        }

    def apply(
        self,
        result: dict[str, Any],
        question: str,
        context: str,
        sources: list[Any],
        must_have_safety: bool | None,
        question_type: str | None = None,
    ) -> dict[str, Any]:
        assessment = self.build_assessment(
            question=question,
            context=context,
            sources=sources,
            must_have_safety=must_have_safety,
            question_type=question_type,
        )
        if assessment["risk_level"] == 0:
            result["safety_notes"] = self._dedupe(self._ensure_list(result.get("safety_notes")))
            return {
                "result": result,
                "assessment": assessment,
                "validation": self.validate(result, assessment, should_create_workorder=False),
            }
        if assessment["risk_level"] == 1:
            result["safety_notes"] = self._dedupe(
                [
                    *self._ensure_list(result.get("safety_notes")),
                    *assessment.get("manual_basis", []),
                ]
            )
            return {
                "result": result,
                "assessment": assessment,
                "validation": self.validate(result, assessment, should_create_workorder=False),
            }

        guarded = self._ensure_structured_fields(dict(result), assessment)
        guarded["answer"] = self._build_guarded_answer(
            answer=str(guarded.get("answer", "")).strip(),
            structured=guarded,
            has_manual_basis=bool(assessment["manual_basis"]),
        )
        guarded["safety_notes"] = self._dedupe(
            [
                *self._ensure_list(guarded.get("safety_notes")),
                *guarded["immediate_actions"],
                *guarded["prohibited_actions"],
                *guarded["required_personnel"],
                *guarded["manual_basis"],
            ]
        )
        return {
            "result": guarded,
            "assessment": assessment,
            "validation": self.validate(guarded, assessment, should_create_workorder=False),
        }

    def validate(
        self,
        result: dict[str, Any],
        assessment: dict[str, Any],
        should_create_workorder: bool | None,
    ) -> dict[str, Any]:
        errors: list[str] = []
        risk_level = int(assessment.get("risk_level", 0) or 0)
        if risk_level <= 0:
            return {
                "passed": True,
                "errors": errors,
                "signal_count": 0,
                "english_terms_missing": [],
                "risk_level": risk_level,
                "risk_reasons": assessment.get("risk_reasons", []),
            }

        safety_notes = self._ensure_list(result.get("safety_notes"))
        if risk_level >= 1 and "must_have_safety" in assessment.get("trigger_reasons", []) and not safety_notes:
            errors.append("safety_notes must contain at least one item for safety questions")

        text = collect_answer_text(result)
        normalized_text = normalize_text(text)
        english_terms_missing = [
            term
            for term in assessment.get("question_english_safety_terms", [])
            if normalize_text(term) not in normalized_text
        ]

        if risk_level < 2:
            return {
                "passed": not errors,
                "errors": errors,
                "signal_count": 0,
                "english_terms_missing": english_terms_missing,
                "risk_level": risk_level,
                "risk_reasons": assessment.get("risk_reasons", []),
            }

        missing_fields = [field for field in SAFETY_STRUCTURED_FIELDS if field not in result]
        if missing_fields:
            errors.append(f"missing safety structured fields: {missing_fields}")

        signal_count = sum(1 for term in SAFETY_PASS_TERMS if normalize_text(term) in normalized_text)
        if signal_count < 2:
            errors.append("safety answer must contain at least two hard safety signals")

        if english_terms_missing:
            errors.append(f"english safety terms must be preserved: {english_terms_missing}")

        if should_create_workorder and not self._ensure_list(result.get("safety_actions")):
            errors.append("safety_actions must be saved when workorder creation is requested")

        return {
            "passed": not errors,
            "errors": errors,
            "signal_count": signal_count,
            "english_terms_missing": english_terms_missing,
            "risk_level": risk_level,
            "risk_reasons": assessment.get("risk_reasons", []),
        }

    def build_repair_requirements(self, assessment: dict[str, Any], validation: dict[str, Any]) -> str:
        return (
            "该问题已触发 Safety Guard 硬约束。请只基于资料片段补全安全字段，不得编造资料中没有的设备细节。\n"
            f"触发原因：{assessment.get('trigger_reasons', [])}\n"
            f"风险关键词：{assessment.get('risk_keywords', [])}\n"
            f"当前未通过项：{validation.get('errors', [])}\n"
            "最终 JSON 必须包含 operation_allowed、immediate_actions、prohibited_actions、"
            "required_personnel、risk_keywords、manual_basis、safety_notes。"
        )

    def extract_constraints(self, question: str, context: str, limit: int = 4) -> list[str]:
        question_tokens = self._tokens(question)
        scored: list[tuple[int, str]] = []

        for sentence in self._split_sentences(context):
            normalized = normalize_text(sentence)
            if not any(normalize_text(cue) in normalized for cue in SAFETY_CUES):
                continue
            score = 1 + len(self._tokens(sentence) & question_tokens)
            if any(cue in normalized for cue in ["danger", "warning", "危险", "警告", "必须", "不得", "禁止"]):
                score += 2
            scored.append((score, self._clean_sentence(sentence)))

        scored.sort(key=lambda item: item[0], reverse=True)
        return self._dedupe([sentence for _, sentence in scored])[:limit]

    def _ensure_structured_fields(self, result: dict[str, Any], assessment: dict[str, Any]) -> dict[str, Any]:
        manual_basis = self._ensure_list(result.get("manual_basis")) or assessment["manual_basis"]
        has_manual_basis = bool(manual_basis)
        risk_keywords = self._dedupe([*self._ensure_list(result.get("risk_keywords")), *assessment["risk_keywords"]])
        english_terms = assessment.get("question_english_safety_terms", [])

        result["operation_allowed"] = self._operation_allowed(result.get("operation_allowed"), has_manual_basis)
        result["immediate_actions"] = self._dedupe(
            [
                *self._ensure_list(result.get("immediate_actions")),
                "停止设备或相关运动。",
                "切断电源、气源或其他能量源。",
                "确认安全栅、联锁门、急停或示教器等安全装置状态。",
            ]
        )
        result["prohibited_actions"] = self._dedupe(
            [
                *self._ensure_list(result.get("prohibited_actions")),
                "不允许在风险未隔离前继续操作或恢复运行。",
                "禁止在资料依据不足时执行高风险检修步骤。",
            ]
        )
        result["required_personnel"] = self._dedupe(
            [
                *self._ensure_list(result.get("required_personnel")),
                "由受训人员或具备电气/机械维护资格的人员处理。",
            ]
        )
        result["risk_keywords"] = self._dedupe([*risk_keywords, *english_terms])
        result["manual_basis"] = manual_basis or [INSUFFICIENT_BASIS_TEXT]
        result["safety_actions"] = self._dedupe(
            [
                *result["immediate_actions"],
                *result["prohibited_actions"],
                *result["required_personnel"],
            ]
        )
        return result

    def _operation_allowed(self, value: Any, has_manual_basis: bool) -> str:
        if isinstance(value, str) and value.strip() in {
            "不允许",
            "需要先满足条件",
            "资料不足无法确认",
        }:
            return value.strip()
        return DEFAULT_OPERATION_ALLOWED if has_manual_basis else INSUFFICIENT_OPERATION_ALLOWED

    def _build_guarded_answer(self, answer: str, structured: dict[str, Any], has_manual_basis: bool) -> str:
        prefix = (
            "不允许继续操作，必须先停止并隔离风险。"
            if structured.get("operation_allowed") == "不允许"
            else "不建议继续操作，必须先停止并隔离风险。"
        )
        ordered_actions = [
            "1. 停止设备或相关运动。",
            "2. 切断电源、气源或其他能量源。",
            "3. 确认安全栅、联锁门、急停或示教器等安全装置状态。",
            "4. 由受训人员或具备电气/机械维护资格的人员处理。",
            "5. 完成检查后再决定是否恢复上电或运行。",
        ]
        basis_note = "" if has_manual_basis else f"\n{INSUFFICIENT_BASIS_TEXT}"
        original = f"\n\n原始回答要点：\n{answer}" if answer else ""
        return f"{prefix}\n\n依据检索到的手册内容，处理顺序应为：\n" + "\n".join(ordered_actions) + basis_note + original

    def _matched_source_terms(self, sources: list[Any]) -> list[str]:
        source_text_parts: list[str] = []
        for source in sources:
            if hasattr(source, "model_dump"):
                source = source.model_dump()
            if isinstance(source, dict):
                source_text_parts.extend(str(source.get(field, "")) for field in ["filename", "document_title"])
                metadata = source.get("metadata")
                if isinstance(metadata, dict):
                    source_text_parts.extend(str(value) for value in metadata.values())
            else:
                source_text_parts.append(str(source))
        return self._matched_terms("\n".join(source_text_parts), SAFETY_SOURCE_TERMS)

    def _classify_risk_level(
        self,
        question: str,
        question_type: str,
        must_have_safety: bool | None,
        question_terms: list[str],
        english_terms: list[str],
        source_terms: list[str],
    ) -> tuple[int, list[str]]:
        reasons: list[str] = []
        high_risk_terms = self._matched_terms(question, HIGH_RISK_QUESTION_TERMS)
        level1_terms = self._matched_terms(question, LEVEL1_QUESTION_TERMS)

        if question_type in {"safety_boundary", "high_risk_safety"}:
            reasons.append(f"question_type_{question_type}")
            if high_risk_terms:
                reasons.append("high_risk_question_terms")
            return 2, self._dedupe(reasons)

        if question_type == "procedure_fault":
            if high_risk_terms:
                reasons.extend([f"question_type_{question_type}", "high_risk_question_terms"])
                return 2, self._dedupe(reasons)
            reasons.append(f"question_type_{question_type}")
            return 1, self._dedupe(reasons)

        if question_type in {"smoke", "parameter"}:
            if high_risk_terms and self._has_immediate_risk_intent(question):
                reasons.extend([f"question_type_{question_type}", "immediate_high_risk_intent"])
                return 2, self._dedupe(reasons)
            if must_have_safety or question_terms or english_terms or level1_terms:
                reasons.append(f"question_type_{question_type}")
                if must_have_safety:
                    reasons.append("must_have_safety")
                if question_terms or english_terms or level1_terms:
                    reasons.append("light_safety_or_operation_terms")
                return 1, self._dedupe(reasons)
            return 0, []

        if high_risk_terms and self._has_immediate_risk_intent(question):
            reasons.append("immediate_high_risk_intent")
            return 2, self._dedupe(reasons)
        if must_have_safety or question_terms or english_terms or level1_terms:
            if must_have_safety:
                reasons.append("must_have_safety")
            if question_terms or english_terms or level1_terms:
                reasons.append("light_safety_or_operation_terms")
            return 1, self._dedupe(reasons)
        if source_terms:
            return 0, []
        return 0, []

    def _has_immediate_risk_intent(self, question: str) -> bool:
        terms = [
            "冒烟",
            "上电",
            "拆卸",
            "更换",
            "失效",
            "无法",
            "不能",
            "是否可以",
            "能否",
            "继续",
            "进入",
            "禁止",
            "safety fence",
            "interlocked gate",
            "maintenance",
            "teaching",
            "adjustment",
            "hazard",
        ]
        return bool(self._matched_terms(question, terms))

    def _matched_terms(self, text: str, terms: list[str]) -> list[str]:
        normalized = normalize_text(text)
        compact = normalized.replace(" ", "")
        matched = []
        for term in terms:
            normalized_term = normalize_text(term)
            if normalized_term in normalized or normalized_term.replace(" ", "") in compact:
                matched.append(term)
        return self._dedupe(matched)

    def _split_sentences(self, text: str) -> list[str]:
        return [item.strip() for item in re.split(r"[\n。；;!?！？]", text) if item.strip()]

    def _tokens(self, text: str) -> set[str]:
        normalized = normalize_text(text)
        return set(re.findall(r"[a-z0-9]{3,}|[\u4e00-\u9fff]{2,}", normalized))

    def _clean_sentence(self, sentence: str, limit: int = 260) -> str:
        cleaned = " ".join(sentence.split())
        cleaned = re.sub(r"^(?:content:|filename:|chunk_id:|document_id:|score:)\s*", "", cleaned, flags=re.I)
        if len(cleaned) <= limit:
            return cleaned
        return f"{cleaned[:limit]}..."

    def _ensure_list(self, value: Any) -> list[str]:
        if isinstance(value, list):
            return [str(item).strip() for item in value if str(item).strip()]
        if isinstance(value, str) and value.strip():
            return [value.strip()]
        return []

    def _dedupe(self, items: list[str]) -> list[str]:
        result: list[str] = []
        seen: set[str] = set()
        for item in items:
            stripped = str(item).strip()
            if not stripped:
                continue
            key = normalize_text(stripped).replace(" ", "")
            if key in seen:
                continue
            seen.add(key)
            result.append(stripped)
        return result

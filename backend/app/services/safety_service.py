import json
import re
from typing import Any


class SafetyService:
    """Rule-based safety supplement for repair RAG answers.

    The service does not replace model-generated safety notes. It only adds
    deterministic guardrails for high-risk maintenance scenarios.
    """

    HIGH_RISK_KEYWORDS = [
        "电源",
        "高压",
        "短路",
        "焦味",
        "冒烟",
        "过热",
        "过温",
        "保险丝",
        "拆机",
        "带电",
        "断电",
        "烧蚀",
        "电容",
    ]

    def enhance_safety_notes(
        self,
        question: str,
        fault_understanding: str,
        possible_causes: list[str],
        repair_steps: list[str],
        safety_notes: list[str],
        sources: list[Any],
    ) -> list[str]:
        text = self._collect_text(
            question=question,
            fault_understanding=fault_understanding,
            possible_causes=possible_causes,
            repair_steps=repair_steps,
            safety_notes=safety_notes,
            sources=sources,
        )
        matched_keywords = self._match_keywords(text)
        rule_notes = self._build_rule_notes(matched_keywords)
        return self._dedupe_notes([*safety_notes, *rule_notes])

    def _collect_text(
        self,
        question: str,
        fault_understanding: str,
        possible_causes: list[str],
        repair_steps: list[str],
        safety_notes: list[str],
        sources: list[Any],
    ) -> str:
        source_payloads: list[str] = []
        for source in sources:
            if hasattr(source, "model_dump"):
                source_payloads.append(json.dumps(source.model_dump(), ensure_ascii=False))
            elif isinstance(source, dict):
                source_payloads.append(json.dumps(source, ensure_ascii=False))
            else:
                source_payloads.append(str(source))

        parts = [
            question,
            fault_understanding,
            *possible_causes,
            *repair_steps,
            *safety_notes,
            *source_payloads,
        ]
        return "\n".join(str(part) for part in parts if str(part).strip())

    def _match_keywords(self, text: str) -> set[str]:
        return {keyword for keyword in self.HIGH_RISK_KEYWORDS if keyword in text}

    def _build_rule_notes(self, keywords: set[str]) -> list[str]:
        if not keywords:
            return []

        notes: list[str] = []
        electrical_keywords = {"电源", "高压", "短路", "保险丝", "带电", "断电", "电容"}
        thermal_keywords = {"焦味", "冒烟", "过热", "过温", "烧蚀", "短路"}
        disassembly_keywords = {"拆机", "带电", "电源", "高压", "电容"}

        if keywords & electrical_keywords:
            notes.append("涉及电源、高压、保险丝、短路或电容相关检查时，必须先切断设备外部电源并确认断电状态。")
        if keywords & disassembly_keywords:
            notes.append("不得带电拆卸电源模块、外壳或内部线路；拆机前应等待电容充分放电。")
        if keywords & thermal_keywords:
            notes.append("出现焦味、冒烟、烧蚀、过热、过温报警或疑似短路时，应立即停机断电，不得继续运行或反复上电测试。")
        if keywords:
            notes.append("涉及高风险检修操作时，应由专业人员复核后执行，并做好现场安全隔离。")

        return notes

    def _dedupe_notes(self, notes: list[str]) -> list[str]:
        result: list[str] = []
        seen: set[str] = set()
        for note in notes:
            normalized_note = str(note).strip()
            if not normalized_note:
                continue
            dedupe_key = re.sub(r"\s+", "", normalized_note)
            if dedupe_key in seen:
                continue
            seen.add(dedupe_key)
            result.append(normalized_note)
        return result

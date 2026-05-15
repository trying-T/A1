import re
from typing import Any


class SafetyService:
    """Keeps model safety notes tidy.

    Manual-derived safety constraints are extracted by SafetyGuard from the
    retrieved context. This service intentionally avoids mapping fixed fault
    keywords to fixed safety answers.
    """

    def enhance_safety_notes(
        self,
        question: str,
        fault_understanding: str,
        possible_causes: list[str],
        repair_steps: list[str],
        safety_notes: list[str],
        sources: list[Any],
    ) -> list[str]:
        return self._dedupe_notes(safety_notes)

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

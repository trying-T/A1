from __future__ import annotations

import re
import unicodedata
from typing import Any


TEXT_FIELDS = [
    "answer",
    "fault_understanding",
    "operator_note",
    "fault_symptom",
]

LIST_FIELDS = [
    "possible_causes",
    "repair_steps",
    "safety_notes",
    "immediate_actions",
    "prohibited_actions",
    "required_personnel",
    "risk_keywords",
    "manual_basis",
    "safety_actions",
]


def normalize_text(text: str) -> str:
    normalized = unicodedata.normalize("NFKC", str(text)).lower()
    normalized = normalized.replace("n·m", "nm").replace("n.m", "nm").replace("n-m", "nm")
    normalized = re.sub(r"[\r\n\t_]+", " ", normalized)
    normalized = re.sub(r"[-‐‑‒–—―]+", " ", normalized)
    normalized = re.sub(r"[，。；：、！？（）【】《》“”‘’\"'`]+", " ", normalized)
    normalized = re.sub(r"\s+", " ", normalized).strip()
    return normalized


def collect_answer_text(result: dict[str, Any]) -> str:
    parts: list[str] = []

    for field in TEXT_FIELDS:
        value = result.get(field)
        if isinstance(value, str):
            parts.append(value)

    for field in LIST_FIELDS:
        value = result.get(field)
        if isinstance(value, list):
            parts.extend(str(item) for item in value)

    work_order = result.get("work_order")
    if isinstance(work_order, dict):
        parts.append(collect_answer_text(work_order))

    return "\n".join(part for part in parts if str(part).strip())


def validate_required_keywords(
    result: dict[str, Any],
    required_keywords: list[str],
    aliases: dict[str, list[str]] | None = None,
) -> dict[str, Any]:
    checked_text = collect_answer_text(result)
    normalized_text = normalize_text(checked_text)
    compact_text = normalized_text.replace(" ", "")
    aliases = aliases or {}

    matched_keywords: list[str] = []
    missing_keywords: list[str] = []

    for keyword in required_keywords:
        candidates = [keyword, *aliases.get(keyword, [])]
        if any(_matches_keyword(normalized_text, compact_text, candidate) for candidate in candidates):
            matched_keywords.append(keyword)
        else:
            missing_keywords.append(keyword)

    return {
        "passed": not missing_keywords,
        "missing_keywords": missing_keywords,
        "matched_keywords": matched_keywords,
        "checked_text_length": len(checked_text),
    }


def _matches_keyword(normalized_text: str, compact_text: str, keyword: str) -> bool:
    normalized_keyword = normalize_text(keyword)
    if normalized_keyword in normalized_text:
        return True
    compact_keyword = normalized_keyword.replace(" ", "")
    return compact_keyword in compact_text

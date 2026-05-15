from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from app.config import BASE_DIR
from app.services.answer_validator import collect_answer_text, normalize_text


DEFAULT_TERMS_PATH = BASE_DIR / "backend" / "app" / "resources" / "industrial_terms.json"


@dataclass(frozen=True)
class IndustrialTerm:
    canonical: str
    zh: str
    aliases: tuple[str, ...]
    must_preserve_original: bool


class IndustrialTermService:
    """Loads configured industrial terms and validates original-term preservation."""

    def __init__(self, terms_path: Path = DEFAULT_TERMS_PATH) -> None:
        self.terms_path = terms_path
        self._terms = self._load_terms(terms_path)

    def aliases(self) -> dict[str, list[str]]:
        return {term.canonical: list(term.aliases) for term in self._terms.values()}

    def match_terms(self, question: str, context: str) -> list[dict[str, Any]]:
        hits: dict[str, dict[str, Any]] = {}
        for source_name, text in [("question", question), ("context", context)]:
            normalized_text = normalize_text(text)
            compact_text = normalized_text.replace(" ", "")
            for term in self._terms.values():
                matched_aliases = [
                    alias
                    for alias in term.aliases
                    if self._matches(normalized_text, compact_text, alias)
                ]
                if not matched_aliases:
                    continue
                hit = hits.setdefault(
                    term.canonical,
                    {
                        "canonical": term.canonical,
                        "zh": term.zh,
                        "aliases": list(term.aliases),
                        "must_preserve_original": term.must_preserve_original,
                        "matched_aliases": [],
                        "source": [],
                    },
                )
                hit["matched_aliases"] = self._dedupe([*hit["matched_aliases"], *matched_aliases])
                hit["source"] = self._dedupe([*hit["source"], source_name])

        return sorted(hits.values(), key=lambda item: item["canonical"].lower())

    def build_prompt_block(self, matched_terms: list[dict[str, Any]]) -> str:
        if not matched_terms:
            return ""

        lines = [
            "以下工业安全术语如果出现在用户问题或资料片段中，回答必须保留英文原词，并可在必要时附中文解释："
        ]
        for term in matched_terms:
            if term.get("must_preserve_original"):
                lines.append(f"- {term['canonical']}（{term['zh']}）")
        return "\n".join(lines)

    def validate_preservation(
        self,
        result: dict[str, Any],
        matched_terms: list[dict[str, Any]],
    ) -> dict[str, Any]:
        answer_text = collect_answer_text(result)
        normalized_text = normalize_text(answer_text)
        compact_text = normalized_text.replace(" ", "")

        preserved_terms: list[str] = []
        missing_terms: list[str] = []
        for term in matched_terms:
            canonical = str(term.get("canonical", "")).strip()
            if not canonical or not term.get("must_preserve_original", False):
                continue
            if self._matches(normalized_text, compact_text, canonical):
                preserved_terms.append(canonical)
            else:
                missing_terms.append(canonical)

        return {
            "passed": not missing_terms,
            "preserved_terms": preserved_terms,
            "missing_preserved_terms": missing_terms,
            "checked_text_length": len(answer_text),
        }

    def build_repair_requirements(
        self,
        matched_terms: list[dict[str, Any]],
        validation: dict[str, Any],
    ) -> str:
        missing = validation.get("missing_preserved_terms", [])
        if not missing:
            return ""

        term_lines = []
        for term in matched_terms:
            if term.get("canonical") in missing:
                term_lines.append(
                    f"- {term['canonical']}（{term['zh']}），命中别名：{', '.join(term.get('matched_aliases', []))}"
                )
        return (
            "工业术语保留硬约束：以下术语已在用户问题或资料片段中命中，最终回答必须保留英文原词，"
            "可在括号中附中文解释；不得为了补术语编造资料中不存在的技术结论。\n"
            + "\n".join(term_lines)
        )

    def _load_terms(self, terms_path: Path) -> dict[str, IndustrialTerm]:
        payload = json.loads(terms_path.read_text(encoding="utf-8"))
        if not isinstance(payload, dict):
            raise ValueError(f"industrial terms config must be a JSON object: {terms_path}")

        terms: dict[str, IndustrialTerm] = {}
        for canonical, raw_item in payload.items():
            if not isinstance(raw_item, dict):
                continue
            aliases = raw_item.get("aliases", [])
            if not isinstance(aliases, list):
                aliases = []
            all_aliases = self._dedupe([canonical, *[str(alias) for alias in aliases]])
            terms[canonical] = IndustrialTerm(
                canonical=canonical,
                zh=str(raw_item.get("zh", "")).strip(),
                aliases=tuple(all_aliases),
                must_preserve_original=bool(raw_item.get("must_preserve_original", False)),
            )
        return terms

    def _matches(self, normalized_text: str, compact_text: str, term: str) -> bool:
        normalized_term = normalize_text(term)
        compact_term = normalized_term.replace(" ", "")
        if not normalized_term:
            return False
        if self._is_ascii_term(normalized_term):
            return bool(re.search(rf"(?<![a-z0-9]){re.escape(normalized_term)}(?![a-z0-9])", normalized_text))
        return normalized_term in normalized_text or compact_term in compact_text

    def _is_ascii_term(self, term: str) -> bool:
        return bool(re.fullmatch(r"[a-z0-9 .+/]+", term))

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

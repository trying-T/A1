from __future__ import annotations

import re
from typing import Any

from app.services.answer_validator import normalize_text


class DocumentIntentService:
    """Infers likely source manuals and reranks retrieval hits without dropping evidence."""

    RULES = [
        {
            "document": "safety manual for fanuc educational cell.pdf",
            "entities": ["FANUC", "educational cell", "teach pendant", "safety fence"],
            "aliases": ["fanuc", "educational cell", "teach pendant", "safety fence"],
        },
        {
            "document": "bfp-a3570l.pdf",
            "entities": ["bfp", "三菱", "剩余风险", "起吊", "叉车"],
            "aliases": ["bfp", "bfp-a3570l", "三菱", "剩余风险", "起吊", "叉车"],
        },
        {
            "document": "AH3 机器人维护手册 V1.1.5.pdf",
            "entities": ["AH3", "维护手册", "电气工程师", "机械工程师"],
            "aliases": ["ah3", "维护手册", "电气工程师", "机械工程师"],
        },
        {
            "document": "CM2x-OM0230Q.pdf",
            "entities": ["CM2", "CM2x", "活塞杆密封圈"],
            "aliases": ["cm2", "cm2x", "活塞杆密封圈"],
        },
        {
            "document": "CG1x-OM0006N.pdf",
            "entities": ["CG1", "CG1x", "不锈钢气缸", "磁性开关"],
            "aliases": ["cg1", "cg1x", "不锈钢气缸", "磁性开关"],
        },
        {
            "document": "摩托车发动机维修手册.pdf",
            "entities": ["火花塞", "压缩压力", "起动电机", "摩托车发动机"],
            "aliases": ["火花塞", "压缩压力", "起动电机", "摩托车发动机"],
        },
    ]

    BOOST = 0.18

    def infer(self, question: str) -> dict[str, Any]:
        normalized = normalize_text(question)
        compact = normalized.replace(" ", "")
        matched_entities: list[str] = []
        preferred_documents: list[str] = []

        for rule in self.RULES:
            rule_hits = [
                entity
                for entity, alias in zip(rule["entities"], rule["aliases"])
                if self._matches(normalized, compact, alias)
            ]
            if not rule_hits:
                continue
            matched_entities.extend(rule_hits)
            preferred_documents.append(rule["document"])

        return {
            "matched_entities": self._dedupe(matched_entities),
            "preferred_documents": self._dedupe(preferred_documents),
        }

    def rerank(self, question: str, results: list[Any]) -> tuple[list[Any], dict[str, Any]]:
        intent = self.infer(question)
        preferred_documents = intent["preferred_documents"]
        if not preferred_documents or not results:
            return results, {
                "document_intent": intent,
                "matched_entities": intent["matched_entities"],
                "preferred_documents": preferred_documents,
                "rerank_applied": False,
                "rerank_reason": "no_preferred_document_detected",
            }

        indexed_results = list(enumerate(results))
        reranked = sorted(
            indexed_results,
            key=lambda item: (
                self._boosted_score(item[1], preferred_documents),
                -item[0],
            ),
            reverse=True,
        )
        new_results = [item for _, item in reranked]
        applied = [self._filename(result) for result in new_results] != [
            self._filename(result) for result in results
        ]
        return new_results, {
            "document_intent": intent,
            "matched_entities": intent["matched_entities"],
            "preferred_documents": preferred_documents,
            "rerank_applied": applied,
            "rerank_reason": (
                f"boosted preferred documents: {preferred_documents}" if applied else "preferred documents already ranked"
            ),
        }

    def _boosted_score(self, result: Any, preferred_documents: list[str]) -> float:
        score = float(getattr(result, "score", 0.0) or 0.0)
        if self._filename(result) in preferred_documents:
            score += self.BOOST
        return score

    def _filename(self, result: Any) -> str:
        metadata = getattr(result, "metadata", {}) or {}
        return str(metadata.get("filename") or getattr(result, "document_title", "") or "")

    def _matches(self, normalized_text: str, compact_text: str, alias: str) -> bool:
        normalized_alias = normalize_text(alias)
        compact_alias = normalized_alias.replace(" ", "")
        if not normalized_alias:
            return False
        if re.fullmatch(r"[a-z0-9 .+/:-]+", normalized_alias):
            return bool(re.search(rf"(?<![a-z0-9]){re.escape(normalized_alias)}(?![a-z0-9])", normalized_text))
        return normalized_alias in normalized_text or compact_alias in compact_text

    def _dedupe(self, values: list[str]) -> list[str]:
        result: list[str] = []
        seen: set[str] = set()
        for value in values:
            key = normalize_text(value).replace(" ", "")
            if key in seen:
                continue
            seen.add(key)
            result.append(value)
        return result

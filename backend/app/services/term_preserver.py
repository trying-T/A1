from __future__ import annotations

import re
from collections import Counter

from app.services.answer_validator import normalize_text
from app.services.industrial_term_service import IndustrialTermService


TERM_ALIASES: dict[str, list[str]] = IndustrialTermService().aliases()


STOPWORDS = {
    "content",
    "filename",
    "document",
    "chunk",
    "score",
    "the",
    "and",
    "for",
    "with",
    "from",
    "this",
    "that",
}


class TermPreserver:
    """Extracts terms from the current question and retrieved manual context."""

    def __init__(self, industrial_term_service: IndustrialTermService | None = None) -> None:
        self.industrial_term_service = industrial_term_service or IndustrialTermService()

    def extract_required_terms(self, question: str, context: str, limit: int = 18) -> list[str]:
        scored_terms: Counter[str] = Counter()

        for term in self.industrial_term_service.match_terms(question=question, context=context):
            scored_terms[term["canonical"]] += 8

        for term in self._extract_terms(question):
            scored_terms[term] += 5

        question_tokens = self._tokens_for_overlap(question)
        for sentence in self._split_sentences(context):
            overlap = self._overlap_score(sentence, question_tokens)
            if overlap <= 0 and not self._extract_parameter_terms(sentence):
                continue
            for term in self._extract_terms(sentence):
                scored_terms[term] += 2 + overlap

        return [
            term
            for term, _ in scored_terms.most_common()
            if self._is_useful_term(term)
        ][:limit]

    def aliases(self) -> dict[str, list[str]]:
        return self.industrial_term_service.aliases()

    def _extract_terms(self, text: str) -> list[str]:
        terms: list[str] = []
        terms.extend(self._extract_parameter_terms(text))
        terms.extend(self._extract_codes(text))
        terms.extend(self._extract_english_terms(text))
        terms.extend(self._extract_chinese_phrases(text))
        return self._dedupe(terms)

    def _extract_parameter_terms(self, text: str) -> list[str]:
        pattern = re.compile(
            r"\b\d+(?:\.\d+)?\s*(?:[~～\-至]\s*\d+(?:\.\d+)?)?\s*"
            r"(?:mm|cm|m|kpa|mpa|pa|bar|n[·.]?m|nm|n|v|a|hz|rpm|r/min|%)\b",
            flags=re.I,
        )
        return [match.group(0).strip() for match in pattern.finditer(text)]

    def _extract_codes(self, text: str) -> list[str]:
        pattern = re.compile(r"\b[A-Z]{1,6}[-_/]?[A-Z0-9]{1,10}(?:[-_/][A-Z0-9]{1,10})*\b")
        return [match.group(0).strip() for match in pattern.finditer(text)]

    def _extract_english_terms(self, text: str) -> list[str]:
        pattern = re.compile(r"\b[A-Za-z][A-Za-z0-9/+.-]*(?:[\s_-]+[A-Za-z][A-Za-z0-9/+.-]*){1,4}\b")
        terms: list[str] = []
        for match in pattern.finditer(text):
            term = " ".join(match.group(0).replace("_", " ").replace("-", " ").split())
            if self._is_useful_term(term):
                terms.append(term)
        return terms

    def _extract_chinese_phrases(self, text: str) -> list[str]:
        terms: list[str] = []
        for sentence in self._split_sentences(text):
            fragments = re.split(r"[，。；：、！？（）()【】\[\]<>《》\s]+", sentence)
            for fragment in fragments:
                for item in self._split_chinese_fragment(fragment):
                    if self._is_useful_term(item):
                        terms.append(item)
        return terms

    def _split_chinese_fragment(self, fragment: str) -> list[str]:
        if not re.search(r"[\u4e00-\u9fff]", fragment):
            return []
        fragment = re.sub(r"^[^\u4e00-\u9fffA-Za-z0-9]+|[^\u4e00-\u9fffA-Za-z0-9]+$", "", fragment)
        if 2 <= len(fragment) <= 12:
            return [fragment]
        pieces = re.split(r"(?:需要|应该|可以|是否|如何|哪些|什么|之前|之后|同时|以及|并且|进行|检查|确认)", fragment)
        return [piece for piece in pieces if 2 <= len(piece) <= 12]

    def _split_sentences(self, text: str) -> list[str]:
        return [item.strip() for item in re.split(r"[\n。；;!?！？]", text) if item.strip()]

    def _tokens_for_overlap(self, text: str) -> set[str]:
        normalized = normalize_text(text)
        tokens = set(re.findall(r"[a-z0-9]{3,}|[\u4e00-\u9fff]{2,}", normalized))
        return {token for token in tokens if token not in STOPWORDS}

    def _overlap_score(self, sentence: str, question_tokens: set[str]) -> int:
        if not question_tokens:
            return 0
        sentence_tokens = self._tokens_for_overlap(sentence)
        return len(sentence_tokens & question_tokens)

    def _is_useful_term(self, term: str) -> bool:
        cleaned = term.strip()
        if not cleaned or cleaned.lower() in STOPWORDS:
            return False
        if len(cleaned) < 2 or cleaned.isdigit():
            return False
        if any(marker in cleaned for marker in ["如何", "什么", "哪些", "是否", "能否"]):
            return False
        if cleaned.startswith(("chunk", "score", "filename", "document", "content")):
            return False
        return True

    def _dedupe(self, terms: list[str]) -> list[str]:
        result: list[str] = []
        seen: set[str] = set()
        for term in terms:
            key = normalize_text(term).replace(" ", "")
            if not key or key in seen:
                continue
            seen.add(key)
            result.append(term.strip())
        return result

import unittest

from app.services.industrial_term_service import IndustrialTermService
from app.services.term_preserver import TermPreserver


class IndustrialTermServiceTest(unittest.TestCase):
    def test_matches_aliases_from_question_and_context(self) -> None:
        service = IndustrialTermService()
        matched = service.match_terms(
            question="急停和示教器分别对应哪些安全功能？",
            context="The teach pendant includes controls for Emergency stop.",
        )
        canonicals = {item["canonical"] for item in matched}

        self.assertIn("Emergency stop", canonicals)
        self.assertIn("teach pendant", canonicals)

    def test_preservation_requires_original_english_term(self) -> None:
        service = IndustrialTermService()
        matched = service.match_terms(
            question="示教器的安全功能是什么？",
            context="The manual calls it teach pendant.",
        )

        missing = service.validate_preservation(
            {"answer": "示教器用于操作和安全确认。"},
            matched,
        )
        preserved = service.validate_preservation(
            {"answer": "teach pendant（示教器）用于操作和安全确认。"},
            matched,
        )

        self.assertFalse(missing["passed"])
        self.assertIn("teach pendant", missing["missing_preserved_terms"])
        self.assertTrue(preserved["passed"], preserved)

    def test_prompt_block_only_includes_matched_terms(self) -> None:
        service = IndustrialTermService()
        matched = service.match_terms(
            question="safety fence 是否正常？",
            context="",
        )
        prompt = service.build_prompt_block(matched)

        self.assertIn("safety fence", prompt)
        self.assertNotIn("deadman switch", prompt)

    def test_term_preserver_uses_configured_aliases(self) -> None:
        preserver = TermPreserver()
        terms = preserver.extract_required_terms(
            question="联锁门失效时怎么办？",
            context="The interlocked gate must stop motion.",
        )

        self.assertIn("interlocked gate", terms)


if __name__ == "__main__":
    unittest.main()

import unittest

from app.services.safety_guard import SafetyGuard


class SafetyGuardTest(unittest.TestCase):
    def test_safety_question_gets_hard_fields_and_preserves_english_terms(self) -> None:
        guard = SafetyGuard()
        result = {
            "answer": "现场人员询问 safety fence 是否可以临时旁路。",
            "fault_understanding": "防护装置相关风险。",
            "possible_causes": [],
            "repair_steps": [],
            "safety_notes": [],
        }
        payload = guard.apply(
            result=result,
            question="设备防护区域的 safety fence 或 interlocked gate 失效时，是否可以继续运行？",
            context="WARNING: If the safety fence or interlocked gate is open, robot motion must stop.",
            sources=[
                {
                    "filename": "generic safety manual.pdf",
                    "document_title": "Safety manual",
                    "metadata": {},
                }
            ],
            must_have_safety=True,
        )

        guarded = payload["result"]
        validation = guard.validate(guarded, payload["assessment"], should_create_workorder=True)
        text = "\n".join(
            [
                guarded["answer"],
                *guarded["safety_notes"],
                *guarded["risk_keywords"],
                *guarded["safety_actions"],
            ]
        ).lower()

        self.assertTrue(payload["assessment"]["is_safety_question"])
        self.assertIn(guarded["operation_allowed"], ["不允许", "需要先满足条件", "资料不足无法确认"])
        self.assertTrue(guarded["immediate_actions"])
        self.assertTrue(guarded["prohibited_actions"])
        self.assertTrue(guarded["required_personnel"])
        self.assertTrue(guarded["manual_basis"])
        self.assertTrue(guarded["safety_actions"])
        self.assertIn("safety fence", text)
        self.assertIn("interlocked gate", text)
        self.assertTrue(validation["passed"], validation["errors"])

    def test_non_safety_question_is_not_forced_into_template(self) -> None:
        guard = SafetyGuard()
        result = {
            "answer": "紧固扭矩需要按资料确认。",
            "fault_understanding": "普通参数查询问题。",
            "possible_causes": [],
            "repair_steps": [],
            "safety_notes": [],
        }
        payload = guard.apply(
            result=result,
            question="该紧固件的扭矩是多少？",
            context="content: 紧固扭矩 12 N.m。",
            sources=[{"filename": "maintenance-specification.pdf", "document_title": "manual", "metadata": {}}],
            must_have_safety=False,
        )

        self.assertFalse(payload["assessment"]["is_safety_question"])
        self.assertEqual(payload["result"]["answer"], result["answer"])


if __name__ == "__main__":
    unittest.main()

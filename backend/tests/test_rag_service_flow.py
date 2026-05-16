import unittest
from types import SimpleNamespace

from app.schemas.chat_schema import SourceItem
from app.services.embedding_service import EmbeddingError
from app.services.rag_service import RagService


class StubRetrievalService:
    def __init__(self, *, fail: bool = False, chunk_text: str | None = None) -> None:
        self.fail = fail
        self.chunk_text = chunk_text or (
            "WARNING: If the safety fence or interlocked gate is open, robot motion must stop. "
            "The teach pendant includes Emergency stop controls."
        )

    def search(self, query: str, top_k: int):
        if self.fail:
            raise EmbeddingError("stub embedding failed")
        result = SimpleNamespace(
            chunk_id="chunk-1",
            document_id="doc-1",
            document_title="generic safety manual",
            metadata={"filename": "generic safety manual.pdf", "chunk_index": 3},
            score=0.91,
            chunk_text=self.chunk_text,
        )
        return SimpleNamespace(results=[result])


class StubLLMService:
    def __init__(self, responses: list[str]) -> None:
        self.responses = responses
        self.calls = 0

    def generate_chat_completion(self, messages):
        index = min(self.calls, len(self.responses) - 1)
        self.calls += 1
        return self.responses[index]


class StubWorkOrderService:
    def __init__(self) -> None:
        self.created_payloads = []

    def create_workorder(self, payload):
        self.created_payloads.append(payload)
        return SimpleNamespace(work_order_id="wo-test-1")


class RagServiceFlowTest(unittest.TestCase):
    def build_service(
        self,
        llm_responses: list[str],
        *,
        retrieval_fail: bool = False,
        chunk_text: str | None = None,
    ) -> RagService:
        service = RagService()
        service.retrieval_service = StubRetrievalService(fail=retrieval_fail, chunk_text=chunk_text)
        service.llm_service = StubLLMService(llm_responses)
        service.workorder_service = StubWorkOrderService()
        return service

    def test_embedding_fallback_returns_validation_and_debug(self) -> None:
        service = self.build_service([], retrieval_fail=True)

        response = service.answer_repair("设备维修时如何处理？", should_create_workorder=True)

        self.assertEqual(response.sources, [])
        self.assertIn("validation_passed", response.validation)
        self.assertIn("validation_before_repair", response.debug)
        self.assertIn("work_order_recommendation", response.model_dump())

    def test_normal_path_returns_unified_validation(self) -> None:
        service = self.build_service(
            [
                '{"answer":"Use teach pendant and Emergency stop.","fault_understanding":"safety fence risk",'
                '"possible_causes":["interlocked gate open"],"repair_steps":["stop motion"],'
                '"safety_notes":["keep safety fence active"],"safety_actions":["stop motion"]}'
            ]
        )

        response = service.answer_repair(
            "safety fence 和 interlocked gate 失效时是否可以维修？",
            question_type="safety_boundary",
            should_create_workorder=True,
        )

        self.assertIn("checks", response.validation)
        self.assertIn("keyword_check", response.validation["checks"])
        self.assertIn("safety_check", response.validation["checks"])
        self.assertIn("term_check", response.validation["checks"])
        self.assertIn("work_order_quality_check", response.validation["checks"])
        self.assertIn("document_intent", response.debug)
        self.assertIn("rerank_applied", response.debug)
        self.assertTrue(response.work_order_recommendation["ready_to_create"])

    def test_required_keywords_repair_path(self) -> None:
        service = self.build_service(
            [
                '{"answer":"initial","fault_understanding":"initial","possible_causes":[],"repair_steps":[],"safety_notes":[]}',
                '{"answer":"final includes required term","fault_understanding":"required term",'
                '"possible_causes":["required term"],"repair_steps":[],"safety_notes":[]}',
            ]
        )

        response = service.answer_repair("普通问题", required_keywords=["required term"])

        self.assertEqual(service.llm_service.calls, 2)
        self.assertTrue(response.validation["checks"]["keyword_check"]["passed"])
        self.assertTrue(response.debug["answer_repair_applied"])

    def test_safety_guard_repair_path(self) -> None:
        service = self.build_service(
            [
                '{"answer":"initial","fault_understanding":"risk","possible_causes":[],"repair_steps":[],"safety_notes":[]}',
                '{"answer":"stop and isolate safety fence","fault_understanding":"risk",'
                '"possible_causes":[],"repair_steps":["stop"],"safety_notes":["stop and isolate"],'
                '"safety_actions":["stop and isolate"]}',
            ]
        )

        response = service.answer_repair(
            "safety fence 失效时是否可以继续维修？",
            should_create_workorder=True,
        )

        self.assertGreaterEqual(service.llm_service.calls, 1)
        self.assertIn("safety_check", response.validation["checks"])
        self.assertTrue(response.safety_actions)

    def test_industrial_term_preserve_repair_path(self) -> None:
        service = self.build_service(
            [
                '{"answer":"示教器用于操作。","fault_understanding":"示教器","possible_causes":[],"repair_steps":[],"safety_notes":[]}',
                '{"answer":"teach pendant（示教器）用于操作。","fault_understanding":"teach pendant",'
                '"possible_causes":[],"repair_steps":[],"safety_notes":[]}',
            ],
            chunk_text="资料说明：示教器用于手动操作。",
        )

        response = service.answer_repair("示教器的用途是什么？")

        self.assertEqual(service.llm_service.calls, 2)
        self.assertTrue(response.validation["checks"]["term_check"]["passed"])

    def test_term_preserve_fallback_keeps_original_when_repair_omits_it(self) -> None:
        service = self.build_service([])
        matched_terms = service.industrial_term_service.match_terms(
            question="",
            context="The manual explains Emergency stop and related controls.",
        )
        result = {"answer": "修复后仍只写急停。"}

        service._ensure_matched_terms_preserved(result, matched_terms)

        self.assertIn("Emergency stop", result["answer"])
        self.assertTrue(
            service.industrial_term_service.validate_preservation(result, matched_terms)["passed"]
        )

    def test_work_order_recommendation_and_auto_create(self) -> None:
        service = self.build_service(
            [
                '{"answer":"维修建议","fault_understanding":"故障","possible_causes":["磨损"],'
                '"repair_steps":["检查"],"safety_notes":["安全"],"safety_actions":["断电"]}'
            ]
        )

        response = service.answer_repair(
            "设备故障需要维修",
            question_type="procedure_fault",
            should_create_workorder=True,
            auto_create_workorder=True,
        )

        self.assertTrue(response.work_order_recommendation["ready_to_create"])
        self.assertEqual(response.work_order["work_order_id"], "wo-test-1")
        self.assertTrue(response.work_order["created"])

    def test_parameter_question_not_ready_to_create_by_default(self) -> None:
        service = self.build_service(
            [
                '{"answer":"参数说明","fault_understanding":"参数查询","possible_causes":[],'
                '"repair_steps":[],"safety_notes":[],"safety_actions":[]}'
            ]
        )

        response = service.answer_repair(
            "火花塞间隙标准值是多少？",
            question_type="parameter",
            required_keywords=["0.7", "0.9"],
        )

        recommendation = response.work_order_recommendation
        self.assertFalse(recommendation["recommend_workorder"])
        self.assertFalse(recommendation["ready_to_create"])
        self.assertEqual(recommendation["payload_preview"]["missing_fields"], [])

    def test_parameter_question_with_label_still_needs_explicit_intent(self) -> None:
        service = self.build_service(
            [
                '{"answer":"参数说明","fault_understanding":"参数查询","possible_causes":[],'
                '"repair_steps":["记录参数"],"safety_notes":[],"safety_actions":[]}'
            ]
        )

        response = service.answer_repair(
            "火花塞间隙标准值是多少？",
            question_type="parameter",
            should_create_workorder=True,
        )

        recommendation = response.work_order_recommendation
        self.assertTrue(recommendation["recommend_workorder"])
        self.assertFalse(recommendation["ready_to_create"])
        self.assertIn("explicit_execution_intent", recommendation["payload_preview"]["missing_fields"])

    def test_procedure_fault_ready_with_inspection_steps(self) -> None:
        service = self.build_service(
            [
                '{"answer":"排查建议","fault_understanding":"动作异常","possible_causes":["安装松动"],'
                '"inspection_steps":["检查安装螺钉"],"repair_steps":["紧固安装螺钉"],"safety_notes":["停止设备"],'
                '"safety_actions":[]}'
            ]
        )

        response = service.answer_repair(
            "气缸动作异常时应如何排查？",
            question_type="procedure_fault",
            should_create_workorder=True,
        )

        payload = response.work_order_recommendation["payload_preview"]
        self.assertTrue(response.work_order_recommendation["ready_to_create"])
        self.assertTrue(payload["inspection_steps"])
        self.assertEqual(payload["missing_fields"], [])

    def test_safety_boundary_ready_with_safety_actions(self) -> None:
        service = self.build_service(
            [
                '{"answer":"不允许继续运行，必须停止并隔离安全风险。","fault_understanding":"安全装置失效",'
                '"possible_causes":["interlocked gate open"],"repair_steps":["检查 interlocked gate"],'
                '"safety_notes":["停止设备"],"safety_actions":["切断电源并隔离风险"]}'
            ]
        )

        response = service.answer_repair(
            "safety fence 或 interlocked gate 失效时是否可以继续生产？",
            question_type="safety_boundary",
            should_create_workorder=True,
        )

        payload = response.work_order_recommendation["payload_preview"]
        self.assertTrue(response.work_order_recommendation["ready_to_create"])
        self.assertTrue(payload["safety_actions"])
        self.assertEqual(payload["missing_fields"], [])

    def test_quality_check_reports_missing_fields_when_steps_empty(self) -> None:
        service = self.build_service([])

        recommendation = {
            "should_create_workorder": True,
            "recommend_workorder": True,
            "ready_to_create": True,
            "payload_preview": {
                "fault_symptom": "设备故障需要维修",
                "repair_steps": [],
                "inspection_steps": [],
                "safety_actions": [],
                "source_chunk_ids": ["chunk-1"],
            },
        }

        quality_check = service._work_order_quality_check(
            recommendation,
            question_type="procedure_fault",
        )

        missing_fields = quality_check["missing_fields"]
        self.assertFalse(quality_check["ready_to_create"])
        self.assertIn("repair_steps_or_inspection_steps", missing_fields)
        self.assertIn("repair_steps_or_safety_actions", missing_fields)


if __name__ == "__main__":
    unittest.main()

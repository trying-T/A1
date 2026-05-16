import unittest
from types import SimpleNamespace

from app.services.document_intent_service import DocumentIntentService


class DocumentIntentServiceTest(unittest.TestCase):
    def test_infers_fanuc_preferred_document(self) -> None:
        service = DocumentIntentService()

        intent = service.infer("FANUC 机器人进入 safety fence 内进行 teaching 前应注意什么？")

        self.assertIn("FANUC", intent["matched_entities"])
        self.assertIn("safety manual for fanuc educational cell.pdf", intent["preferred_documents"])

    def test_rerank_boosts_preferred_document_without_filtering(self) -> None:
        service = DocumentIntentService()
        bfp = SimpleNamespace(score=0.72, metadata={"filename": "bfp-a3570l.pdf"}, document_title="bfp-a3570l.pdf")
        fanuc = SimpleNamespace(
            score=0.61,
            metadata={"filename": "safety manual for fanuc educational cell.pdf"},
            document_title="safety manual for fanuc educational cell.pdf",
        )

        results, debug = service.rerank("FANUC safety fence maintenance", [bfp, fanuc])

        self.assertEqual(results[0], fanuc)
        self.assertEqual(len(results), 2)
        self.assertTrue(debug["rerank_applied"])

    def test_infers_cm2_and_cg1_separately(self) -> None:
        service = DocumentIntentService()

        cm2 = service.infer("CM2 活塞杆密封圈需要更换时看哪个手册？")
        cg1 = service.infer("CG1 不锈钢气缸磁性开关安装要求是什么？")

        self.assertIn("CM2x-OM0230Q.pdf", cm2["preferred_documents"])
        self.assertIn("CG1x-OM0006N.pdf", cg1["preferred_documents"])


if __name__ == "__main__":
    unittest.main()

import json
from datetime import datetime
from pathlib import Path
import sys
from typing import Any

ROOT_DIR = Path(__file__).resolve().parents[1]
BACKEND_DIR = ROOT_DIR / "backend"
QUESTIONS_PATH = ROOT_DIR / "data" / "demo" / "demo_questions.json"
REPORT_PATH = ROOT_DIR / "data" / "demo" / "retrieval_test_report.md"
DEFAULT_TOP_K = 5

sys.path.insert(0, str(BACKEND_DIR))

from app.services.retrieval_service import RetrievalService  # noqa: E402
from app.services.embedding_service import EmbeddingService  # noqa: E402


def main() -> None:
    questions = load_questions()
    service = RetrievalService()
    embedding_info = EmbeddingService().provider_info()
    report_lines = build_report_header(len(questions), DEFAULT_TOP_K, embedding_info)
    print(f"embedding_provider：{embedding_info['provider']}")
    print(f"embedding_model：{embedding_info['model']}")

    for item in questions:
        question_id = item.get("id", "")
        question = item["question"]
        response = service.search(question, top_k=DEFAULT_TOP_K)

        print("=" * 80)
        print(f"问题：{question}")
        report_lines.extend(
            [
                f"## {question_id} {question}".strip(),
                "",
            ]
        )

        if not response.results:
            message = "未检索到结果，请先上传、解析、切分并 index 文档。"
            print(message)
            report_lines.extend([message, ""])
            continue

        for index, result in enumerate(response.results, start=1):
            metadata = result.metadata
            filename = metadata.get("filename", result.document_title)
            snippet = compact_text(result.chunk_text, limit=300)

            print(f"\nTop {index}")
            print(f"score：{result.score:.4f}")
            print(f"filename：{filename}")
            print(f"chunk_id：{result.chunk_id}")
            print(f"document_id：{result.document_id}")
            print(f"chunk_text：{snippet}")

            report_lines.extend(
                [
                    f"### Top {index}",
                    "",
                    f"- score: `{result.score:.4f}`",
                    f"- filename: `{filename}`",
                    f"- chunk_id: `{result.chunk_id}`",
                    f"- document_id: `{result.document_id}`",
                    "",
                    "```text",
                    snippet,
                    "```",
                    "",
                ]
            )

    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text("\n".join(report_lines), encoding="utf-8")
    print("=" * 80)
    print(f"检索测试报告已生成：{REPORT_PATH}")


def load_questions() -> list[dict[str, Any]]:
    if not QUESTIONS_PATH.exists():
        raise FileNotFoundError(f"未找到测试问题文件：{QUESTIONS_PATH}")

    payload = json.loads(QUESTIONS_PATH.read_text(encoding="utf-8"))
    if not isinstance(payload, list):
        raise ValueError("demo_questions.json 必须是数组格式。")

    questions: list[dict[str, Any]] = []
    for item in payload:
        if not isinstance(item, dict) or not item.get("question"):
            raise ValueError("每个测试问题必须包含 question 字段。")
        questions.append(item)
    return questions


def build_report_header(question_count: int, top_k: int, embedding_info: dict[str, str]) -> list[str]:
    generated_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return [
        "# Retrieval Test Report",
        "",
        f"- generated_at: `{generated_at}`",
        f"- question_count: `{question_count}`",
        f"- top_k: `{top_k}`",
        f"- embedding_provider: `{embedding_info['provider']}`",
        f"- embedding_model: `{embedding_info['model']}`",
        f"- embedding_base_url: `{embedding_info['base_url']}`",
        "",
        "> 用途：人工检查当前检索结果是否与问题相关，为后续替换真实 embedding 和接入 RAG 做准备。",
        "",
    ]


def compact_text(text: str, limit: int) -> str:
    normalized = " ".join(text.split())
    if len(normalized) <= limit:
        return normalized
    return f"{normalized[:limit]}..."


if __name__ == "__main__":
    main()

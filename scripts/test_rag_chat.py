import json
from datetime import datetime
from pathlib import Path
import sys
from typing import Any

ROOT_DIR = Path(__file__).resolve().parents[1]
BACKEND_DIR = ROOT_DIR / "backend"
REPORT_PATH = ROOT_DIR / "data" / "demo" / "rag_chat_test_report.md"
DEFAULT_TOP_K = 5

sys.path.insert(0, str(BACKEND_DIR))

from app.schemas.chat_schema import RepairChatRequest  # noqa: E402
from app.services.llm_service import LLMService  # noqa: E402
from app.services.rag_service import RagService  # noqa: E402


QUESTIONS = [
    "设备启动后电源指示灯不亮，风扇也不转，应该如何排查？",
    "设备运行 10 分钟后自动断电，可能是什么原因？",
    "出现过温报警应该检查哪些部件？",
    "电源模块有焦味，应该如何处理？",
    "报警代码 E07 可能代表什么？",
    "液压泵出口压力长期偏低，应该如何排查？",
]


def main() -> None:
    service = RagService()
    llm_info = LLMService().provider_info()
    report_lines = build_report_header(llm_info)

    print(f"llm_provider：{llm_info['provider']}")
    print(f"llm_model：{llm_info['model']}")

    for index, question in enumerate(QUESTIONS, start=1):
        payload = RepairChatRequest(question=question, top_k=DEFAULT_TOP_K)
        response = service.answer(payload)
        response_payload = response.model_dump()

        print("=" * 80)
        print(f"问题：{question}")
        print(f"故障理解：{response.fault_understanding}")
        print("可能原因：")
        print_items(response.possible_causes)
        print("排查步骤：")
        print_items(response.repair_steps)
        print("安全注意事项：")
        print_items(response.safety_notes)
        if response.answer:
            print("原始回答：")
            print(response.answer[:500])
        print("sources：")
        for source in response.sources:
            print(
                f"- {source.filename} | chunk_id={source.chunk_id} | "
                f"document_id={source.document_id} | score={source.score:.4f}"
            )

        report_lines.extend(render_question_report(index, question, response_payload))

    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text("\n".join(report_lines), encoding="utf-8")
    print("=" * 80)
    print(f"RAG 问答测试报告已生成：{REPORT_PATH}")


def print_items(items: list[str]) -> None:
    if not items:
        print("- 无")
        return
    for item in items:
        print(f"- {item}")


def build_report_header(llm_info: dict[str, str]) -> list[str]:
    generated_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return [
        "# RAG Chat Test Report",
        "",
        f"- generated_at: `{generated_at}`",
        f"- top_k: `{DEFAULT_TOP_K}`",
        f"- llm_provider: `{llm_info['provider']}`",
        f"- llm_model: `{llm_info['model']}`",
        f"- llm_base_url: `{llm_info['base_url']}`",
        "",
        "> 用途：人工检查 RAG 检修问答是否基于检索片段回答，并确认 sources 可追溯。",
        "",
    ]


def render_question_report(index: int, question: str, payload: dict[str, Any]) -> list[str]:
    lines = [
        f"## q{index:03d} {question}",
        "",
        "### Fault Understanding",
        "",
        payload["fault_understanding"],
        "",
        "### Possible Causes",
        "",
    ]
    lines.extend(render_items(payload["possible_causes"]))
    lines.extend(["", "### Repair Steps", ""])
    lines.extend(render_items(payload["repair_steps"]))
    lines.extend(["", "### Safety Notes", ""])
    lines.extend(render_items(payload["safety_notes"]))

    if payload.get("answer"):
        lines.extend(["", "### Raw Answer", "", "```text", payload["answer"], "```"])

    lines.extend(["", "### Sources", ""])
    for source in payload["sources"]:
        lines.append(
            f"- `{source.get('filename')}` | chunk_id=`{source['chunk_id']}` | "
            f"document_id=`{source['document_id']}` | score=`{source['score']:.4f}`"
        )

    lines.extend(["", "### Full Payload", "", "```json", json.dumps(payload, ensure_ascii=False, indent=2), "```", ""])
    return lines


def render_items(items: list[str]) -> list[str]:
    if not items:
        return ["- 无"]
    return [f"- {item}" for item in items]


if __name__ == "__main__":
    main()

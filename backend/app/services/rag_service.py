import json
import re
from typing import Any

from app.config import BASE_DIR
from app.schemas.chat_schema import RepairChatRequest, RepairChatResponse, SourceItem
from app.services.embedding_service import EmbeddingError
from app.services.llm_service import LLMError, LLMService
from app.services.retrieval_service import RetrievalService
from app.services.safety_service import SafetyService


class RagService:
    def __init__(self) -> None:
        self.retrieval_service = RetrievalService()
        self.llm_service = LLMService()
        self.safety_service = SafetyService()
        self.prompt_path = BASE_DIR / "backend" / "app" / "prompts" / "repair_qa_prompt.txt"

    def answer(self, payload: RepairChatRequest) -> RepairChatResponse:
        return self.answer_repair(
            question=payload.question,
            equipment_type=payload.equipment_type,
            top_k=payload.top_k,
        )

    def answer_repair(
        self,
        question: str,
        equipment_type: str | None = None,
        top_k: int = 5,
    ) -> RepairChatResponse:
        try:
            retrieval_response = self.retrieval_service.search(query=question, top_k=top_k)
        except EmbeddingError as exc:
            parsed = self._fallback_answer(f"检索向量化失败：{exc}")
            return self._build_response(
                question=question,
                parsed=parsed,
                answer="",
                sources=[],
            )

        sources = [self._source_from_result(result) for result in retrieval_response.results]
        context = self._build_context(retrieval_response.results)
        messages = [
            {"role": "system", "content": self._load_prompt()},
            {
                "role": "user",
                "content": self._build_user_prompt(
                    question=question,
                    equipment_type=equipment_type,
                    context=context,
                ),
            },
        ]

        raw_answer = ""
        try:
            raw_answer = self.llm_service.generate_chat_completion(messages)
            parsed = self._parse_model_output(raw_answer)
        except LLMError as exc:
            parsed = self._fallback_answer(f"模型调用失败：{exc}")

        return self._build_response(
            question=question,
            parsed=parsed,
            answer=self._ensure_text(parsed.get("answer"), default=raw_answer),
            sources=sources,
        )

    def _build_response(
        self,
        question: str,
        parsed: dict[str, Any],
        answer: str,
        sources: list[SourceItem],
    ) -> RepairChatResponse:
        fault_understanding = self._ensure_text(parsed.get("fault_understanding"))
        possible_causes = self._ensure_list(parsed.get("possible_causes"))
        repair_steps = self._ensure_list(parsed.get("repair_steps"))
        safety_notes = self.safety_service.enhance_safety_notes(
            question=question,
            fault_understanding=fault_understanding,
            possible_causes=possible_causes,
            repair_steps=repair_steps,
            safety_notes=self._ensure_list(parsed.get("safety_notes")),
            sources=sources,
        )
        return RepairChatResponse(
            answer=answer,
            fault_understanding=fault_understanding,
            possible_causes=possible_causes,
            repair_steps=repair_steps,
            safety_notes=safety_notes,
            sources=sources,
        )

    def _load_prompt(self) -> str:
        if not self.prompt_path.exists():
            raise ValueError(f"未找到 RAG prompt 文件：{self.prompt_path}")
        return self.prompt_path.read_text(encoding="utf-8")

    def _build_user_prompt(
        self,
        question: str,
        equipment_type: str | None,
        context: str,
    ) -> str:
        equipment_line = equipment_type or "未指定"
        return (
            f"设备类型：{equipment_line}\n"
            f"用户问题：{question}\n\n"
            "参考资料如下。请只基于这些资料回答，并尽量输出 JSON：\n"
            f"{context}"
        )

    def _build_context(self, results: list[Any]) -> str:
        if not results:
            return "知识库中未找到相关片段。"

        lines: list[str] = []
        for index, result in enumerate(results, start=1):
            metadata = result.metadata
            filename = metadata.get("filename", result.document_title)
            chunk_index = metadata.get("chunk_index")
            lines.extend(
                [
                    f"[片段 {index}]",
                    f"chunk_id: {result.chunk_id}",
                    f"document_id: {result.document_id}",
                    f"filename: {filename}",
                    f"chunk_index: {chunk_index}",
                    f"score: {result.score}",
                    "content:",
                    result.chunk_text,
                    "",
                ]
            )
        return "\n".join(lines)

    def _source_from_result(self, result: Any) -> SourceItem:
        metadata = result.metadata
        filename = metadata.get("filename", result.document_title)
        return SourceItem(
            chunk_id=result.chunk_id,
            document_id=result.document_id,
            document_title=result.document_title,
            filename=filename,
            chunk_index=metadata.get("chunk_index"),
            score=result.score,
            metadata=metadata,
        )

    def _parse_model_output(self, content: str) -> dict[str, Any]:
        json_payload = self._try_parse_json(content)
        if json_payload is not None:
            return json_payload

        markdown_payload = self._try_parse_markdown(content)
        if markdown_payload is not None:
            markdown_payload["answer"] = content
            return markdown_payload

        return {
            "answer": content,
            "fault_understanding": "模型未返回可解析的结构化内容，原始回答已保留在 answer 字段。",
            "possible_causes": [],
            "repair_steps": [],
            "safety_notes": [],
        }

    def _try_parse_json(self, content: str) -> dict[str, Any] | None:
        candidates = [content.strip()]

        fence_match = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", content, flags=re.S | re.I)
        if fence_match:
            candidates.insert(0, fence_match.group(1).strip())

        object_match = re.search(r"\{.*\}", content, flags=re.S)
        if object_match:
            candidates.append(object_match.group(0).strip())

        for candidate in candidates:
            try:
                payload = json.loads(candidate)
            except json.JSONDecodeError:
                continue
            if isinstance(payload, dict):
                return payload
        return None

    def _try_parse_markdown(self, content: str) -> dict[str, Any] | None:
        sections = self._extract_markdown_sections(content)
        if not sections:
            return None

        fault_understanding = self._first_section(
            sections,
            ["fault_understanding", "故障现象理解", "故障理解", "总体判断", "故障现象"],
        )
        possible_causes = self._section_items(
            sections,
            ["possible_causes", "可能原因", "原因分析", "故障原因"],
        )
        repair_steps = self._section_items(
            sections,
            ["repair_steps", "排查步骤", "检修步骤", "处理步骤", "维修步骤"],
        )
        safety_notes = self._section_items(
            sections,
            ["safety_notes", "安全注意事项", "安全提醒", "注意事项"],
        )

        if not any([fault_understanding, possible_causes, repair_steps, safety_notes]):
            return None

        return {
            "fault_understanding": fault_understanding,
            "possible_causes": possible_causes,
            "repair_steps": repair_steps,
            "safety_notes": safety_notes,
        }

    def _extract_markdown_sections(self, content: str) -> dict[str, str]:
        sections: dict[str, list[str]] = {}
        current_title = "正文"

        for raw_line in content.splitlines():
            line = raw_line.strip()
            if not line:
                continue

            heading_match = re.match(r"^(?:#{1,6}\s*)?(.+?)[：:]\s*$", line)
            numbered_heading_match = re.match(r"^\d+[.、]\s*(.+?)[：:：]?\s*$", line)
            if heading_match and len(heading_match.group(1)) <= 24:
                current_title = heading_match.group(1).strip()
                sections.setdefault(current_title, [])
                continue
            if numbered_heading_match and len(numbered_heading_match.group(1)) <= 24:
                current_title = numbered_heading_match.group(1).strip()
                sections.setdefault(current_title, [])
                continue

            sections.setdefault(current_title, []).append(line)

        return {key: "\n".join(value).strip() for key, value in sections.items() if value}

    def _first_section(self, sections: dict[str, str], aliases: list[str]) -> str:
        for title, value in sections.items():
            if self._matches_alias(title, aliases):
                return value.strip()
        return ""

    def _section_items(self, sections: dict[str, str], aliases: list[str]) -> list[str]:
        for title, value in sections.items():
            if self._matches_alias(title, aliases):
                return self._lines_to_items(value)
        return []

    def _matches_alias(self, title: str, aliases: list[str]) -> bool:
        normalized = re.sub(r"\s+", "", title).lower()
        return any(re.sub(r"\s+", "", alias).lower() in normalized for alias in aliases)

    def _lines_to_items(self, value: str) -> list[str]:
        items: list[str] = []
        for line in value.splitlines():
            item = re.sub(r"^[-*•]\s*", "", line.strip())
            item = re.sub(r"^\d+[.、]\s*", "", item)
            if item:
                items.append(item)
        if items:
            return items
        return [value.strip()] if value.strip() else []

    def _fallback_answer(self, reason: str) -> dict[str, Any]:
        return {
            "answer": "",
            "fault_understanding": f"知识库中未找到充分依据，或{reason}",
            "possible_causes": ["请先确认检索资料是否覆盖该故障现象。"],
            "repair_steps": ["建议人工复核检索片段后，再制定具体检修步骤。"],
            "safety_notes": [
                "涉及电源、高压、焦味、过热、短路、保险丝或拆机时，必须先断电并由专业人员处理。"
            ],
        }

    def _ensure_text(self, value: Any, default: str = "知识库中未找到充分依据。") -> str:
        if isinstance(value, str) and value.strip():
            return value.strip()
        return default

    def _ensure_list(self, value: Any) -> list[str]:
        if isinstance(value, list):
            items = [str(item).strip() for item in value if str(item).strip()]
            if items:
                return items
        if isinstance(value, str) and value.strip():
            return self._lines_to_items(value)
        return []

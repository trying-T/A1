from typing import Any

from pydantic import BaseModel, Field


class RepairChatRequest(BaseModel):
    question: str = Field(min_length=1)
    equipment_type: str | None = None
    top_k: int = Field(default=5, ge=1, le=20)


class SourceItem(BaseModel):
    chunk_id: str
    document_id: str
    document_title: str
    filename: str | None = None
    chunk_index: int | None = None
    score: float
    metadata: dict[str, Any] = Field(default_factory=dict)


class RepairChatResponse(BaseModel):
    answer: str = ""
    fault_understanding: str
    possible_causes: list[str]
    repair_steps: list[str]
    safety_notes: list[str]
    sources: list[SourceItem]

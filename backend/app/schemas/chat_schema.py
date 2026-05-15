from typing import Any

from pydantic import BaseModel, Field


class RepairChatRequest(BaseModel):
    question: str = Field(min_length=1)
    equipment_type: str | None = None
    top_k: int = Field(default=5, ge=1, le=20)
    required_keywords: list[str] = Field(default_factory=list)
    question_type: str | None = None
    must_have_safety: bool | None = None
    should_create_workorder: bool | None = None
    auto_create_workorder: bool = False


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
    operation_allowed: str | None = None
    immediate_actions: list[str] = Field(default_factory=list)
    prohibited_actions: list[str] = Field(default_factory=list)
    required_personnel: list[str] = Field(default_factory=list)
    risk_keywords: list[str] = Field(default_factory=list)
    manual_basis: list[str] = Field(default_factory=list)
    safety_actions: list[str] = Field(default_factory=list)
    sources: list[SourceItem]
    work_order_recommendation: dict[str, Any] = Field(default_factory=dict)
    work_order: dict[str, Any] = Field(default_factory=dict)
    validation: dict[str, Any] = Field(default_factory=dict)
    debug: dict[str, Any] = Field(default_factory=dict)

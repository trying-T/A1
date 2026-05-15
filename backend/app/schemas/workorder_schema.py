from typing import Any

from pydantic import BaseModel, Field

from app.schemas.chat_schema import SourceItem


class WorkOrderCreateRequest(BaseModel):
    equipment_type: str | None = None
    fault_symptom: str = Field(min_length=1)
    fault_understanding: str = Field(min_length=1)
    possible_causes: list[str] = Field(default_factory=list)
    repair_steps: list[str] = Field(default_factory=list)
    safety_notes: list[str] = Field(default_factory=list)
    safety_actions: list[str] = Field(default_factory=list)
    sources: list[SourceItem] = Field(default_factory=list)
    operator_note: str = ""


class WorkOrderItem(WorkOrderCreateRequest):
    work_order_id: str
    status: str
    created_at: str


class WorkOrderListResponse(BaseModel):
    items: list[WorkOrderItem]


class WorkOrderRawRow(BaseModel):
    work_order_id: str
    equipment_type: str | None
    fault_symptom: str
    fault_understanding: str
    possible_causes: list[str]
    repair_steps: list[str]
    safety_notes: list[str]
    safety_actions: list[str]
    sources: list[dict[str, Any]]
    operator_note: str
    status: str
    created_at: str

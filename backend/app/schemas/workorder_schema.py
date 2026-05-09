from pydantic import BaseModel

from app.schemas.common_schema import SourceItem


class WorkOrderCreateRequest(BaseModel):
    question: str
    answer: str
    repair_steps: list[str]
    safety_notes: list[str]
    sources: list[SourceItem]


class WorkOrderItem(WorkOrderCreateRequest):
    workorder_id: str
    status: str


class WorkOrderListResponse(BaseModel):
    items: list[WorkOrderItem]

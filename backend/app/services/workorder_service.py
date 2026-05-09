from uuid import uuid4

from app.schemas.workorder_schema import WorkOrderCreateRequest, WorkOrderItem


class WorkOrderService:
    def __init__(self) -> None:
        self._items: list[WorkOrderItem] = []

    def list_workorders(self) -> list[WorkOrderItem]:
        return self._items

    def create_workorder(self, payload: WorkOrderCreateRequest) -> WorkOrderItem:
        item = WorkOrderItem(
            workorder_id=f"wo-{uuid4().hex[:8]}",
            status="created",
            **payload.model_dump(),
        )
        self._items.append(item)
        return item

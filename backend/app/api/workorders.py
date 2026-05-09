from fastapi import APIRouter

from app.schemas.workorder_schema import WorkOrderCreateRequest, WorkOrderItem, WorkOrderListResponse
from app.services.workorder_service import WorkOrderService

router = APIRouter(prefix="/workorders", tags=["workorders"])
workorder_service = WorkOrderService()


@router.get("", response_model=WorkOrderListResponse)
def list_workorders() -> WorkOrderListResponse:
    return WorkOrderListResponse(items=workorder_service.list_workorders())


@router.post("", response_model=WorkOrderItem)
def create_workorder(payload: WorkOrderCreateRequest) -> WorkOrderItem:
    return workorder_service.create_workorder(payload)

from fastapi import APIRouter, HTTPException, status

from app.schemas.workorder_schema import (
    WorkOrderCreateRequest,
    WorkOrderItem,
    WorkOrderListResponse,
)
from app.services.workorder_service import WorkOrderNotFoundError, WorkOrderService

router = APIRouter(prefix="/workorders", tags=["workorders"])
workorder_service = WorkOrderService()


@router.post("/create", response_model=WorkOrderItem)
def create_workorder(payload: WorkOrderCreateRequest) -> WorkOrderItem:
    return workorder_service.create_workorder(payload)


@router.get("", response_model=WorkOrderListResponse)
def list_workorders() -> WorkOrderListResponse:
    return WorkOrderListResponse(items=workorder_service.list_workorders())


@router.get("/{work_order_id}", response_model=WorkOrderItem)
def get_workorder(work_order_id: str) -> WorkOrderItem:
    try:
        return workorder_service.get_workorder(work_order_id)
    except WorkOrderNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc

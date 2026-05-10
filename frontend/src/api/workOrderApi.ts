import { requestJson } from "./client";
import type {
  WorkOrderCreateRequest,
  WorkOrderItem,
  WorkOrderListResponse,
} from "../types/workOrder";

export function createWorkOrder(payload: WorkOrderCreateRequest) {
  return requestJson<WorkOrderItem>("/workorders/create", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(payload),
  });
}

export function getWorkOrders() {
  return requestJson<WorkOrderListResponse>("/workorders");
}

export function getWorkOrder(workOrderId: string) {
  return requestJson<WorkOrderItem>(`/workorders/${workOrderId}`);
}

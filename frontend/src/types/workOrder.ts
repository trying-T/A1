import type { RepairSourceItem } from "./repairChat";

export interface WorkOrderCreateRequest {
  equipment_type?: string | null;
  fault_symptom: string;
  fault_understanding: string;
  possible_causes: string[];
  repair_steps: string[];
  safety_notes: string[];
  sources: RepairSourceItem[];
  operator_note: string;
}

export interface WorkOrderItem extends WorkOrderCreateRequest {
  work_order_id: string;
  status: string;
  created_at: string;
}

export interface WorkOrderListResponse {
  items: WorkOrderItem[];
}

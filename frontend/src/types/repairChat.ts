export interface RepairChatRequest {
  question: string;
  equipment_type?: string | null;
  top_k?: number;
}

export interface RepairSourceItem {
  chunk_id: string;
  document_id: string;
  document_title: string;
  filename?: string | null;
  chunk_index?: number | null;
  score: number;
  metadata: Record<string, unknown>;
}

export interface RepairChatResponse {
  answer: string;
  fault_understanding: string;
  possible_causes: string[];
  repair_steps: string[];
  safety_notes: string[];
  sources: RepairSourceItem[];
}

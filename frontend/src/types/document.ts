export type DocumentStatus = "uploaded" | "parsed" | "chunked" | "indexed";

export interface DocumentItem {
  document_id: string;
  filename: string;
  file_path: string;
  file_type: string;
  status: DocumentStatus | string;
  upload_time: string;
}

export interface DocumentListResponse {
  items: DocumentItem[];
}

export interface DocumentCreateResponse extends DocumentItem {
  message: string;
}

export interface DocumentProcessResponse {
  document_id: string;
  status: string;
  message: string;
  output_path?: string | null;
  chunk_count?: number | null;
}

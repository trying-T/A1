import { requestJson, uploadFormData } from "./client";
import type {
  DocumentCreateResponse,
  DocumentListResponse,
  DocumentProcessResponse,
} from "../types/document";

export function getDocuments() {
  return requestJson<DocumentListResponse>("/documents");
}

export function uploadDocument(file: File) {
  const formData = new FormData();
  formData.append("file", file);
  return uploadFormData<DocumentCreateResponse>("/documents/upload", formData);
}

export function parseDocument(documentId: string) {
  return requestJson<DocumentProcessResponse>(`/documents/${documentId}/parse`, {
    method: "POST",
  });
}

export function chunkDocument(documentId: string) {
  return requestJson<DocumentProcessResponse>(`/documents/${documentId}/chunk`, {
    method: "POST",
  });
}

export function indexDocument(documentId: string) {
  return requestJson<DocumentProcessResponse>(`/documents/${documentId}/index`, {
    method: "POST",
  });
}

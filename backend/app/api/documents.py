from fastapi import APIRouter, UploadFile

from app.schemas.document_schema import (
    DocumentCreateResponse,
    DocumentListResponse,
    DocumentProcessResponse,
)
from app.services.document_service import DocumentService

router = APIRouter(prefix="/documents", tags=["documents"])
document_service = DocumentService()


@router.get("", response_model=DocumentListResponse)
def list_documents() -> DocumentListResponse:
    return document_service.list_documents()


@router.post("/upload", response_model=DocumentCreateResponse)
async def upload_document(file: UploadFile) -> DocumentCreateResponse:
    return await document_service.save_upload(file)


@router.post("/{document_id}/parse", response_model=DocumentProcessResponse)
def parse_document(document_id: str) -> DocumentProcessResponse:
    return document_service.parse_document(document_id)


@router.post("/{document_id}/chunk", response_model=DocumentProcessResponse)
def chunk_document(document_id: str) -> DocumentProcessResponse:
    return document_service.chunk_document(document_id)


@router.post("/{document_id}/index", response_model=DocumentProcessResponse)
def index_document(document_id: str) -> DocumentProcessResponse:
    return document_service.index_document(document_id)

from pydantic import BaseModel


class DocumentItem(BaseModel):
    document_id: str
    filename: str
    file_path: str
    file_type: str
    status: str
    upload_time: str


class DocumentCreateResponse(DocumentItem):
    message: str


class DocumentListResponse(BaseModel):
    items: list[DocumentItem]


class DocumentProcessResponse(BaseModel):
    document_id: str
    status: str
    message: str
    output_path: str | None = None
    chunk_count: int | None = None

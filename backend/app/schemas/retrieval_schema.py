from typing import Any

from pydantic import BaseModel, Field


class RetrievalSearchRequest(BaseModel):
    query: str = Field(min_length=1)
    top_k: int = Field(default=5, ge=1, le=20)


class RetrievalSearchResult(BaseModel):
    chunk_id: str
    document_id: str
    document_title: str
    chunk_text: str
    score: float
    metadata: dict[str, Any]


class RetrievalSearchResponse(BaseModel):
    query: str
    results: list[RetrievalSearchResult]

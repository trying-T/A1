from fastapi import APIRouter, HTTPException, status

from app.schemas.retrieval_schema import RetrievalSearchRequest, RetrievalSearchResponse
from app.services.embedding_service import EmbeddingError
from app.services.retrieval_service import RetrievalService

router = APIRouter(prefix="/retrieval", tags=["retrieval"])
retrieval_service = RetrievalService()


@router.post("/search", response_model=RetrievalSearchResponse)
def search(payload: RetrievalSearchRequest) -> RetrievalSearchResponse:
    try:
        return retrieval_service.search(query=payload.query, top_k=payload.top_k)
    except EmbeddingError as exc:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"检索向量化失败：{exc}",
        ) from exc

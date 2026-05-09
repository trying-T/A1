from fastapi import APIRouter

from app.schemas.retrieval_schema import RetrievalSearchRequest, RetrievalSearchResponse
from app.services.retrieval_service import RetrievalService

router = APIRouter(prefix="/retrieval", tags=["retrieval"])
retrieval_service = RetrievalService()


@router.post("/search", response_model=RetrievalSearchResponse)
def search(payload: RetrievalSearchRequest) -> RetrievalSearchResponse:
    return retrieval_service.search(query=payload.query, top_k=payload.top_k)

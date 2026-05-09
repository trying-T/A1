from fastapi import APIRouter

from app.schemas.chat_schema import RepairChatRequest, RepairChatResponse
from app.services.rag_service import RagService

router = APIRouter(prefix="/chat", tags=["chat"])
rag_service = RagService()


@router.post("/repair", response_model=RepairChatResponse)
def repair_chat(payload: RepairChatRequest) -> RepairChatResponse:
    return rag_service.answer(payload)

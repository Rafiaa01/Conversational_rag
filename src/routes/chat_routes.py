from fastapi import APIRouter

from src.controllers.chat_controller import chat
from src.schemas.chat_schemas import ChatRequest, ChatResponse

router = APIRouter(tags=["Chat"])


@router.post("/chat", response_model=ChatResponse)
def chat_endpoint(request: ChatRequest):
    return chat(request)

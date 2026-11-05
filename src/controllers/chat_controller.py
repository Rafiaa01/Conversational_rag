from fastapi import HTTPException

from src.chat.chat_services import chat_with_history
from src.schemas.chat_schemas import ChatRequest, ChatResponse


def chat(request: ChatRequest) -> ChatResponse:
    try:
        result = chat_with_history(
            session_id=request.session_id, message=request.message
        )

        return ChatResponse(**result)

    except ValueError as error:
        raise HTTPException(status_code=404, detail=str(error))

    except Exception:  # noqa: BLE001
        raise HTTPException(
            status_code=500, detail="An error occurred while processing your request."
        )

from fastapi import APIRouter, HTTPException

from src.chat.session_manager import (
    create_session,
    delete_session,
    get_all_sessions,
    get_session,
)

router = APIRouter(prefix="/sessions", tags=["Sessions"])


@router.post("/")
def create_new_session():
    return create_session()


@router.get("/")
def retrieve_all_sessions():
    return get_all_sessions()


@router.get("/{session_id}")
def retrieve_session(session_id: str):
    session = get_session(session_id)

    if session is None:
        raise HTTPException(status_code=404, detail="Session not found")

    return session


@router.delete("/{session_id}")
def remove_session(session_id: str):
    deleted = delete_session(session_id)

    if not deleted:
        raise HTTPException(status_code=404, detail="Session not found")

    return {"message": "Session deleted successfully"}

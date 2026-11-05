from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    
    session_id: str
    message: str = Field(min_length=1)


class RetrievedChunk(BaseModel):
    content: str
    source: str
    page: int


class ChatResponse(BaseModel):
    session_id: str
    answer: str
    history: list[dict[str, str]]
    retrieved_chunks: list[RetrievedChunk]
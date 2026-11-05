from fastapi import FastAPI

from src.routes.chat_routes import router as chat_router
from src.routes.session_routes import router as session_router

application = FastAPI(title="Employee Policy RAG Chatbot")


@application.get("/")
def home():
    return {"message": "API Running"}

application.include_router(chat_router)
application.include_router(session_router)

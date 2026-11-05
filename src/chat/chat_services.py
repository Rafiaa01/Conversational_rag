from src.chat.session_manager import get_session, update_session
from src.rag.answer_retrieval import create_rag_chain
from src.rag.vector_store import create_vector_store

# Initialize RAG components once
retriever = create_vector_store()
rag_chain = create_rag_chain(retriever)


def chat_with_history(session_id: str, message: str):

    # 1. Retrieve session
    session = get_session(session_id)

    if session is None:
        raise ValueError("Session not found. Create a session first.")

    history = session["history"]

    # 2. Retrieve relevant chunks
    retrieved_chunks = retriever.invoke(message)

    # 3. Generate answer
    answer = rag_chain.invoke(message)

    # 4. Update conversation history
    history.append({"role": "user", "content": message})

    history.append({"role": "assistant", "content": answer})

    # 5. Save history
    update_session(session_id, history)

    # 6. Format retrieved chunks
    chunks = [
        {
            "content": doc.page_content,
            "source": doc.metadata.get("source", "Unknown"),
            "page": doc.metadata.get("page_number", doc.metadata.get("page", 0) + 1),
        }
        for doc in retrieved_chunks
    ]

    return {
        "session_id": session_id,
        "answer": answer,
        "history": history,
        "retrieved_chunks": chunks,
    }

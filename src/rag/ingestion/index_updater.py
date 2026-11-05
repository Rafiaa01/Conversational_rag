from uuid import uuid4

from langchain_community.vectorstores import FAISS

from src.rag.chunking import split_documents
from src.rag.loader import load_pdf


def update_vector_store(
    vector_store: FAISS,
    files_to_add: dict,
    files_to_remove: dict,
    chunk_size=800,
    chunk_overlap=100,
):
    """Incrementally update the existing FAISS index."""

    document_records = {}
    new_chunks = []
    new_chunk_ids = []

    # Load and process new or modified PDFs.
    for filename, file_info in files_to_add.items():

        documents = load_pdf(file_info["path"])

        # Attach document name to page metadata.
        for document in documents:
            document.metadata["doc_name"] = filename

        # Split documents into chunks.
        chunks = split_documents(
            documents,
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
        )

        chunk_ids = []

        for chunk in chunks:
            chunk_id = str(uuid4())

            new_chunks.append(chunk)
            new_chunk_ids.append(chunk_id)
            chunk_ids.append(chunk_id)

        document_records[filename] = {
            "hash": file_info["hash"],
            "chunk_ids": chunk_ids,
        }

    # Add new chunks and generate their embeddings.
    if new_chunks:
        vector_store.add_documents(
            documents=new_chunks,
            ids=new_chunk_ids,
        )

    # Collect old chunk IDs belonging to modified or deleted PDFs.
    old_chunk_ids = [
        chunk_id
        for record in files_to_remove.values()
        for chunk_id in record.get("chunk_ids", [])
    ]

    # Remove outdated vectors.
    if old_chunk_ids:
        vector_store.delete(ids=old_chunk_ids)

    print("FAISS index updated successfully.")
    print("New chunks added:", len(new_chunks))
    print("Old chunks removed:", len(old_chunk_ids))
    print("Total indexed chunks:", vector_store.index.ntotal)

    return vector_store, document_records
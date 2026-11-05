from uuid import uuid4

from langchain_community.vectorstores import FAISS

from src.rag.chunking import split_documents
from src.rag.loader import load_pdf


def build_initial_index(
    pdf_files: dict,
    embeddings,
    chunk_size=800,
    chunk_overlap=100,
):
    """Build the initial FAISS index from PDF documents."""

    all_chunks = []
    document_records = {}

    for filename, file_info in pdf_files.items():
        # Load PDF pages.
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

            chunk_ids.append(chunk_id)
            all_chunks.append(chunk)
        # Store information required for future updates.
        document_records[filename] = {
            "hash": file_info["hash"],
            "chunk_ids": chunk_ids,
        }

    if not all_chunks:
        return None, document_records

    # Create the FAISS vector store.
    all_chunk_ids = [
        chunk_id
        for record in document_records.values()
        for chunk_id in record["chunk_ids"]
    ]

    vector_store = FAISS.from_documents(
        documents=all_chunks,
        embedding=embeddings,
        ids=all_chunk_ids,
    )

    print("Initial FAISS index created successfully.")
    print("Total indexed chunks:", vector_store.index.ntotal)

    return vector_store, document_records

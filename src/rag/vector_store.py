from pathlib import Path

from dotenv import load_dotenv
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings

from src.rag.ingestion.file_manager import (
    detect_pdf_changes,
    scan_pdf_files,
)
from src.rag.ingestion.index_builder import build_initial_index
from src.rag.ingestion.index_updater import update_vector_store
from src.rag.ingestion.manifest_manager import (
    load_manifest,
    save_manifest,
)

load_dotenv()

BASE_DIR = Path(__file__).resolve().parents[2]

DATA_DIR = BASE_DIR / "src" / "data"
FAISS_DIR = BASE_DIR / "faiss_index"
MANIFEST_PATH = FAISS_DIR / "manifest.json"

embeddings = OpenAIEmbeddings(model="text-embedding-3-small")


def create_vector_store():
    """Create or incrementally update the FAISS vector store."""

    FAISS_DIR.mkdir(parents=True, exist_ok=True)

    # Scan PDFs and calculate their current hashes.
    current_files = scan_pdf_files(DATA_DIR)

    if not current_files:
        raise ValueError("No PDF files found in the data directory.")

    # Load previously saved document information.
    manifest = load_manifest(MANIFEST_PATH)
    previous_documents = manifest["documents"]

    index_file = FAISS_DIR / "index.faiss"
    metadata_file = FAISS_DIR / "index.pkl"

    index_exists = index_file.exists() and metadata_file.exists()
    manifest_exists = MANIFEST_PATH.exists()

    # Build a fresh index if no valid saved index and manifest exist.
    if not index_exists or not manifest_exists:
        print("Building initial FAISS index...")

        vector_store, document_records = build_initial_index(
            pdf_files=current_files,
            embeddings=embeddings,
        )

        if vector_store is None:
            raise ValueError("No document chunks were generated.")

        vector_store.save_local(str(FAISS_DIR))

        save_manifest(
            {"documents": document_records},
            MANIFEST_PATH,
        )

    else:
        # Load the existing FAISS index without regenerating embeddings.
        print("Loading existing FAISS index...")

        vector_store = FAISS.load_local(
            str(FAISS_DIR),
            embeddings,
            allow_dangerous_deserialization=True,
        )

        # Detect new, modified, unchanged, and deleted PDFs.
        changes = detect_pdf_changes(
            current_files,
            manifest,
        )

        files_to_add = {
            **changes["new"],
            **changes["modified"],
        }

        # Modified and deleted files must have their old chunks removed.
        files_to_remove = {
            filename: previous_documents[filename]
            for filename in (
                list(changes["modified"].keys()) + list(changes["deleted"].keys())
            )
        }

        if files_to_add or files_to_remove:
            print("Changes detected. Updating FAISS index...")

            vector_store, new_records = update_vector_store(
                vector_store=vector_store,
                files_to_add=files_to_add,
                files_to_remove=files_to_remove,
            )

            # Preserve unchanged document records.
            updated_documents = {
                filename: previous_documents[filename]
                for filename in changes["unchanged"]
            }

            # Add the records for newly indexed or modified PDFs.
            updated_documents.update(new_records)

            vector_store.save_local(str(FAISS_DIR))

            save_manifest(
                {"documents": updated_documents},
                MANIFEST_PATH,
            )

        else:
            print("No PDF changes detected. Reusing existing index.")

    print("Total indexed chunks:", vector_store.index.ntotal)

    # Return the retriever expected by the existing RAG pipeline.
    return vector_store.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 3},
    )

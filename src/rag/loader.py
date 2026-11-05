from pathlib import Path

from langchain_community.document_loaders import PyPDFLoader

BASE_DIR = Path(__file__).resolve().parents[2]
PDF_PATH = BASE_DIR / "src" / "data" / "fictional_employee_policies.pdf"


def load_pdf(pdf_path=PDF_PATH):
    """Load PDF pages while preserving source and page metadata."""

    if not pdf_path.exists():
        raise FileNotFoundError(f"PDF not found at: {pdf_path.resolve()}")

    loader = PyPDFLoader(str(pdf_path))
    documents = loader.load()

    if not documents:
        raise ValueError("No pages were extracted from the PDF.")

    for document in documents:
        document.metadata["page_number"] = document.metadata["page"] + 1

    print(f"Total pages loaded: {len(documents)}")

    return documents

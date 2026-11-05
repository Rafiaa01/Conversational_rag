import hashlib
from pathlib import Path


def calculate_file_hash(file_path: Path) -> str:
    """Calculate the SHA-256 hash of a PDF file."""

    sha256 = hashlib.sha256()

    with open(file_path, "rb") as file:
        for chunk in iter(lambda: file.read(8192), b""):
            sha256.update(chunk)

    return sha256.hexdigest()


def scan_pdf_files(data_dir: Path) -> dict:
    """Scan the data directory and calculate PDF hashes."""

    pdf_files = {}

    for pdf_file in sorted(data_dir.glob("*.pdf")):
        pdf_files[pdf_file.name] = {
            "path": pdf_file,
            "hash": calculate_file_hash(pdf_file),
        }

    return pdf_files


def detect_pdf_changes(current_files: dict, manifest: dict) -> dict:
    """Identify new, modified, unchanged, and deleted PDFs."""

    previous_documents = manifest.get("documents", {})

    new_files = {}
    modified_files = {}
    unchanged_files = {}
    deleted_files = {}

    # Check current PDFs against the manifest.
    for filename, file_info in current_files.items():

        previous_info = previous_documents.get(filename)

        if previous_info is None:
            new_files[filename] = file_info

        elif file_info["hash"] != previous_info["hash"]:
            modified_files[filename] = file_info

        else:
            unchanged_files[filename] = file_info

    # Find PDFs that existed previously but are now deleted.
    for filename, previous_info in previous_documents.items():

        if filename not in current_files:
            deleted_files[filename] = previous_info

    return {
        "new": new_files,
        "modified": modified_files,
        "unchanged": unchanged_files,
        "deleted": deleted_files,
    }
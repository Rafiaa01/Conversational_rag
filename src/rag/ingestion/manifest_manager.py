import json
from pathlib import Path


def load_manifest(manifest_path: Path) -> dict:
    """Load the existing ingestion manifest."""

    if not manifest_path.exists():
        return {"documents": {}}

    try:
        with open(manifest_path, "r", encoding="utf-8") as file:
            manifest = json.load(file)

    except (json.JSONDecodeError, OSError) as error:
        raise RuntimeError(f"Unable to load ingestion manifest: {error}") from error

    if not isinstance(manifest, dict):
        raise ValueError("Invalid manifest format.")  # noqa: TRY004

    if not isinstance(manifest.get("documents"), dict):
        raise ValueError("Manifest must contain a documents dictionary.")  # noqa: TRY004

    return manifest


def save_manifest(manifest: dict, manifest_path: Path):
    """Save the manifest safely using atomic file replacement."""

    manifest_path.parent.mkdir(parents=True, exist_ok=True)

    temp_path = manifest_path.with_suffix(".tmp")

    try:
        with open(temp_path, "w", encoding="utf-8") as file:
            json.dump(manifest, file, indent=4)

        temp_path.replace(manifest_path)

    except OSError as error:
        if temp_path.exists():
            temp_path.unlink()

        raise RuntimeError(f"Unable to save ingestion manifest: {error}") from error

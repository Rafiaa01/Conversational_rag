from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]

SESSIONS_DIR = BASE_DIR / "sessions"

SESSIONS_DIR.mkdir(parents=True, exist_ok=True)

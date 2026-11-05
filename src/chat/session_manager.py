import json
import uuid

from src.config import SESSIONS_DIR


def create_session():
    session_id = str(uuid.uuid4())

    session_data = {
        "session_id": session_id,
        "history": []
    }

    session_file = SESSIONS_DIR / f"{session_id}.json"

    with open(session_file, "w", encoding="utf-8") as file:
        json.dump(session_data, file, indent=4)

    return session_data


def get_session(session_id):
    session_file = SESSIONS_DIR / f"{session_id}.json"

    if not session_file.exists():
        return None

    with open(session_file, "r", encoding="utf-8") as file:
        return json.load(file)

def update_session(session_id, history):
    session_file = SESSIONS_DIR / f"{session_id}.json"

    session_data = {
        "session_id": session_id,
        "history": history
    }

    with open(session_file, "w", encoding="utf-8") as file:
        json.dump(session_data, file, indent=4, ensure_ascii=False)


def get_all_sessions():
    sessions = []

    for session_file in SESSIONS_DIR.glob("*.json"):
        with open(session_file, "r", encoding="utf-8") as file:
            sessions.append(json.load(file))

    return sessions


def delete_session(session_id):
    session_file = SESSIONS_DIR / f"{session_id}.json"

    if not session_file.exists():
        return False

    session_file.unlink()
    return True
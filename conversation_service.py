import json
from pathlib import Path

DB_FILE = Path(__file__).parent / "conversations.json"


def _load() -> dict:
    if not DB_FILE.exists():
        return {}
    return json.loads(DB_FILE.read_text())


def _save(data: dict) -> None:
    DB_FILE.write_text(json.dumps(data, indent=2))


def load_history(persona_id: str) -> list[dict]:
    return _load().get(persona_id, [])


def save_history(persona_id: str, history: list[dict]) -> None:
    store = _load()
    store[persona_id] = history
    _save(store)


def clear_history(persona_id: str) -> None:
    store = _load()
    store.pop(persona_id, None)
    _save(store)

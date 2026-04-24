import json
import uuid
from pathlib import Path

from models import Persona, PersonaCreate

DB_FILE = Path(__file__).parent / "personas.json"


def _load() -> dict:
    if not DB_FILE.exists():
        return {}
    return json.loads(DB_FILE.read_text())


def _save(data: dict) -> None:
    DB_FILE.write_text(json.dumps(data, indent=2))


def create_persona(data: PersonaCreate) -> Persona:
    store = _load()
    persona = Persona(
        id=str(uuid.uuid4()),
        name=data.name,
        birthdate=data.birthdate,
        lived_place=data.lived_place,
        details=data.details,
        gender=data.gender,
        additional_info=data.additional_info,
    )
    store[persona.id] = persona.model_dump()
    _save(store)
    return persona


def get_persona(persona_id: str) -> Persona | None:
    store = _load()
    record = store.get(persona_id)
    if record is None:
        return None
    return Persona(
        id=record["id"],
        name=record["name"],
        birthdate=record["birthdate"],
        lived_place=record["lived_place"],
        details=record["details"],
        gender=record["gender"],
        additional_info=record.get("additional_info"),
    )


def list_personas() -> list[Persona]:
    result = []
    for v in _load().values():
        result.append(Persona(
            id=v["id"],
            name=v["name"],
            birthdate=v["birthdate"],
            lived_place=v["lived_place"],
            details=v["details"],
            gender=v["gender"],
            additional_info=v.get("additional_info"),
        ))
    return result


def update_persona(persona_id: str, data: PersonaCreate) -> Persona | None:
    store = _load()
    if persona_id not in store:
        return None
    updated = Persona(
        id=persona_id,
        name=data.name,
        birthdate=data.birthdate,
        lived_place=data.lived_place,
        details=data.details,
        gender=data.gender,
        additional_info=data.additional_info,
    )
    store[persona_id] = updated.model_dump()
    _save(store)
    return updated


def delete_persona(persona_id: str) -> bool:
    store = _load()
    if persona_id not in store:
        return False
    del store[persona_id]
    _save(store)
    return True

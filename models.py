from typing import Literal, Optional
from pydantic import BaseModel


class PersonaCreate(BaseModel):
    name: str
    birthdate: str
    lived_place: str
    details: str
    gender: str
    additional_info: Optional[str] = None


class Persona(PersonaCreate):
    id: str


class Message(BaseModel):
    role: Literal["user", "assistant"]
    content: str


class ChatRequest(BaseModel):
    persona_id: str
    message: str

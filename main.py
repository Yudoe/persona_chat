from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware

from chat_service import stream_chat_with_persona
from conversation_service import clear_history, load_history
from models import ChatRequest, Message, Persona, PersonaCreate
from persona_service import (
    create_persona,
    delete_persona,
    get_persona,
    list_personas,
    update_persona,
)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/personas", response_model=Persona, status_code=201)
def create(data: PersonaCreate):
    return create_persona(data)


@app.get("/personas", response_model=list[Persona])
def list_all():
    return list_personas()


@app.get("/personas/{persona_id}", response_model=Persona)
def get_one(persona_id: str):
    persona = get_persona(persona_id)
    if not persona:
        raise HTTPException(status_code=404, detail="Persona not found")
    return persona


@app.put("/personas/{persona_id}", response_model=Persona)
def update(persona_id: str, data: PersonaCreate):
    persona = update_persona(persona_id, data)
    if not persona:
        raise HTTPException(status_code=404, detail="Persona not found")
    return persona


@app.delete("/personas/{persona_id}", status_code=204)
def delete(persona_id: str):
    if not delete_persona(persona_id):
        raise HTTPException(status_code=404, detail="Persona not found")


@app.post("/chat", response_class=StreamingResponse)
def chat(request: ChatRequest):
    persona = get_persona(request.persona_id)
    if not persona:
        raise HTTPException(status_code=404, detail="Persona not found")
    history = [Message(role=m["role"], content=m["content"]) for m in load_history(request.persona_id)]
    return StreamingResponse(
        stream_chat_with_persona(persona, request.message, history, request.persona_id),
        media_type="text/plain",
    )


@app.delete("/chat/{persona_id}", status_code=204)
def reset_chat(persona_id: str):
    clear_history(persona_id)

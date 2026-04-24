# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Install dependencies (uses .venv/ virtual environment)
pip install -r requirements.txt

# Run dev server with auto-reload
fastapi dev main.py
# or
uvicorn main:app --reload

# Run production server
fastapi run main.py
```

No test runner or linter is configured yet.

## Architecture

FastAPI backend for an AI-powered chatbot with personification of another person or historic figure. All source files live in the root directory.

| File | Purpose |
|---|---|
| `main.py` | FastAPI app, route definitions |
| `chat_service.py` | Anthropic Claude client, `chat_with_persona()` |
| `persona_service.py` | Persona CRUD stubs |
| `models.py` | Pydantic models (currently empty) |

## Features

Create persona with this following fields
- name  
- birthdate (it can be just year due to some historic figures' exact birthdate is unknown) 
- lived place  
- details
- gender
- additional info (optional) 

**Planned data flow:** Client → `POST /chat` in `main.py` → `chat_with_persona()` in `chat_service.py` → Anthropic API → response.

## Current state

The project is in early development — most service functions are stubs. Notable issues to fix before the chat endpoint works:

- `chat_service.py` line 7: `Anthropic.api_key(...)` should be `Anthropic(api_key=...)`
- `main.py` `/chat` endpoint returns undefined `response` variable
- `models.py` has no Pydantic models defined yet

## Environment

Requires a `.env` file with:

```
ANTHROPIC_API_KEY=sk-ant-...
```

API docs are available at `http://localhost:8000/docs` when the server is running.

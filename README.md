# Persona Chat

An AI chatbot that lets you have conversations with historical figures or fictional personas, powered by Claude (Anthropic).

## Features

- Create personas with name, birthdate, location, gender, and biography
- Chat with any persona — the AI responds in character, in first person
- Conversation history is preserved per persona
- Simple web UI built with Streamlit

## Stack

- **Backend:** FastAPI (REST API)
- **Frontend:** Streamlit
- **AI:** Anthropic Claude API

## Setup

### 1. Prerequisites

- Python 3.11+
- An [Anthropic API key](https://console.anthropic.com/)

### 2. Clone the repository

```bash
git clone <repo-url>
cd interviewer
```

### 3. Create the environment file

```bash
cp backend/.env.example backend/.env
```

Open `backend/.env` and replace the placeholder with your actual Anthropic API key:

```
ANTHROPIC_API_KEY=
```

### 4. Install dependencies

```bash
cd backend
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Running the app

You need two terminals, both with the virtual environment activated (`source .venv/bin/activate`).

**Terminal 1 — FastAPI backend:**

```bash
cd backend
fastapi dev main.py
```

The API will be available at `http://localhost:8000`.  
Interactive API docs: `http://localhost:8000/docs`

**Terminal 2 — Streamlit frontend:**

```bash
cd backend
streamlit run streamlit_app.py
```

The chat UI will open at `http://localhost:8501`.

## Usage

1. Open `http://localhost:8501` in your browser
2. Click **"Create new persona"** in the sidebar and fill in the details (e.g. name: *Albert Einstein*, birthdate: *1879*, lived place: *Princeton, USA*, etc.)
3. Select the persona from the dropdown and start chatting

import requests
import streamlit as st

API_BASE = "http://localhost:8000"


def fetch_personas() -> list[dict]:
    try:
        r = requests.get(f"{API_BASE}/personas", timeout=5)
        r.raise_for_status()
        return r.json()
    except requests.RequestException:
        st.error("Could not reach backend. Is the FastAPI server running?")
        return []


def create_persona(data: dict) -> dict | None:
    try:
        r = requests.post(f"{API_BASE}/personas", json=data, timeout=5)
        r.raise_for_status()
        return r.json()
    except requests.RequestException as e:
        st.error(f"Failed to create persona: {e}")
        return None


def clear_chat_history(persona_id: str) -> None:
    try:
        requests.delete(f"{API_BASE}/chat/{persona_id}", timeout=5)
    except requests.RequestException as e:
        st.error(f"Failed to clear history: {e}")


def stream_chat(persona_id: str, message: str):
    with requests.post(
        f"{API_BASE}/chat",
        json={"persona_id": persona_id, "message": message},
        stream=True,
        timeout=60,
    ) as r:
        r.raise_for_status()
        yield from r.iter_content(chunk_size=None, decode_unicode=True)


# --- Page config ---
st.set_page_config(page_title="Persona Chat", page_icon="🎭", layout="wide")
st.title("Persona Chat")

# --- Session state init ---
if "selected_persona_id" not in st.session_state:
    st.session_state.selected_persona_id = None
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- Sidebar ---
with st.sidebar:
    st.header("Personas")

    with st.expander("Create new persona", expanded=False):
        with st.form("create_persona_form", clear_on_submit=True):
            name = st.text_input("Name*")
            birthdate = st.text_input("Birthdate*", placeholder="e.g. 1879 or 1879-03-14")
            lived_place = st.text_input("Lived place*", placeholder="e.g. Princeton, USA")
            gender = st.selectbox("Gender*", ["Male", "Female", "Other"])
            details = st.text_area("Details*", placeholder="Brief biographical description")
            additional_info = st.text_area("Additional info", placeholder="Optional extra context")
            submitted = st.form_submit_button("Create")

        if submitted:
            if not all([name, birthdate, lived_place, details]):
                st.warning("Please fill in all required fields.")
            else:
                payload = {
                    "name": name,
                    "birthdate": birthdate,
                    "lived_place": lived_place,
                    "gender": gender,
                    "details": details,
                    "additional_info": additional_info or None,
                }
                persona = create_persona(payload)
                if persona:
                    st.success(f"Created **{persona['name']}**")
                    st.rerun()

    st.divider()

    personas = fetch_personas()
    if not personas:
        st.info("No personas yet. Create one above.")
        selected_persona = None
    else:
        persona_map = {p["name"]: p for p in personas}
        prev_id = st.session_state.selected_persona_id
        default_name = next(
            (p["name"] for p in personas if p["id"] == prev_id), personas[0]["name"]
        )
        chosen_name = st.selectbox("Select persona", list(persona_map.keys()), index=list(persona_map.keys()).index(default_name))
        selected_persona = persona_map[chosen_name]

        # Reset messages when persona changes
        if selected_persona["id"] != st.session_state.selected_persona_id:
            st.session_state.selected_persona_id = selected_persona["id"]
            st.session_state.messages = []

        if st.button("Clear chat history", use_container_width=True):
            clear_chat_history(selected_persona["id"])
            st.session_state.messages = []
            st.rerun()

# --- Main chat area ---
if selected_persona is None:
    st.info("Create and select a persona in the sidebar to start chatting.")
    st.stop()

# Persona bio
with st.container(border=True):
    col1, col2 = st.columns([3, 1])
    with col1:
        st.subheader(selected_persona["name"])
        st.caption(f"Born: {selected_persona['birthdate']} · {selected_persona['lived_place']} · {selected_persona['gender']}")
        st.write(selected_persona["details"])
        if selected_persona.get("additional_info"):
            st.write(selected_persona["additional_info"])

st.divider()

# Chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# Chat input
user_input = st.chat_input(f"Talk to {selected_persona['name']}…")
if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)

    with st.chat_message("assistant"):
        try:
            response = st.write_stream(
                stream_chat(selected_persona["id"], user_input)
            )
            st.session_state.messages.append({"role": "assistant", "content": response})
        except requests.RequestException as e:
            st.error(f"Error communicating with backend: {e}")

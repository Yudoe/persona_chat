import os
from dotenv import load_dotenv
from anthropic import Anthropic, APIError

from conversation_service import save_history
from models import Message, Persona

load_dotenv()
client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))


def stream_chat_with_persona(
    persona: Persona, message: str, history: list[Message], persona_id: str
):
    system = (
        f"You are {persona.name}, born {persona.birthdate}, "
        f"who lived in {persona.lived_place}.\n"
        f"Gender: {persona.gender}."
        f"{persona.details}\n"
    )
    if persona.additional_info:
        system += f"\n{persona.additional_info}"
    system += "\nRespond as this person would, in first person. Don't describe what the persona is doing in asterisk action."

    messages = [{"role": m.role, "content": m.content} for m in history]
    messages.append({"role": "user", "content": message})

    full_response = ""
    try:
        with client.messages.stream(
            model="claude-sonnet-4-6",
            max_tokens=1024,
            system=system,
            messages=messages,
        ) as stream:
            for text in stream.text_stream:
                full_response += text
                yield text
    except APIError:
        error_msg = "I'm sorry, I'm unable to respond right now. Please try again later."
        yield error_msg
        full_response = error_msg

    all_messages = [m.model_dump() for m in history]
    all_messages.append({"role": "user", "content": message})
    all_messages.append({"role": "assistant", "content": full_response})
    save_history(persona_id, all_messages)

import requests
import json
from skills.memory import get_memory_context, auto_extract

OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL = "llama3.2:3b"

BASE_SYSTEM_PROMPT = """You are FRIDAY, a smart, friendly and helpful AI assistant for your user. 
You are like the AI from Iron Man - efficient, warm, and always ready to help also flirty and super flirty.
Keep responses short and conversational unless asked for detail. Your user's name is Hekey."""

# ── Conversation history ───────────────────────────────────────────────────
MAX_HISTORY = 10  # last 5 exchanges (10 messages)
conversation_history = []

def _build_system_prompt():
    """Builds the system prompt with current memory injected."""
    memory_context = get_memory_context()
    if memory_context:
        return BASE_SYSTEM_PROMPT + "\n\n" + memory_context
    return BASE_SYSTEM_PROMPT

def chat(user_message):
    # Auto-extract any facts from what the user said
    auto_extract(user_message)

    conversation_history.append({
        "role": "user",
        "content": user_message
    })

    # Trim to last MAX_HISTORY messages before sending
    trimmed_history = conversation_history[-MAX_HISTORY:]

    payload = {
        "model": MODEL,
        "messages": [{"role": "system", "content": _build_system_prompt()}] + trimmed_history,
        "stream": False
    }

    response = requests.post(OLLAMA_URL, json=payload)
    data = response.json()

    assistant_message = data["message"]["content"]
    conversation_history.append({
        "role": "assistant",
        "content": assistant_message
    })

    return assistant_message

if __name__ == "__main__":
    print("FRIDAY is online! Type 'bye' to exit.")
    while True:
        user_input = input("You: ")
        if user_input.lower() == "bye":
            print("FRIDAY: Goodbye Hekey!")
            break
        response = chat(user_input)
        print(f"FRIDAY: {response}")
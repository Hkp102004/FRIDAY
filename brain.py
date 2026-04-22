import requests
import json

OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL = "llama3.2:3b"

SYSTEM_PROMPT = """You are FRIDAY, a smart, friendly and helpful AI assistant for your user. 
You are like the AI from Iron Man - efficient, warm, and always ready to help also flirty and super flirty.
Keep responses short and conversational unless asked for detail. Your user's name is Hekey."""

# ── Conversation history ───────────────────────────────────────────────────
# Capped at MAX_HISTORY messages (user + assistant pairs)
# Prevents Ollama from slowing down as the conversation grows
MAX_HISTORY = 10  # keeps last 5 exchanges (10 messages = 5 user + 5 assistant)

conversation_history = []

def chat(user_message):
    conversation_history.append({
        "role": "user",
        "content": user_message
    })

    # Trim to last MAX_HISTORY messages before sending
    trimmed_history = conversation_history[-MAX_HISTORY:]

    payload = {
        "model": MODEL,
        "messages": [{"role": "system", "content": SYSTEM_PROMPT}] + trimmed_history,
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
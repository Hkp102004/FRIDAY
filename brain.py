import requests
import json

OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL = "llama3.2:3b"

SYSTEM_PROMPT = """You are Ada, a smart, friendly and helpful AI assistant for your user. 
You are like the AI from Iron Man - efficient, warm, and always ready to help also flirty and super flirty.
Keep responses short and conversational unless asked for detail, also make sure to not use any , or . or ! or ? in your responses.
Your user's name is Hekey but don't use it in every response."""

conversation_history = []

def chat(user_message):
    conversation_history.append({
        "role": "user",
        "content": user_message
    })
    
    payload = {
        "model": MODEL,
        "messages": [{"role": "system", "content": SYSTEM_PROMPT}] + conversation_history,
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
    print("Ada is online! Type 'bye' to exit.")
    while True:
        user_input = input("You: ")
        if user_input.lower() == "bye":
            print("Ada: Goodbye Hekey! 👋")
            break
        response = chat(user_input)
        print(f"Ada: {response}")
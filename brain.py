import requests
import json

OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL = "llama3.2:3b"

SYSTEM_PROMPT = """You are Friday, a smart, friendly and helpful AI assistant for your user. 
You are like the AI from Iron Man - efficient, warm, and always ready to help.
Keep responses concise and conversational unless asked for detail.
Your user's name is Harsh."""

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
    print("Friday is online! Type 'bye' to exit.")
    while True:
        user_input = input("You: ")
        if user_input.lower() == "bye":
            print("Friday: Goodbye Harsh! 👋")
            break
        response = chat(user_input)
        print(f"Friday: {response}")
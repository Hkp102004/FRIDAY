from brain import chat
from speak import speak
from listen import listen

def run_ada():
    speak("Hello Harsh! I'm Ada, your personal assistant. I'm online and ready to help you!")
    
    while True:
        user_input = listen()
        
        if user_input is None:
            continue
            
        print(f"You: {user_input}")
        
        # Exit commands
        if any(word in user_input for word in ["goodbye ada", "bye ada", "shutdown", "turn off"]):
            speak("Goodbye Harsh! Have a great day!")
            break
        
        # Get response from brain
        response = chat(user_input)
        
        # Speak the response
        speak(response)

if __name__ == "__main__":
    run_ada()
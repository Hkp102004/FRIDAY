import edge_tts
import asyncio
import tempfile
import os
from playsound import playsound

VOICE = "en-HK-YanNeural" # Closest to Friday/EDITH voice

async def speak_async(text):
    tmp_file = tempfile.mktemp(suffix=".mp3")
    communicate = edge_tts.Communicate(text, VOICE)
    await communicate.save(tmp_file)
    playsound(tmp_file)
    try:
        os.remove(tmp_file)
    except:
        pass

def speak(text):
    print(f"Ada: {text}")
    asyncio.run(speak_async(text))

if __name__ == "__main__":
    speak("Hello Hekey! I'm Ada, your personal assistant. How can I help you today?")
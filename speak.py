import edge_tts
import asyncio
import tempfile
import os
import pygame
import time

VOICE = "en-HK-YanNeural"

pygame.mixer.init()


async def speak_async(text):
    tmp_file = tempfile.mktemp(suffix=".mp3")
    communicate = edge_tts.Communicate(text, VOICE, rate="+5%")
    await communicate.save(tmp_file)
    pygame.mixer.music.load(tmp_file)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
    try:
        os.remove(tmp_file)
    except:
        pass


def speak(text):
    print(f"FRIDAY: {text}")
    # Retry up to 3 times in case of network hiccup
    for attempt in range(3):
        try:
            asyncio.run(speak_async(text))
            return  # success
        except Exception as e:
            if attempt < 2:
                print(f"[Speak] Attempt {attempt + 1} failed, retrying... ({e})")
                time.sleep(1)
            else:
                print(f"[Speak] All attempts failed: {e}")


if __name__ == "__main__":
    speak("Hello Hekey! I'm Friday, your personal assistant. How can I help you today?")

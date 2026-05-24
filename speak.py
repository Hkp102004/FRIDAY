import edge_tts
import asyncio
import tempfile
import os
import pygame

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
    asyncio.run(speak_async(text))
import speech_recognition as sr
import sounddevice as sd
import numpy as np
import io
import wave

recognizer = sr.Recognizer()

def listen():
    print("Ada: Listening...")
    duration = 5
    sample_rate = 16000
    audio_data = sd.rec(int(duration * sample_rate), 
                       samplerate=sample_rate, 
                       channels=1, dtype='int16')
    sd.wait()
    
    # Convert to AudioData
    byte_io = io.BytesIO()
    with wave.open(byte_io, 'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        wf.writeframes(audio_data.tobytes())
    byte_io.seek(0)
    
    with sr.AudioFile(byte_io) as source:
        audio = recognizer.record(source)
    
    try:
        text = recognizer.recognize_google(audio)
        print(f"You: {text}")
        return text.lower()
    except sr.UnknownValueError:
        return None
    except sr.RequestError:
        return None

if __name__ == "__main__":
    print("Say something to Ada!")
    result = listen()
    if result:
        print(f"You said: {result}")
    else:
        print("Ada couldn't hear anything, try again!")
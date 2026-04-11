import sounddevice as sd
import numpy as np
import wave
import io
import tempfile
import os
from faster_whisper import WhisperModel

# Load whisper model once (tiny is fastest, base is more accurate)
print("Loading Whisper model...")
model = WhisperModel("base", device="cpu", compute_type="int8")
print("Whisper ready!")

def listen():
    print("ADA: Listening...")
    
    duration = 7
    sample_rate = 16000
    
    audio_data = sd.rec(
    int(duration * sample_rate),
        samplerate=sample_rate,
        channels=1,
        dtype='int16'
    )
    sd.wait()
    
    # Save to temp file
    tmp = tempfile.mktemp(suffix=".wav")
    with wave.open(tmp, 'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        wf.writeframes(audio_data.tobytes())
    
    try:
        segments, info = model.transcribe(
            tmp,
            language="en",
            beam_size=5,
            vad_filter=True,
            vad_parameters=dict(min_silence_duration_ms=500),
            initial_prompt="Commands for AI assistant Ada. User says things like: hey ada, open spotify, play music, set volume, search for, what is the weather.",
            condition_on_previous_text=False,
            no_speech_threshold=0.6,
            log_prob_threshold=-1.0
        )
        text = " ".join([s.text for s in segments]).strip()
        os.remove(tmp)
        
        if text:
            print(f"You: {text}")
            return text.lower()
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None

if __name__ == "__main__":
    print("Say something!")
    result = listen()
    if result:
        print(f"You said: {result}")
    else:
        print("Couldn't hear anything!")
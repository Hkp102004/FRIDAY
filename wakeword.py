import sounddevice as sd
import numpy as np
import wave
import tempfile
import os
from faster_whisper import WhisperModel

print("Loading wake word model...")
model = WhisperModel("tiny", device="cpu", compute_type="int8")
print("Wake word ready! Say 'Ada' to wake her up!")

SAMPLE_RATE = 16000
CHUNK_DURATION = 3
WAKE_WORDS = ["ada", "hey ada", "eda", "aida", "hada", "haina", "aada", "aaddaa", "adda" "ada baby", "hello aada", "hello ada", "dah", "either", "nada", "hada"]

def check_for_wakeword():
    audio_data = sd.rec(
        int(CHUNK_DURATION * SAMPLE_RATE),
        samplerate=SAMPLE_RATE,
        channels=1,
        dtype='int16'
    )
    sd.wait()

    tmp = tempfile.mktemp(suffix=".wav")
    with wave.open(tmp, 'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(SAMPLE_RATE)
        wf.writeframes(audio_data.tobytes())

    try:
        segments, _ = model.transcribe(
            tmp,
            language="en",
            beam_size=1,
            vad_filter=True,
            no_speech_threshold=0.5
        )
        text = " ".join([s.text for s in segments]).strip().lower()
        os.remove(tmp)

        if text:
            print(f"Heard: {text}")
            for wake_word in WAKE_WORDS:
                if wake_word in text:
                    return True
        return False
    except:
        try:
            os.remove(tmp)
        except:
            pass
        return False

def listen_for_wakeword():
    while True:
        if check_for_wakeword():
            return True

if __name__ == "__main__":
    print("Listening for 'Ada'...")
    if listen_for_wakeword():
        print("Wake word detected!")
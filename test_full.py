import sounddevice as sd
import numpy as np
import wave
import tempfile
import os
os.add_dll_directory(r"C:\FRIDAY\venv\Lib\site-packages\nvidia\cublas\bin")
os.add_dll_directory(r"C:\FRIDAY\venv\Lib\site-packages\nvidia\cudnn\bin")
os.add_dll_directory(r"C:\FRIDAY\venv\Lib\site-packages\ctranslate2")
from faster_whisper import WhisperModel

print("Loading model on CUDA...")
model = WhisperModel("medium", device="cuda", compute_type="float16")
print("Model loaded!")

print("\nRecording 5 seconds... SAY SOMETHING!")
audio = sd.rec(int(5 * 16000), samplerate=16000, channels=1, dtype='int16')
sd.wait()
print("Recording done!")

rms = np.sqrt(np.mean(audio.astype(np.float32) ** 2))
print(f"RMS level: {rms:.1f} (should be 20+ if you spoke)")

tmp = tempfile.mktemp(suffix=".wav")
with wave.open(tmp, 'wb') as wf:
    wf.setnchannels(1)
    wf.setsampwidth(2)
    wf.setframerate(16000)
    wf.writeframes(audio.tobytes())

print("Transcribing...")
segments, _ = model.transcribe(tmp, language="en", temperature=0.0)
text = " ".join([s.text for s in segments]).strip()
os.remove(tmp)

print(f"You said: {text}")
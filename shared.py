import os
os.add_dll_directory(r"C:\FRIDAY\venv\Lib\site-packages\nvidia\cublas\bin")
os.add_dll_directory(r"C:\FRIDAY\venv\Lib\site-packages\nvidia\cudnn\bin")

import threading
import queue
import numpy as np
import sounddevice as sd
from faster_whisper import WhisperModel

# ── Whisper model (loaded once, shared by listen and wakeword) ─────────────
print("Loading Whisper model...")
whisper_model = WhisperModel("medium", device="cuda", compute_type="float16")
print("Whisper ready!")

# ── Audio stream settings ──────────────────────────────────────────────────
SAMPLE_RATE   = 16000
CHUNK_SAMPLES = 512  # small chunks for low latency

# ── Shared audio queue ─────────────────────────────────────────────────────
# The single mic stream pushes chunks here continuously.
# wakeword and listen both read from this same queue.
_audio_queue = queue.Queue()

# ── Mode flag ──────────────────────────────────────────────────────────────
# "wake"   = wakeword is reading the queue
# "listen" = listen.py is reading the queue
_mode = "wake"
_mode_lock = threading.Lock()

def get_mode():
    with _mode_lock:
        return _mode

def set_mode(mode):
    with _mode_lock:
        global _mode
        _mode = mode

def _audio_callback(indata, frames, time_info, status):
    """Called by sounddevice for every chunk — just push to queue."""
    _audio_queue.put(indata.copy())

def start_audio_stream():
    """Start the single continuous mic stream."""
    stream = sd.InputStream(
        samplerate=SAMPLE_RATE,
        channels=1,
        dtype='int16',
        blocksize=CHUNK_SAMPLES,
        callback=_audio_callback
    )
    stream.start()
    print("[Audio] Mic stream started!")
    return stream

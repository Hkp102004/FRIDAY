import sounddevice as sd
import numpy as np
import wave
import tempfile
import os
import threading
import queue
from faster_whisper import WhisperModel

# ── Shared model (tiny = fast enough for wake word detection) ──────────────
print("Loading wake word model...")
model = WhisperModel("tiny", device="cuda", compute_type="int8")
print("Wake word ready! Say 'FRIDAY' to wake her up!")

SAMPLE_RATE = 16000
CHUNK_DURATION = 2  # shorter chunks = less deaf gap

WAKE_WORDS = [
    "Friday","friday","hey there","hey friday","wake up friday", "ok friday",
    "hello there","friday wake up","friday wakeup", "time for work","time for work friday",
    "alright daddy's home", "let's get to work friday"
]

# ── Audio chunk queue ──────────────────────────────────────────────────────
_audio_queue = queue.Queue()


def _recording_thread():
    """Continuously records chunks and pushes them to the queue."""
    while True:
        audio = sd.rec(
            int(CHUNK_DURATION * SAMPLE_RATE),
            samplerate=SAMPLE_RATE,
            channels=1,
            dtype='int16'
        )
        sd.wait()
        _audio_queue.put(audio.copy())


def _transcribe_chunk(audio_data):
    """Save chunk to temp wav and transcribe it."""
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
        return text
    except Exception:
        return ""
    finally:
        try:
            os.remove(tmp)
        except Exception:
            pass


def listen_for_wakeword():
    """
    Starts a background recording thread so Ada is never deaf.
    The main thread processes chunks from the queue as fast as possible.
    Returns True as soon as the wake word is detected.
    """
    # Start the recorder in a daemon thread (dies when main program exits)
    t = threading.Thread(target=_recording_thread, daemon=True)
    t.start()

    while True:
        audio = _audio_queue.get()  # blocks until a chunk is ready
        text = _transcribe_chunk(audio)

        if text:
            print(f"[Wake] Heard: {text}")
            for wake_word in WAKE_WORDS:
                if wake_word in text:
                    print("[Wake] Wake word detected!")
                    return True


if __name__ == "__main__":
    print("Listening for 'FRIDAY'...")
    if listen_for_wakeword():
        print("Wake word detected!")
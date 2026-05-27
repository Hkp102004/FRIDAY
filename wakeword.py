import numpy as np
import wave
import tempfile
import os

from shared import (
    whisper_model, _audio_queue, SAMPLE_RATE,
    get_mode, set_mode
)

print("Wake word ready! Say 'FRIDAY' to wake her up!")

WAKE_CHUNK_S  = 2       # collect 2 seconds of audio then check for wake word
SILENCE_THRESH = 10     # skip transcription if too quiet

WAKE_WORDS = [
    "friday", "hey friday", "ok friday",
    "hello friday", "wake up friday", "friday wake up",
]


def _collect_audio(seconds):
    """Collect N seconds worth of audio chunks from the shared queue."""
    target_samples = int(SAMPLE_RATE * seconds)
    collected = []
    total = 0

    while total < target_samples:
        chunk = _audio_queue.get()
        chunk_np = np.frombuffer(chunk, dtype=np.int16).flatten()
        collected.append(chunk_np)
        total += len(chunk_np)

    return np.concatenate(collected)


def _transcribe(audio_data):
    """Transcribe audio, skip if too quiet."""
    rms = np.sqrt(np.mean(audio_data.astype(np.float32) ** 2))
    if rms < SILENCE_THRESH:
        return ""

    tmp = tempfile.mktemp(suffix=".wav")
    with wave.open(tmp, 'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(SAMPLE_RATE)
        wf.writeframes(audio_data.tobytes())
    try:
        segments, _ = whisper_model.transcribe(
            tmp,
            language="en",
            beam_size=1,
            vad_filter=True,
            no_speech_threshold=0.5,
            temperature=0.0,
        )
        return " ".join([s.text for s in segments]).strip().lower()
    except Exception:
        return ""
    finally:
        try:
            os.remove(tmp)
        except:
            pass


def listen_for_wakeword():
    """
    Reads from shared audio queue in 2s chunks.
    Returns True when wake word detected.
    """
    set_mode("wake")

    while True:
        # Only process if we're in wake mode
        if get_mode() != "wake":
            import time
            time.sleep(0.1)
            continue

        audio = _collect_audio(WAKE_CHUNK_S)
        text = _transcribe(audio)

        if text:
            print(f"[Wake] Heard: {text}")
            for wake_word in WAKE_WORDS:
                if wake_word in text:
                    print("[Wake] Wake word detected!")
                    return True


if __name__ == "__main__":
    from shared import start_audio_stream
    stream = start_audio_stream()
    print("Listening for 'FRIDAY'...")
    if listen_for_wakeword():
        print("Wake word detected!")
    stream.stop()

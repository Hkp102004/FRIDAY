import sounddevice as sd
import numpy as np
import wave
import tempfile
import os

# ── Shared Whisper model ───────────────────────────────────────────────────
# Imported here so wakeword.py can also import from this module if needed.
# Only one model is ever loaded into RAM.
from faster_whisper import WhisperModel

print("Loading Whisper model...")
whisper_model = WhisperModel("small", device="cpu", compute_type="int8")
print("Whisper ready!")

# ── VAD recording settings ─────────────────────────────────────────────────
SAMPLE_RATE      = 16000
CHUNK_MS         = 30           # analyse silence in 30ms chunks
SILENCE_LIMIT_S  = 1.2          # stop after this many seconds of silence
MAX_DURATION_S   = 10           # hard cap so it never hangs
SILENCE_THRESH   = 300          # RMS below this = silence


def _is_silent(chunk: np.ndarray) -> bool:
    return int(np.sqrt(np.mean(chunk.astype(np.float32) ** 2))) < SILENCE_THRESH


def _record_until_silence() -> np.ndarray:
    """
    Records audio in 30ms chunks.
    Stops recording once the user has been silent for SILENCE_LIMIT_S seconds,
    or after MAX_DURATION_S seconds as a hard cap.
    Returns the full audio as a numpy array.
    """
    chunk_samples   = int(SAMPLE_RATE * CHUNK_MS / 1000)
    max_chunks      = int(MAX_DURATION_S * 1000 / CHUNK_MS)
    silence_chunks  = int(SILENCE_LIMIT_S * 1000 / CHUNK_MS)

    frames = []
    silent_count = 0
    started_speaking = False

    with sd.InputStream(samplerate=SAMPLE_RATE, channels=1, dtype='int16') as stream:
        for _ in range(max_chunks):
            chunk, _ = stream.read(chunk_samples)
            chunk_np = np.frombuffer(chunk, dtype=np.int16)
            frames.append(chunk_np)

            if _is_silent(chunk_np):
                if started_speaking:
                    silent_count += 1
                    if silent_count >= silence_chunks:
                        break   # user stopped speaking
            else:
                started_speaking = True
                silent_count = 0

    return np.concatenate(frames)


def listen():
    print("ADA: Listening...")

    audio_data = _record_until_silence()

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
            beam_size=5,
            vad_filter=True,
            vad_parameters=dict(min_silence_duration_ms=500),
            initial_prompt="Commands for AI assistant Ada. User says things like: open spotify, play music, set volume, search for, what is the weather.",
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
        try:
            os.remove(tmp)
        except Exception:
            pass
        return None


if __name__ == "__main__":
    print("Say something!")
    result = listen()
    if result:
        print(f"You said: {result}")
    else:
        print("Couldn't hear anything!")
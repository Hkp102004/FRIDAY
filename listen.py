import numpy as np
import wave
import tempfile
import os

from shared import (
    whisper_model, _audio_queue, SAMPLE_RATE,
    get_mode, set_mode
)

SILENCE_THRESH  = 10
SILENCE_LIMIT_S = 1.2
MAX_DURATION_S  = 10
CHUNK_MS        = 30


def _is_silent(chunk):
    return int(np.sqrt(np.mean(chunk.astype(np.float32) ** 2))) < SILENCE_THRESH


def _record_until_silence():
    """
    Reads from shared audio queue until silence detected.
    Returns full audio as numpy array.
    """
    chunk_samples  = int(SAMPLE_RATE * CHUNK_MS / 1000)
    max_chunks     = int(MAX_DURATION_S * 1000 / CHUNK_MS)
    silence_chunks = int(SILENCE_LIMIT_S * 1000 / CHUNK_MS)

    frames        = []
    silent_count  = 0
    started       = False

    for _ in range(max_chunks):
        # Collect enough samples for one chunk
        collected = []
        total = 0
        while total < chunk_samples:
            raw = _audio_queue.get()
            chunk_np = np.frombuffer(raw, dtype=np.int16).flatten()
            collected.append(chunk_np)
            total += len(chunk_np)

        chunk = np.concatenate(collected)[:chunk_samples]
        frames.append(chunk)

        if _is_silent(chunk):
            if started:
                silent_count += 1
                if silent_count >= silence_chunks:
                    break
        else:
            started = True
            silent_count = 0

    return np.concatenate(frames)


def listen():
    print("FRIDAY: Listening...")

    # Switch to listen mode — wakeword stops processing queue
    set_mode("listen")

    # Flush stale audio chunks from queue
    while not _audio_queue.empty():
        try:
            _audio_queue.get_nowait()
        except:
            break

    audio_data = _record_until_silence()

    # Switch back to wake mode
    set_mode("wake")

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
            condition_on_previous_text=False,
            no_speech_threshold=0.45,
            log_prob_threshold=-0.5,
            temperature=0.0,
        )
        text = " ".join([s.text for s in segments]).strip()
        os.remove(tmp)

        if text:
            print(f"You: {text}")
            return text.lower()
        return None

    except Exception as e:
        print(f"[Listen] Error: {e}")
        try:
            os.remove(tmp)
        except:
            pass
        return None


if __name__ == "__main__":
    from shared import start_audio_stream
    stream = start_audio_stream()
    print("Say something!")
    result = listen()
    if result:
        print(f"You said: {result}")
    else:
        print("Couldn't hear anything!")
    stream.stop()

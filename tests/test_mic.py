import sounddevice as sd
import numpy as np

SAMPLE_RATE = 16000

print("Testing mic levels... speak normally!")
print("Watch the RMS values!\n")

while True:
    chunk = sd.rec(
        int(0.5 * SAMPLE_RATE),
        samplerate=SAMPLE_RATE,
        channels=1,
        dtype='int16'
    )
    sd.wait()
    rms = np.sqrt(np.mean(chunk.astype(np.float32) ** 2))
    print(f"RMS: {rms:.1f}")
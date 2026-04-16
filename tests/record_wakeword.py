import sounddevice as sd
import numpy as np
import wave
import os
import time

SAMPLE_RATE = 16000
DURATION = 2  # seconds per recording
OUTPUT_DIR = "wakeword_samples/ada"

os.makedirs(OUTPUT_DIR, exist_ok=True)

def record_sample(filename):
    print("Recording in 3...")
    time.sleep(0.7)
    print("2...")
    time.sleep(0.7)
    print("1...")
    time.sleep(0.7)
    print("🎤 Say 'Ada' NOW!")
    
    audio = sd.rec(
        int(DURATION * SAMPLE_RATE),
        samplerate=SAMPLE_RATE,
        channels=1,
        dtype='int16'
    )
    sd.wait()
    print("✅ Recorded!")
    
    with wave.open(filename, 'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(SAMPLE_RATE)
        wf.writeframes(audio.tobytes())

def main():
    existing = len([f for f in os.listdir(OUTPUT_DIR) if f.endswith('.wav')])
    print(f"\n🎯 Wake Word Recorder — 'Ada'")
    print(f"Already recorded: {existing} samples")
    print(f"Target: 100 samples")
    print(f"\nTips for best results:")
    print("- Say 'Ada' clearly and naturally")
    print("- Vary your tone slightly each time")
    print("- Say it from different distances")
    print("- Some loud, some soft")
    print("\nPress Enter to start each recording, 'q' to quit\n")
    
    count = existing
    while count < 100:
        inp = input(f"Sample {count+1}/100 — Press Enter to record (or 'q' to quit): ")
        if inp.lower() == 'q':
            break
        filename = os.path.join(OUTPUT_DIR, f"ada_{count+1:03d}.wav")
        record_sample(filename)
        count += 1
        print(f"Progress: {count}/100\n")
    
    print(f"\n✅ Done! Recorded {count} samples!")
    print("Now run: python train_wakeword.py")

if __name__ == "__main__":
    main()
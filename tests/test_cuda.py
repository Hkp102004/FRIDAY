from faster_whisper import WhisperModel

print("Loading tiny model on CUDA...")
try:
    model = WhisperModel("tiny", device="cuda", compute_type="float16")
    print("✅ CUDA Whisper works!")
except Exception as e:
    print(f"❌ CUDA failed: {e}")
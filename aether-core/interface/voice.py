# Dummy voice interface for server use (no TTS, no speech recognition)

def speak(text):
    print(f"[TTS DISABLED] {text}")

def listen():
    print("[TTS DISABLED] Voice input not available on server.")
    return "" 
# interface/voice.py
import os

if os.environ.get("ENABLE_TTS") == "1":
    import pyttsx3
    import speech_recognition as sr
    engine = pyttsx3.init()
    engine.setProperty("rate", 160)

    def speak(text):
        print(f"🤖 Speaking: {text}")
        engine.say(text)
        engine.runAndWait()

    def listen():
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            print("🎤 Listening...")
            try:
                audio = recognizer.listen(source, timeout=5)
                text = recognizer.recognize_google(audio)
                print(f"🎤 Heard: {text}")
                return text
            except sr.WaitTimeoutError:
                print("⏰ No speech detected")
                return None
            except sr.UnknownValueError:
                print("❓ Could not understand audio")
                return None
            except Exception as e:
                print(f"❌ Error: {e}")
                return None
else:
    def speak(text):
        print(f"[TTS DISABLED] {text}")
    def listen():
        print("[TTS DISABLED] Voice input not available on server.")
        return "" 
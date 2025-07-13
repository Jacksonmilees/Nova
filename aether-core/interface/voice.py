# interface/voice.py
import pyttsx3
import speech_recognition as sr

# Initialize voice engine
engine = pyttsx3.init()
engine.setProperty("rate", 160)

def speak(text):
    print(f"🔊 Speaking: {text}")
    engine.say(text)
    engine.runAndWait()

def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎙️ Listening...")
        audio = r.listen(source)
        try:
            command = r.recognize_google(audio)
            print(f"🗣️ You said: {command}")
            return command
        except sr.UnknownValueError:
            return "I didn't understand that."
        except sr.RequestError:
            return "Speech recognition failed." 
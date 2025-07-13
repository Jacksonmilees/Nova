import speech_recognition as sr
import pyttsx3
import time
from core.thinker import think

class VoiceBot:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.engine = pyttsx3.init()
        
    def listen(self):
        """Listen for voice input and convert to text"""
        with sr.Microphone() as source:
            print("🎤 Listening...")
            try:
                audio = self.recognizer.listen(source, timeout=5)
                text = self.recognizer.recognize_google(audio)
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
    
    def speak(self, text):
        """Convert text to speech"""
        print(f"🤖 Speaking: {text}")
        self.engine.say(text)
        self.engine.runAndWait()
    
    def run_voice_loop(self):
        print("🎤 Voice Bot is online. Say 'exit' to quit.")
        while True:
            user_input = self.listen()
            if user_input:
                if user_input.lower() == 'exit':
                    self.speak("Goodbye!")
                    break
                
                # Get response from NOVA
                reply = think(user_input)
                self.speak(reply)

if __name__ == "__main__":
    bot = VoiceBot()
    bot.run_voice_loop() 
import threading
import time
from core.thinker import think
from telegram_bot import run_telegram_loop
from voice_bot import VoiceBot

def run_terminal_mode():
    """Run NOVA in terminal mode"""
    print("\n🔵 NOVA ONLINE (Terminal Mode) | Type 'exit' to shut down.")
    while True:
        try:
            prompt = input("🧠 You: ").strip()
            if prompt.lower() in ["exit", "quit"]:
                print("⚪ Shutting down NOVA.")
                break
            elif prompt:
                reply = think(prompt)
                print(f"🤖 NOVA: {reply}\n")
        except Exception as e:
            print(f"⚠️ Error: {e}")

def run_telegram_mode():
    """Run NOVA in Telegram mode"""
    print("📱 Starting Telegram Bot...")
    run_telegram_loop()

def run_voice_mode():
    """Run NOVA in voice mode"""
    print("🎤 Starting Voice Bot...")
    bot = VoiceBot()
    bot.run_voice_loop()

def run_multi_mode():
    """Run NOVA in multiple modes simultaneously"""
    print("🚀 NOVA Multi-Mode Interface")
    print("1. Terminal Mode")
    print("2. Telegram Mode") 
    print("3. Voice Mode")
    print("4. All Modes")
    
    choice = input("Select mode (1-4): ").strip()
    
    if choice == "1":
        run_terminal_mode()
    elif choice == "2":
        run_telegram_mode()
    elif choice == "3":
        run_voice_mode()
    elif choice == "4":
        # Run all modes in separate threads
        print("🔄 Starting all modes...")
        
        # Start Telegram bot in background
        telegram_thread = threading.Thread(target=run_telegram_mode, daemon=True)
        telegram_thread.start()
        
        # Start Voice bot in background  
        voice_thread = threading.Thread(target=run_voice_mode, daemon=True)
        voice_thread.start()
        
        # Run terminal mode in main thread
        run_terminal_mode()
    else:
        print("❌ Invalid choice")

if __name__ == "__main__":
    run_multi_mode() 
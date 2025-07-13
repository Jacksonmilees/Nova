#!/usr/bin/env python3
"""
NOVA GUI Launcher
Launches the NOVA AI interface with GUI
"""

import sys
import os
from pathlib import Path

# Add the current directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

def main():
    try:
        import tkinter as tk
        from interface.ui import NovaUI
        
        print("🔵 Launching NOVA GUI Interface...")
        print("📱 Features:")
        print("  - 🎤 Voice input")
        print("  - 💬 Text chat")
        print("  - 🔧 Quick commands")
        print("  - 📝 Live logs")
        print("  - 🔊 Voice responses")
        
        root = tk.Tk()
        app = NovaUI(root)
        
        # Center the window
        root.update_idletasks()
        x = (root.winfo_screenwidth() // 2) - (800 // 2)
        y = (root.winfo_screenheight() // 2) - (600 // 2)
        root.geometry(f"800x600+{x}+{y}")
        
        print("✅ GUI launched successfully!")
        print("💡 Tips:")
        print("  - Type messages and press Enter")
        print("  - Click 🎤 for voice input")
        print("  - Use quick command buttons")
        print("  - Type 'help' for commands")
        
        root.mainloop()
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Make sure all dependencies are installed:")
        print("pip install pyttsx3 SpeechRecognition pyaudio")
    except Exception as e:
        print(f"❌ Error launching GUI: {e}")
        print("Check that all modules are in place.")

if __name__ == "__main__":
    main() 
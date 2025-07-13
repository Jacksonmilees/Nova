#!/usr/bin/env python3
"""
NOVA GUI Launcher
Simple script to launch the NOVA GUI interface
"""

import sys
import os
from pathlib import Path

# Add the current directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

try:
    from interface.ui import main
    print("🔵 Launching NOVA GUI...")
    main()
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Make sure all dependencies are installed:")
    print("pip install pyttsx3 SpeechRecognition pyaudio")
except Exception as e:
    print(f"❌ Error launching GUI: {e}")
    print("Check that all modules are in place.") 
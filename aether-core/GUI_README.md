# NOVA AI - GUI Interface

## 🎯 Overview

NOVA now has a modern GUI interface built with Tkinter that provides:

- 🎤 **Voice Input**: Click the voice button to speak to NOVA
- 💬 **Text Chat**: Type messages and press Enter
- 🔧 **Quick Commands**: One-click access to common functions
- 📝 **Live Logs**: Real-time conversation history
- 🔊 **Voice Responses**: NOVA speaks back to you
- 🎨 **Modern UI**: Dark theme with colorful accents

## 🚀 Quick Start

### Method 1: Direct GUI Launch
```bash
python gui_launcher.py
```

### Method 2: Main Menu
```bash
python main.py
# Then choose option 2 for GUI mode
```

### Method 3: Command Line
```bash
python main.py --gui
```

## 🎮 Interface Features

### Main Window
- **Chat Area**: Shows conversation history with timestamps
- **Input Field**: Type your messages here
- **Voice Button**: Click to speak to NOVA
- **Send Button**: Send text messages
- **Clear Button**: Clear chat history
- **Help Button**: Show available commands

### Quick Commands
- 🔧 **Explorer**: Open File Explorer
- 🌐 **Chrome**: Open web browser
- 📝 **Code**: Open VS Code
- 📸 **Screenshot**: Take a screenshot
- 📋 **Tasks**: List your tasks
- ❓ **Help**: Show help information

### Status Bar
Shows current status:
- 🟢 Ready
- 🎙️ Listening
- 🔄 Thinking
- 🔴 Error

## 🎤 Voice Commands

1. Click the **🎤 Voice Input** button
2. Speak your message clearly
3. NOVA will process and respond
4. Both text and voice responses

## 💬 Text Commands

Type any of these commands:

### System Control
- `explorer` - Open File Explorer
- `chrome` - Open web browser  
- `code` - Open VS Code
- `screenshot` - Take screenshot
- `shutdown [minutes]` - Shutdown computer
- `cancel shutdown` - Cancel shutdown

### Task Management
- `add task: description` - Add new task
- `list tasks` - Show all tasks
- `complete task: name` - Mark task done

### File Operations
- `list files [directory]` - List files
- `create folder [name]` - Create folder
- `delete [file]` - Delete file/folder

### AI Features
- `help` - Show all commands
- Ask questions naturally
- Research topics
- Create skills

## 🎨 UI Features

### Color Scheme
- **Background**: Dark blue-gray (#1e1e2f)
- **Chat Area**: Dark gray (#2d2d3f)
- **User Messages**: Blue (#88aaff)
- **NOVA Responses**: Green (#88ff88)
- **System Messages**: Orange (#ffaa44)

### Responsive Design
- Window resizable
- Scrollable chat area
- Auto-scroll to latest messages
- Thread-safe updates

## 🔧 Troubleshooting

### Common Issues

**GUI won't launch:**
```bash
pip install tkinter  # Usually included with Python
```

**Voice not working:**
```bash
pip install pyttsx3 SpeechRecognition pyaudio
```

**Import errors:**
- Make sure you're in the `aether-core` directory
- Check all dependencies are installed

**API rate limits:**
- NOVA will show fallback commands
- System commands still work
- Try again later

### Error Messages

- `⚠️ API rate limit reached` - Wait and try again
- `❌ Voice error` - Check microphone permissions
- `🔴 Error` - Check console for details

## 🎯 Tips

1. **Voice Input**: Speak clearly and wait for the listening indicator
2. **Quick Commands**: Use the buttons for common tasks
3. **Natural Language**: Ask questions naturally
4. **Commands**: Use specific commands for system control
5. **Help**: Type `help` anytime for command list

## 🔄 Integration

The GUI integrates with all existing NOVA features:

- ✅ Voice interface
- ✅ System control
- ✅ Task management
- ✅ File operations
- ✅ AI conversations
- ✅ Skill system
- ✅ Memory system

## 🚀 Next Steps

After mastering the GUI, explore:

1. **Telegram Bot**: Remote access via Telegram
2. **Research Agent**: Web research capabilities
3. **Skill Creation**: Build custom skills
4. **System Automation**: Advanced system control

---

**🎉 Enjoy your NOVA AI experience!** 
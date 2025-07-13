# NOVA Cursor-like Capabilities Guide

## 🤖 NOVA - Your AI-Powered File Manager & App Developer

NOVA now has advanced file operations and AI-powered development capabilities, making it like Cursor but even more powerful!

## 📁 File Operations

### Read Any File
```
read file: path/to/file.txt
read file: main.py
read file: ../config/settings.json
```

### Write Files
```
write file: new_file.txt | This is the content of the file
write file: scripts/backup.py | import os\nprint("Backup script")
```

### AI-Powered File Editing
```
edit file: main.py | Add error handling to the main function
edit file: config.json | Update the API key to use the new endpoint
edit file: README.md | Add installation instructions at the top
```

### List Files
```
list files
list files apps/
list files ../shared_memory
```

### Search File Contents
```
search files: NOVA
search files: API_KEY
search files: def main
```

## 🚀 App Development

### Create Complete Applications
```
create app: todo_app | A simple todo list application with add, delete, and mark complete functionality
create app: weather_app | A weather app that fetches current weather data from an API
create app: calculator | A GUI calculator with basic arithmetic operations
create app: file_manager | A file manager with copy, move, delete, and search capabilities
```

## 📝 Task Management

### Add Tasks
```
add task: Review the new code changes
add task: Test the file operations
add task: Deploy the web app
```

### List Tasks
```
list tasks
```

### Complete Tasks
```
complete task: Review the new code changes
```

## 🔧 System Commands

### Execute Commands
```
run: ls -la
run: python script.py
run: git status
run: pip install requests
```

## 💬 General AI Chat

Just ask questions naturally:
```
What is the weather like today?
How do I install Python packages?
Explain the difference between lists and tuples
Write a function to sort a list
```

## 🎯 Example Use Cases

### 1. Code Review & Editing
```
read file: my_script.py
edit file: my_script.py | Add input validation and error handling
```

### 2. Project Setup
```
create app: my_project | A web application with Flask backend and HTML frontend
list files apps/my_project
read file: apps/my_project/main.py
```

### 3. File Management
```
list files
search files: password
write file: backup_config.json | {"backup_enabled": true, "frequency": "daily"}
```

### 4. System Administration
```
run: df -h
run: ps aux | grep python
run: systemctl status nova
```

## 🔄 Integration with Existing Features

NOVA maintains all its existing capabilities:
- **Voice Interface**: Speak commands naturally
- **Telegram Bot**: Use commands via Telegram
- **GUI Interface**: Visual interface with file operations
- **Memory System**: Remembers your file operations and preferences
- **Multi-AI Fallback**: Uses Ollama when Gemini hits rate limits

## 🛠️ Advanced Features

### AI-Powered Code Generation
NOVA can generate complete applications from descriptions, including:
- Main application files
- Dependencies (requirements.txt)
- Documentation (README.md)
- Configuration files
- Tests and utilities

### Intelligent File Editing
- Understands context and intent
- Maintains code structure and formatting
- Handles multiple file types (Python, JavaScript, HTML, etc.)
- Preserves existing functionality while making changes

### Cross-Platform Compatibility
- Works on Windows, macOS, and Linux
- Handles different file encodings
- Supports various file formats

## 🚀 Getting Started

1. **Start NOVA**:
   ```bash
   cd aether-core
   python main.py
   ```

2. **Try File Operations**:
   ```
   read file: main.py
   list files
   ```

3. **Create Your First App**:
   ```
   create app: hello_world | A simple greeting application
   ```

4. **Use Voice Commands**:
   Just speak your commands when prompted!

## 📱 Telegram Bot Usage

Send commands to your NOVA bot:
```
/start - Get started
/help - Show all commands
read file: main.py
create app: my_app | A web application
run: ls -la
```

## 🎨 GUI Interface

Launch the GUI for visual file operations:
```bash
python main.py --gui
```

## 🔧 Troubleshooting

### File Not Found
- Use absolute paths: `read file: /full/path/to/file`
- Check current directory: `list files`

### Permission Errors
- Ensure NOVA has read/write permissions
- Use `run: chmod +rw file.txt` if needed

### AI Rate Limits
- NOVA automatically falls back to Ollama
- Commands still work during rate limits
- Check logs for details

## 🎯 Pro Tips

1. **Be Specific**: Instead of "edit the file", say "edit file: main.py | Add error handling"

2. **Use Descriptive App Names**: "create app: weather_dashboard" vs "create app: app"

3. **Combine Commands**: Create an app, then immediately read and edit its files

4. **Leverage Memory**: NOVA remembers your file operations and preferences

5. **Use Voice**: Speak complex commands naturally

## 🔮 Future Enhancements

- **Git Integration**: Commit, push, and manage repositories
- **Database Operations**: Create and manage databases
- **Web Scraping**: Extract data from websites
- **API Testing**: Test and debug API endpoints
- **Docker Support**: Create and manage containers

---

**NOVA is now your AI-powered development environment!** 🚀

Just describe what you want, and NOVA will make it happen - whether it's reading files, editing code, creating applications, or answering questions. It's like having Cursor's capabilities but with AI that can understand and execute your intentions across your entire system. 
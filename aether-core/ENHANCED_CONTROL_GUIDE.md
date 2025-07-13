# NOVA Enhanced System Control Guide

## 🎯 New Features

### 📸 **Screenshot + Telegram Integration**
- Takes screenshots and automatically sends them to your Telegram
- Timestamped filenames (e.g., `screenshot_20250713_044633.png`)
- Works from Telegram bot, GUI, voice, or console

### ⚡ **Execute Any Command**
- Run any system command on your computer
- Two syntax options:
  - `execute: command`
  - `run command: command`

### 📊 **System Information**
- Get real-time system stats
- CPU usage, memory usage, disk usage
- Command: `system info`

## 🚀 How to Use

### 1. **Screenshot to Telegram**

**Via Telegram Bot:**
```
Send: screenshot
```
Result: Screenshot taken and sent to your Telegram

**Via Console/GUI:**
```
Type: screenshot
```
Result: Screenshot saved locally and sent to Telegram

### 2. **Execute Commands**

**Basic Commands:**
```
execute: dir
execute: ipconfig
execute: tasklist
execute: echo Hello World
```

**Alternative Syntax:**
```
run command: dir
run command: ipconfig
run command: tasklist
run command: echo Hello World
```

**Advanced Commands:**
```
execute: netstat -an
execute: systeminfo
execute: wmic cpu get name
execute: powershell Get-Process
```

### 3. **System Information**

```
system info
```
Shows:
- CPU Usage percentage
- Memory usage (GB used / GB total)
- Disk usage (GB used / GB total)

## 📱 Telegram Integration

### Setup
1. The bot automatically detects your chat ID
2. Screenshots are sent to the same chat where you send commands
3. No additional setup required

### Commands via Telegram
```
screenshot          - Take screenshot and send to Telegram
system info        - Get system information
execute: dir       - Run directory listing
run command: ipconfig  - Run IP configuration
```

## 🔧 Technical Details

### Screenshot Process
1. Takes screenshot using `pyautogui`
2. Saves with timestamp: `screenshot_YYYYMMDD_HHMMSS.png`
3. Sends to Telegram via bot API
4. Returns success/failure message

### Command Execution
1. Uses `subprocess.check_output()` for safe execution
2. Captures both stdout and stderr
3. Returns formatted output
4. Handles errors gracefully

### System Information
1. Uses `psutil` library for system stats
2. Real-time CPU, memory, and disk usage
3. Formatted output with emojis

## 🛡️ Security Features

### Command Execution Safety
- All commands run in subprocess
- Output is captured and returned
- Errors are handled gracefully
- No direct shell access

### Telegram Integration
- Uses your existing bot token
- Chat ID is set automatically
- Files sent only to your chat
- No data shared with third parties

## 📋 Example Commands

### System Information
```
system info
```

### File Operations
```
execute: dir
execute: dir C:\Users
execute: type filename.txt
execute: copy file1.txt file2.txt
```

### Network Commands
```
execute: ipconfig
execute: ping google.com
execute: netstat -an
execute: tracert google.com
```

### Process Management
```
execute: tasklist
execute: taskkill /IM notepad.exe
execute: powershell Get-Process
```

### System Commands
```
execute: systeminfo
execute: wmic cpu get name
execute: wmic memorychip get capacity
execute: wmic diskdrive get size
```

## 🎮 Usage Examples

### Via Telegram Bot
1. Start bot: `python telegram_bot.py`
2. Send commands to your bot:
   ```
   screenshot
   system info
   execute: dir
   run command: ipconfig
   ```

### Via GUI
1. Launch GUI: `python gui_launcher.py`
2. Use quick command buttons or type:
   ```
   screenshot
   system info
   execute: dir
   ```

### Via Console
1. Run console: `python main.py`
2. Type commands:
   ```
   screenshot
   system info
   execute: dir
   ```

## 🔍 Troubleshooting

### Screenshot Issues
- **pyautogui not installed**: `pip install pyautogui`
- **Permission denied**: Run as administrator
- **Telegram error**: Check bot token and chat ID

### Command Execution Issues
- **Command not found**: Use full path or check PATH
- **Permission denied**: Run as administrator
- **Output too long**: Commands are truncated for readability

### System Info Issues
- **psutil not installed**: `pip install psutil`
- **Permission error**: Run as administrator

## 🎯 Advanced Usage

### Batch Commands
```
execute: for %i in (1,2,3) do echo %i
execute: dir /s /b *.txt
execute: findstr "error" *.log
```

### PowerShell Commands
```
execute: powershell Get-Service
execute: powershell Get-EventLog -LogName System -Newest 10
execute: powershell Get-WmiObject -Class Win32_ComputerSystem
```

### Network Diagnostics
```
execute: nslookup google.com
execute: arp -a
execute: route print
execute: netstat -r
```

## 🎉 Benefits

1. **Remote Control**: Control your computer from anywhere via Telegram
2. **Screenshot Sharing**: Instantly share screenshots with yourself
3. **System Monitoring**: Real-time system information
4. **Command Execution**: Run any command remotely
5. **Multi-Interface**: Works via Telegram, GUI, voice, and console
6. **Safe Execution**: All commands run safely with error handling

## 🔮 Future Enhancements

- File upload/download via Telegram
- Remote file management
- System monitoring alerts
- Scheduled command execution
- Advanced security features

---

**🎯 Your computer is now fully controllable via NOVA!** 
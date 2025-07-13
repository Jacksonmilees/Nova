# 🚀 Manual NOVA Deployment Guide for Contabo VPS

## 📋 **Prerequisites**
- SSH access to your VPS (164.68.118.21)
- Root password: `3r14F65gMv`
- SSH client (PuTTY, Windows Terminal, or similar)

## 🔧 **Step-by-Step Deployment**

### **Step 1: Connect to Your VPS**
```bash
ssh root@164.68.118.21
# Password: 3r14F65gMv
```

### **Step 2: Update System and Install Dependencies**
```bash
# Update system
apt update && apt upgrade -y

# Install Python and required packages
apt install python3 python3-pip python3-venv git screen curl wget -y

# Install system dependencies
apt install ffmpeg portaudio19-dev python3-dev -y
```

### **Step 3: Create NOVA Directory**
```bash
# Create dedicated folder for NOVA
mkdir -p /opt/nova
cd /opt/nova
```

### **Step 4: Upload NOVA Files**
From your local computer, upload the files:

**Option A: Using SCP (from your local machine)**
```bash
# From your local Aether directory
scp -r aether-core/* root@164.68.118.21:/opt/nova/
```

**Option B: Using File Transfer**
1. Use WinSCP or similar tool
2. Connect to: `164.68.118.21`
3. Username: `root`
4. Password: `3r14F65gMv`
5. Upload all files from `aether-core/` to `/opt/nova/`

### **Step 5: Setup Python Environment**
```bash
cd /opt/nova

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install requirements
pip install --upgrade pip
pip install google-generativeai requests pillow pyttsx3 SpeechRecognition psutil
```

### **Step 6: Configure NOVA**
```bash
# Create config directory if it doesn't exist
mkdir -p config

# Create settings.json with your API key
cat > config/settings.json << 'EOF'
{
    "GEMINI_API_KEY": "your-api-key-here",
    "MODEL": "gemini-1.5-flash",
    "TELEGRAM_BOT_TOKEN": "8002118162:AAGfvEmGBXns_PfsdAq5OREJS7_73M1yfzE"
}
EOF
```

### **Step 7: Create Systemd Service**
```bash
# Create service file
cat > /etc/systemd/system/nova.service << 'EOF'
[Unit]
Description=NOVA AI System
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/opt/nova
Environment=PATH=/opt/nova/venv/bin
ExecStart=/opt/nova/venv/bin/python telegram_bot_enhanced.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# Enable and start service
systemctl daemon-reload
systemctl enable nova
systemctl start nova
```

### **Step 8: Test the Deployment**
```bash
# Check if service is running
systemctl status nova

# View logs
journalctl -u nova -f

# Test the bot manually
cd /opt/nova
source venv/bin/activate
python telegram_bot_enhanced.py
```

## 🎯 **Verification Steps**

### **Check Service Status**
```bash
systemctl status nova
```

### **View Logs**
```bash
journalctl -u nova -f
```

### **Test Telegram Bot**
1. Open Telegram
2. Send message to your bot
3. Try commands like:
   - `run: ls`
   - `system info`
   - `help`

## 🔧 **Management Commands**

### **Service Management**
```bash
# Check status
systemctl status nova

# View logs
journalctl -u nova -f

# Restart service
systemctl restart nova

# Stop service
systemctl stop nova

# Start service
systemctl start nova

# Enable auto-start
systemctl enable nova

# Disable auto-start
systemctl disable nova
```

### **Manual Testing**
```bash
cd /opt/nova
source venv/bin/activate
python telegram_bot_enhanced.py
```

## 📁 **File Structure on VPS**
```
/opt/nova/
├── main.py
├── telegram_bot_enhanced.py
├── requirements.txt
├── vault.py
├── venv/
├── core/
│   └── thinker.py
├── actions/
│   └── system_control.py
├── interface/
│   └── voice.py
└── config/
    └── settings.json
```

## 🛠️ **Troubleshooting**

### **If Service Won't Start**
```bash
# Check logs
journalctl -u nova -f

# Check file permissions
ls -la /opt/nova/

# Test manually
cd /opt/nova
source venv/bin/activate
python telegram_bot_enhanced.py
```

### **If Files Are Missing**
```bash
# Check what's in the directory
ls -la /opt/nova/

# Re-upload files if needed
# Use SCP or file transfer tool
```

### **If Python Dependencies Fail**
```bash
cd /opt/nova
source venv/bin/activate
pip install --upgrade pip
pip install google-generativeai requests pillow pyttsx3 SpeechRecognition psutil
```

## 🎉 **Success Indicators**

✅ **Service is running**: `systemctl status nova` shows "active (running)"  
✅ **Bot responds**: Telegram bot replies to messages  
✅ **Commands work**: `run: ls` returns directory listing  
✅ **Screenshots work**: `screenshot` command takes and sends screenshots  

## 🔒 **Security Notes**

1. **Change default password** after deployment
2. **Use SSH keys** instead of password authentication
3. **Configure firewall** to restrict access
4. **Keep system updated** regularly
5. **Monitor logs** for suspicious activity

## 📞 **Support**

If you encounter issues:
1. Check the logs: `journalctl -u nova -f`
2. Test manually: `cd /opt/nova && source venv/bin/activate && python telegram_bot_enhanced.py`
3. Verify file permissions and ownership
4. Check network connectivity and firewall settings

---

**🎯 Your NOVA system will be deployed to `/opt/nova/` and can be managed as a system service!** 
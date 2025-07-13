# NOVA Remote Access Guide

## 🌐 Access NOVA from Anywhere

NOVA is now available as a web API that you can access from any computer, anywhere in the world!

---

## 🚀 Quick Start

### 1. Start NOVA Server (on your main computer)
```bash
cd aether-core
python nova_api_server.py
```

Or use the batch file:
```bash
start_nova_server.bat
```

### 2. Connect from Any Computer
```bash
python nova_client.py --server http://YOUR_IP:5000
```

---

## 📡 API Endpoints

### Chat with NOVA
```bash
curl -X POST http://localhost:5000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "read file: main.py"}'
```

### File Operations
```bash
# Read file
curl -X POST http://localhost:5000/files/read \
  -H "Content-Type: application/json" \
  -d '{"path": "main.py"}'

# Write file
curl -X POST http://localhost:5000/files/write \
  -H "Content-Type: application/json" \
  -d '{"path": "test.txt", "content": "Hello NOVA!"}'

# Edit file with AI
curl -X POST http://localhost:5000/files/edit \
  -H "Content-Type: application/json" \
  -d '{"path": "main.py", "changes": "Add error handling"}'

# List files
curl -X POST http://localhost:5000/files/list \
  -H "Content-Type: application/json" \
  -d '{"directory": "."}'

# Search files
curl -X POST http://localhost:5000/files/search \
  -H "Content-Type: application/json" \
  -d '{"query": "NOVA"}'
```

### App Creation
```bash
curl -X POST http://localhost:5000/apps/create \
  -H "Content-Type: application/json" \
  -d '{"name": "my_app", "description": "A web application with Flask"}'
```

### System Commands
```bash
curl -X POST http://localhost:5000/system/run \
  -H "Content-Type: application/json" \
  -d '{"command": "dir"}'
```

### Task Management
```bash
# Add task
curl -X POST http://localhost:5000/tasks/add \
  -H "Content-Type: application/json" \
  -d '{"task": "Review the new code"}'

# List tasks
curl -X GET http://localhost:5000/tasks/list
```

---

## 💻 Client Usage Examples

### Interactive Mode
```bash
python nova_client.py --server http://localhost:5000
```

Then type commands like:
- `read file: main.py`
- `edit file: config.json | Update API key`
- `create app: todo | A simple todo list app`
- `run: pip install requests`
- `add task: Test the new features`

### Single Commands
```bash
# Read a file
python nova_client.py --file main.py

# List files
python nova_client.py --list .

# Search files
python nova_client.py --search NOVA

# Create app
python nova_client.py --create-app "weather_app" "A weather application with API"

# Run command
python nova_client.py --run "dir"

# Add task
python nova_client.py --add-task "Deploy the new version"

# List tasks
python nova_client.py --list-tasks

# Check status
python nova_client.py --status
```

---

## 🌍 Remote Access Setup

### 1. Make NOVA Accessible from Internet

**Option A: Port Forwarding (Router)**
- Forward port 5000 to your computer
- Use your public IP address

**Option B: Cloud Deployment**
- Deploy to your VPS (164.68.118.21)
- Access via: `http://164.68.118.21:5000`

**Option C: ngrok (Temporary)**
```bash
# Install ngrok
# Then run:
ngrok http 5000
# Use the provided URL
```

### 2. Connect from Any Computer
```bash
# From any computer, anywhere:
python nova_client.py --server http://YOUR_PUBLIC_IP:5000
```

---

## 🔧 Advanced Usage

### Python Script Example
```python
import requests

# Connect to NOVA
nova_url = "http://localhost:5000"

# Read a file
response = requests.post(f"{nova_url}/files/read", 
                       json={"path": "main.py"})
print(response.json()["response"])

# Create an app
response = requests.post(f"{nova_url}/apps/create",
                       json={"name": "my_app", 
                             "description": "A web app"})
print(response.json()["response"])

# Chat with NOVA
response = requests.post(f"{nova_url}/chat",
                       json={"message": "What can you do?"})
print(response.json()["response"])
```

### JavaScript/Node.js Example
```javascript
const axios = require('axios');

const novaUrl = 'http://localhost:5000';

// Read a file
axios.post(`${novaUrl}/files/read`, {path: 'main.py'})
  .then(response => console.log(response.data.response));

// Create an app
axios.post(`${novaUrl}/apps/create`, {
  name: 'my_app',
  description: 'A web application'
})
.then(response => console.log(response.data.response));
```

---

## 🛡️ Security Considerations

### For Local Network
- NOVA server runs on `0.0.0.0:5000` (accessible from network)
- Use firewall rules to restrict access if needed

### For Internet Access
- Use HTTPS (SSL/TLS) for production
- Implement authentication if needed
- Consider using a reverse proxy (nginx)

---

## 📱 Mobile Access

### Using cURL on Mobile
```bash
# Android (Termux)
curl -X POST http://YOUR_IP:5000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "read file: main.py"}'
```

### Using Web Browser
- Open: `http://YOUR_IP:5000/`
- Use browser's developer tools to make API calls

---

## 🚀 Deployment Options

### 1. Local Network
```bash
# Start server
python nova_api_server.py

# Connect from another computer on same network
python nova_client.py --server http://192.168.1.100:5000
```

### 2. VPS/Cloud
```bash
# Deploy to your VPS
scp nova_api_server.py root@164.68.118.21:/opt/nova/
ssh root@164.68.118.21 "cd /opt/nova && python nova_api_server.py"

# Connect from anywhere
python nova_client.py --server http://164.68.118.21:5000
```

### 3. Docker
```dockerfile
FROM python:3.9
WORKDIR /app
COPY . .
RUN pip install flask flask-cors requests
EXPOSE 5000
CMD ["python", "nova_api_server.py"]
```

---

## 🎯 Use Cases

### 1. Remote Development
- Access NOVA from your laptop while traveling
- Create apps and edit files remotely

### 2. Team Collaboration
- Share NOVA access with team members
- Collaborative AI-powered development

### 3. Mobile Development
- Use NOVA from your phone
- Quick file operations and app creation

### 4. CI/CD Integration
- Automate app creation and deployment
- Use NOVA in your build pipeline

---

## 🔍 Troubleshooting

### Connection Issues
```bash
# Check if server is running
curl http://localhost:5000/status

# Check firewall
netstat -an | grep 5000

# Test from another computer
ping YOUR_IP
telnet YOUR_IP 5000
```

### Common Errors
- **Connection refused**: Server not running
- **Timeout**: Firewall blocking port 5000
- **Invalid JSON**: Check request format

---

## 📊 Monitoring

### Check Server Status
```bash
curl http://localhost:5000/status
```

### View Logs
```bash
# Server logs are printed to console
# Check for errors and successful requests
```

---

**Now you can access NOVA from anywhere in the world!** 🌍

Just start the server and connect from any computer, phone, or device with internet access. 
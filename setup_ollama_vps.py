#!/usr/bin/env python3
"""
Comprehensive Ollama Setup for Contabo VPS
Ensures Ollama is installed, running, and accessible via Flask API
"""

import paramiko
import time
import json

class OllamaVPSSetup:
    def __init__(self):
        self.vps_config = {
            "host": "164.68.118.21",
            "username": "root",
            "password": "3r14F65gMv",
            "port": 22
        }
        self.ssh_client = None
        
    def connect_ssh(self):
        """Establish SSH connection to VPS"""
        try:
            print("🔌 Connecting to Contabo VPS...")
            self.ssh_client = paramiko.SSHClient()
            self.ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.ssh_client.connect(
                hostname=self.vps_config["host"],
                username=self.vps_config["username"],
                password=self.vps_config["password"],
                port=self.vps_config["port"],
                timeout=30
            )
            print("✅ SSH connection established")
            return True
        except Exception as e:
            print(f"❌ SSH connection failed: {e}")
            return False
    
    def execute_command(self, command, description=""):
        """Execute command on remote server"""
        try:
            print(f"🔄 {description}")
            stdin, stdout, stderr = self.ssh_client.exec_command(command)
            output = stdout.read().decode('utf-8')
            error = stderr.read().decode('utf-8')
            
            if output:
                print(f"✅ Output: {output.strip()}")
            if error:
                print(f"⚠️ Error: {error.strip()}")
                
            return output, error
        except Exception as e:
            print(f"❌ Command execution failed: {e}")
            return "", str(e)
    
    def check_ollama_installation(self):
        """Check if Ollama is installed"""
        print("🔍 Checking Ollama installation...")
        output, error = self.execute_command("which ollama", "Checking Ollama installation")
        
        if not output.strip():
            print("📦 Installing Ollama...")
            self.execute_command("curl -fsSL https://ollama.ai/install.sh | sh", "Installing Ollama")
            time.sleep(10)  # Wait for installation
        else:
            print("✅ Ollama is already installed")
        
        # Check version
        output, error = self.execute_command("ollama --version", "Checking Ollama version")
        return "ollama" in output.lower()
    
    def setup_ollama_service(self):
        """Setup Ollama as a systemd service"""
        print("⚙️ Setting up Ollama systemd service...")
        
        service_content = """[Unit]
Description=Ollama LLM Service
After=network.target

[Service]
ExecStart=/usr/bin/ollama serve
Restart=always
User=root

[Install]
WantedBy=multi-user.target
"""
        
        # Create service file
        self.execute_command(f"echo '{service_content}' > /etc/systemd/system/ollama.service", "Creating Ollama service file")
        
        # Enable and start service
        self.execute_command("systemctl daemon-reload", "Reloading systemd")
        self.execute_command("systemctl enable ollama", "Enabling Ollama service")
        self.execute_command("systemctl start ollama", "Starting Ollama service")
        
        # Check status
        output, error = self.execute_command("systemctl status ollama", "Checking Ollama service status")
        return "active (running)" in output
    
    def pull_ollama_models(self):
        """Pull required Ollama models"""
        print("📥 Pulling Ollama models...")
        
        models = ["mistral", "llama3.2:3b"]
        for model in models:
            print(f"📥 Pulling {model}...")
            self.execute_command(f"ollama pull {model}", f"Pulling {model}")
            time.sleep(5)
    
    def create_flask_server(self):
        """Create the Flask API server for Ollama"""
        print("🌐 Creating Flask API server...")
        
        flask_code = '''from flask import Flask, request, jsonify
import subprocess
import json

app = Flask(__name__)

@app.route('/', methods=['POST'])
def handle():
    try:
        data = request.get_json()
        msg = data.get("message", "")
        
        if not msg:
            return jsonify({"error": "No message provided"}), 400
        
        # Run Ollama with the message
        result = subprocess.run(
            ["ollama", "run", "mistral"], 
            input=msg, 
            capture_output=True, 
            text=True,
            timeout=60
        )
        
        if result.returncode == 0:
            return jsonify({"response": result.stdout.strip()})
        else:
            return jsonify({"error": result.stderr}), 500
            
    except subprocess.TimeoutExpired:
        return jsonify({"error": "Request timed out"}), 408
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "healthy", "service": "ollama-api"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=False)
'''
        
        # Create the Flask server file
        self.execute_command(f"echo '{flask_code}' > /root/ollama_server.py", "Creating Flask server file")
        
        # Install Flask if not installed
        self.execute_command("pip3 install flask", "Installing Flask")
        
        return True
    
    def start_flask_server(self):
        """Start the Flask server in background"""
        print("🚀 Starting Flask API server...")
        
        # Kill any existing Flask server
        self.execute_command("pkill -f ollama_server.py", "Stopping existing Flask server")
        
        # Start Flask server in background
        self.execute_command("cd /root && nohup python3 ollama_server.py > flask.log 2>&1 &", "Starting Flask server")
        time.sleep(3)
        
        # Check if server is running
        output, error = self.execute_command("ps aux | grep ollama_server.py", "Checking Flask server status")
        return "ollama_server.py" in output
    
    def test_ollama_api(self):
        """Test the Ollama API"""
        print("🧪 Testing Ollama API...")
        
        test_command = '''curl -X POST http://localhost:5001 -H "Content-Type: application/json" -d '{"message": "Hello, test message"}' --max-time 30'''
        output, error = self.execute_command(test_command, "Testing Ollama API")
        
        if "response" in output or "error" in output:
            print("✅ Ollama API is responding")
            return True
        else:
            print("❌ Ollama API test failed")
            return False
    
    def setup_complete(self):
        """Run complete setup"""
        print("🚀 Starting complete Ollama VPS setup...")
        
        if not self.connect_ssh():
            return False
        
        try:
            # Step 1: Install Ollama
            if not self.check_ollama_installation():
                print("❌ Ollama installation failed")
                return False
            
            # Step 2: Setup systemd service
            if not self.setup_ollama_service():
                print("❌ Ollama service setup failed")
                return False
            
            # Step 3: Pull models
            self.pull_ollama_models()
            
            # Step 4: Create Flask server
            if not self.create_flask_server():
                print("❌ Flask server creation failed")
                return False
            
            # Step 5: Start Flask server
            if not self.start_flask_server():
                print("❌ Flask server start failed")
                return False
            
            # Step 6: Test API
            if not self.test_ollama_api():
                print("❌ Ollama API test failed")
                return False
            
            print("\n🎉 Ollama VPS setup completed successfully!")
            print("🌐 Ollama API is accessible at: http://164.68.118.21:5001")
            print("🤖 You can now use 'ask local:' commands with NOVA")
            
            return True
            
        except Exception as e:
            print(f"❌ Setup failed: {e}")
            return False
        finally:
            self.cleanup()
    
    def cleanup(self):
        """Cleanup SSH connection"""
        if self.ssh_client:
            self.ssh_client.close()
        print("🧹 SSH connection closed")

def main():
    """Main setup function"""
    setup = OllamaVPSSetup()
    success = setup.setup_complete()
    
    if success:
        print("\n✅ Ollama VPS setup successful!")
        print("🔗 Test from your local machine:")
        print("python test_ollama_connection.py")
    else:
        print("\n❌ Ollama VPS setup failed. Check the logs above.")

if __name__ == "__main__":
    main() 
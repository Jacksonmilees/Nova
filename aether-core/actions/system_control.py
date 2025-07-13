# actions/system_control.py
import subprocess
import os
import platform
import requests
from pathlib import Path
import time

class SystemController:
    def __init__(self):
        self.system = platform.system()
        self.telegram_token = '8002118162:AAGfvEmGBXns_PfsdAq5OREJS7_73M1yfzE'
        self.telegram_chat_id = None  # Will be set when first message is received
    
    def set_telegram_chat_id(self, chat_id):
        """Set the Telegram chat ID for sending files"""
        self.telegram_chat_id = chat_id
    
    def send_telegram_message(self, message):
        """Send a text message to Telegram"""
        if not self.telegram_chat_id:
            return "❌ No Telegram chat ID set"
        
        try:
            url = f"https://api.telegram.org/bot{self.telegram_token}/sendMessage"
            data = {
                'chat_id': self.telegram_chat_id,
                'text': message
            }
            response = requests.post(url, data=data)
            if response.status_code == 200:
                return "✅ Message sent to Telegram"
            else:
                return f"❌ Failed to send message: {response.text}"
        except Exception as e:
            return f"❌ Telegram error: {str(e)}"
    
    def send_telegram_file(self, file_path, caption=""):
        """Send a file to Telegram"""
        if not self.telegram_chat_id:
            return "❌ No Telegram chat ID set"
        
        try:
            url = f"https://api.telegram.org/bot{self.telegram_token}/sendPhoto"
            with open(file_path, 'rb') as file:
                files = {'photo': file}
                data = {
                    'chat_id': self.telegram_chat_id,
                    'caption': caption
                }
                response = requests.post(url, files=files, data=data)
                if response.status_code == 200:
                    return "✅ File sent to Telegram"
                else:
                    return f"❌ Failed to send file: {response.text}"
        except Exception as e:
            return f"❌ Telegram file error: {str(e)}"
    
    def open_app(self, app_name):
        """Open applications by name"""
        try:
            if app_name.lower() in ["explorer", "file explorer"]:
                subprocess.Popen("explorer .")
                return "✅ File explorer opened!"
            elif app_name.lower() in ["chrome", "browser"]:
                subprocess.Popen("start chrome")
                return "✅ Chrome opened!"
            elif app_name.lower() in ["code", "vscode", "vs code"]:
                subprocess.Popen("code .")
                return "✅ VS Code opened!"
            elif app_name.lower() in ["notepad", "text editor"]:
                subprocess.Popen("notepad")
                return "✅ Notepad opened!"
            else:
                # Try to open with default program
                subprocess.Popen(f"start {app_name}")
                return f"✅ Attempted to open {app_name}"
        except Exception as e:
            return f"❌ Failed to open {app_name}: {str(e)}"
    
    def take_screenshot(self, send_to_telegram=True):
        """Take a screenshot and optionally send to Telegram"""
        try:
            import pyautogui
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            filename = f"screenshot_{timestamp}.png"
            
            screenshot = pyautogui.screenshot()
            screenshot.save(filename)
            
            result = f"✅ Screenshot saved as {filename}"
            
            # Send to Telegram if requested
            if send_to_telegram and self.telegram_chat_id:
                print(f"📤 Sending screenshot to Telegram chat ID: {self.telegram_chat_id}")
                telegram_result = self.send_telegram_file(filename, f"📸 Screenshot taken at {timestamp}")
                result += f"\n{telegram_result}"
            elif send_to_telegram and not self.telegram_chat_id:
                result += f"\n⚠️ No Telegram chat ID set - screenshot not sent to Telegram"
            
            return result
        except ImportError:
            return "❌ pyautogui not installed. Run: pip install pyautogui"
        except Exception as e:
            return f"❌ Screenshot failed: {str(e)}"
    
    def execute_command(self, command):
        """Execute any system command"""
        try:
            print(f"🔧 Executing: {command}")
            result = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT, text=True)
            return f"✅ Command executed successfully!\nOutput:\n{result}"
        except subprocess.CalledProcessError as e:
            return f"❌ Command failed:\n{e.output}"
        except Exception as e:
            return f"❌ Command error: {str(e)}"
    
    def shutdown_computer(self, minutes=0):
        """Shutdown computer after specified minutes"""
        try:
            if minutes == 0:
                subprocess.run(["shutdown", "/s", "/t", "0"])
                return "🔄 Shutting down computer..."
            else:
                subprocess.run(["shutdown", "/s", "/t", str(minutes * 60)])
                return f"⏰ Computer will shutdown in {minutes} minutes"
        except Exception as e:
            return f"❌ Shutdown failed: {str(e)}"
    
    def cancel_shutdown(self):
        """Cancel scheduled shutdown"""
        try:
            subprocess.run(["shutdown", "/a"])
            return "✅ Shutdown cancelled"
        except Exception as e:
            return f"❌ Failed to cancel shutdown: {str(e)}"
    
    def list_files(self, directory="."):
        """List files in directory"""
        try:
            path = Path(directory)
            files = list(path.iterdir())
            result = f"📁 Files in {directory}:\n"
            for file in files[:10]:  # Limit to 10 files
                result += f"  {'📁' if file.is_dir() else '📄'} {file.name}\n"
            if len(files) > 10:
                result += f"  ... and {len(files) - 10} more files"
            return result
        except Exception as e:
            return f"❌ Failed to list files: {str(e)}"
    
    def create_folder(self, folder_name):
        """Create a new folder"""
        try:
            Path(folder_name).mkdir(exist_ok=True)
            return f"✅ Folder '{folder_name}' created"
        except Exception as e:
            return f"❌ Failed to create folder: {str(e)}"
    
    def delete_file(self, file_path):
        """Delete a file or folder"""
        try:
            path = Path(file_path)
            if path.exists():
                if path.is_file():
                    path.unlink()
                else:
                    import shutil
                    shutil.rmtree(path)
                return f"✅ Deleted {file_path}"
            else:
                return f"❌ File {file_path} not found"
        except Exception as e:
            return f"❌ Failed to delete {file_path}: {str(e)}"
    
    def get_system_info(self):
        """Get system information"""
        try:
            import psutil
            cpu_percent = psutil.cpu_percent()
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            
            info = f"🖥️ System Information:\n"
            info += f"CPU Usage: {cpu_percent}%\n"
            info += f"Memory: {memory.percent}% used ({memory.used // (1024**3)}GB / {memory.total // (1024**3)}GB)\n"
            info += f"Disk: {disk.percent}% used ({disk.used // (1024**3)}GB / {disk.total // (1024**3)}GB)"
            
            return info
        except ImportError:
            return "❌ psutil not installed. Run: pip install psutil"
        except Exception as e:
            return f"❌ Failed to get system info: {str(e)}"

# Global instance
system = SystemController() 
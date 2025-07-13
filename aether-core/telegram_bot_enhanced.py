#!/usr/bin/env python3
"""
Enhanced Telegram Bot - Terminal Command Execution
Can run terminal commands directly like Cursor does
"""

import requests
import time
import json
import subprocess
import os
from actions.system_control import system

print("🔧 Loading Enhanced Telegram Bot with Terminal Command Execution")

BOT_TOKEN = '8002118162:AAGfvEmGBXns_PfsdAq5OREJS7_73M1yfzE'
BASE_URL = f'https://api.telegram.org/bot{BOT_TOKEN}/'
LAST_UPDATE_ID = None

def get_updates():
    global LAST_UPDATE_ID
    response = requests.get(BASE_URL + 'getUpdates', params={'offset': LAST_UPDATE_ID, 'timeout': 100})
    data = response.json()
    if 'result' in data:
        return data['result']
    return []

def send_message(chat_id, text):
    try:
        response = requests.post(BASE_URL + 'sendMessage', data={'chat_id': chat_id, 'text': text})
        if response.status_code != 200:
            print(f"❌ Failed to send message: {response.text}")
        else:
            print(f"✅ Message sent successfully")
    except Exception as e:
        print(f"❌ Error sending message: {e}")

def send_file(chat_id, file_path, caption=""):
    """Send a file to Telegram"""
    try:
        with open(file_path, 'rb') as f:
            files = {'document': f}
            data = {'chat_id': chat_id, 'caption': caption}
            response = requests.post(BASE_URL + 'sendDocument', data=data, files=files)
            if response.status_code == 200:
                print(f"✅ File sent successfully: {file_path}")
                return True
            else:
                print(f"❌ Failed to send file: {response.text}")
                return False
    except Exception as e:
        print(f"❌ Error sending file: {e}")
        return False

def execute_terminal_command(command):
    """Execute a terminal command and return the result"""
    try:
        print(f"🔧 Executing command: {command}")
        result = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT, text=True)
        return f"✅ Command executed successfully!\nOutput:\n{result}"
    except subprocess.CalledProcessError as e:
        return f"❌ Command failed:\n{e.output}"
    except Exception as e:
        return f"❌ Command error: {str(e)}"

def run_telegram_loop():
    print("📱 Enhanced Telegram Bot with Terminal Commands is online.")
    print("🔧 Commands available:")
    print("  - run: command (execute terminal command)")
    print("  - screenshot (take screenshot)")
    print("  - system info (get system info)")
    print("  - explorer (open file explorer)")
    print("  - help (show all commands)")
    
    global LAST_UPDATE_ID
    while True:
        updates = get_updates()
        for update in updates:
            LAST_UPDATE_ID = update['update_id'] + 1
            if 'message' in update and 'text' in update['message']:
                chat_id = update['message']['chat']['id']
                user_msg = update['message']['text']
                
                # Set the Telegram chat ID for system control
                system.set_telegram_chat_id(chat_id)
                print(f"📱 Chat ID set: {chat_id}")
                print(f"📩 {user_msg}")
                
                # Handle different command types
                if user_msg.lower().startswith("run:"):
                    # Execute terminal command
                    command = user_msg.replace("run:", "").strip()
                    print(f"⚡ Processing terminal command: {command}")
                    result = execute_terminal_command(command)
                    print(f"🤖 Reply: {result}")
                    send_message(chat_id, result)
                    
                elif user_msg.lower() in ["screenshot", "take screenshot"]:
                    # Take screenshot
                    print("📸 Processing screenshot...")
                    result = system.take_screenshot(send_to_telegram=True)
                    print(f"🤖 Reply: {result}")
                    send_message(chat_id, result)
                    
                elif user_msg.lower() in ["system info", "sysinfo"]:
                    # Get system info
                    print("📊 Processing system info...")
                    result = system.get_system_info()
                    print(f"🤖 Reply: {result}")
                    send_message(chat_id, result)
                    
                elif user_msg.lower() in ["explorer", "file explorer"]:
                    # Open file explorer
                    print("🔧 Processing explorer...")
                    result = system.open_app("explorer")
                    print(f"🤖 Reply: {result}")
                    send_message(chat_id, result)
                    
                elif user_msg.lower() == "help":
                    # Show help
                    help_text = """🤖 Enhanced Telegram Bot Commands:

🔧 Terminal Commands:
- run: command (execute any terminal command)
- run: dir (list files)
- run: ipconfig (network info)
- run: tasklist (running processes)
- run: systeminfo (system details)

📸 Screenshot & System:
- screenshot (take screenshot + send to Telegram)
- system info (get system information)
- explorer (open file explorer)

💬 Examples:
- run: dir C:\\Users
- run: ipconfig /all
- run: tasklist /v
- run: systeminfo
- run: echo Hello World

🎯 Your computer is now fully controllable via Telegram!"""
                    print("❓ Processing help...")
                    print(f"🤖 Reply: {help_text}")
                    send_message(chat_id, help_text)
                    
                elif user_msg.lower() == "test":
                    # Test command
                    result = "🧪 Enhanced bot is working! Try:\n- run: dir\n- screenshot\n- system info"
                    print(f"🤖 Reply: {result}")
                    send_message(chat_id, result)
                    
                else:
                    # Default response
                    result = f"💬 You said: {user_msg}\n\nTry these commands:\n- run: dir\n- screenshot\n- system info\n- help"
                    print(f"🤖 Reply: {result}")
                    send_message(chat_id, result)

if __name__ == "__main__":
    run_telegram_loop() 
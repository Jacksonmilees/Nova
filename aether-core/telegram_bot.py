import requests
import time
import json
from core.thinker import think
from actions.system_control import system

# Debug: Print which module we're using
print("🔧 Loading Telegram bot with core.thinker module")

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

def run_telegram_loop():
    print("📱 Telegram Bot is online.")
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
                
                # Debug: Test which think function is being used
                if user_msg.lower() == "test":
                    reply = "🧪 Testing core.thinker module - if you see this, the new module is working!"
                else:
                    reply = think(user_msg)
                
                print(f"🤖 Reply: {reply}")
                send_message(chat_id, reply)

if __name__ == "__main__":
    run_telegram_loop() 
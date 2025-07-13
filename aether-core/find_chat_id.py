#!/usr/bin/env python3
"""
Find Telegram Chat ID
Helps you find your Telegram chat ID for testing
"""

import requests

BOT_TOKEN = '8002118162:AAGfvEmGBXns_PfsdAq5OREJS7_73M1yfzE'
BASE_URL = f'https://api.telegram.org/bot{BOT_TOKEN}/'

def get_updates():
    """Get updates from Telegram"""
    try:
        response = requests.get(BASE_URL + 'getUpdates', params={'timeout': 10})
        data = response.json()
        if 'result' in data:
            return data['result']
        return []
    except Exception as e:
        print(f"❌ Error getting updates: {e}")
        return []

def main():
    print("🔍 Finding your Telegram Chat ID")
    print("=" * 40)
    
    print("📱 Getting recent messages...")
    updates = get_updates()
    
    if not updates:
        print("❌ No messages found!")
        print("\n💡 To get your chat ID:")
        print("1. Send a message to your bot in Telegram")
        print("2. Run this script again")
        return
    
    print(f"✅ Found {len(updates)} recent messages")
    print("\n📋 Recent messages:")
    
    for i, update in enumerate(updates[-5:], 1):  # Show last 5 messages
        if 'message' in update:
            chat_id = update['message']['chat']['id']
            user_name = update['message']['from'].get('first_name', 'Unknown')
            text = update['message'].get('text', '[No text]')
            
            print(f"{i}. Chat ID: {chat_id}")
            print(f"   User: {user_name}")
            print(f"   Message: {text}")
            print()
    
    # Use the most recent chat ID
    latest_update = updates[-1]
    if 'message' in latest_update:
        chat_id = latest_update['message']['chat']['id']
        print(f"🎯 Your Chat ID: {chat_id}")
        print(f"💡 Use this ID for testing: {chat_id}")

if __name__ == "__main__":
    main() 
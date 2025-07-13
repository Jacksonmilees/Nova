# Telegram Bot Setup Guide

## 🎯 How to Test Screenshot + Telegram Integration

### Step 1: Start the Telegram Bot
```bash
cd aether-core
python telegram_bot.py
```

### Step 2: Send a Message to Your Bot
1. Open Telegram
2. Find your bot (the one with token: `8002118162:AAGfvEmGBXns_PfsdAq5OREJS7_73M1yfzE`)
3. Send any message (like "hello")

### Step 3: Check the Console Output
You should see something like:
```
📱 Chat ID set: 123456789
📩 hello
🔍 Processing: hello
🤖 Reply: Hello! How can I assist you today?
✅ Message sent successfully
```

### Step 4: Test Screenshot
Send "screenshot" to your bot. You should see:
```
📩 screenshot
🔍 Processing: screenshot
📤 Sending screenshot to Telegram chat ID: 123456789
✅ Screenshot saved as screenshot_20250713_045036.png
✅ File sent to Telegram
🤖 Reply: ✅ Screenshot saved as screenshot_20250713_045036.png
✅ File sent to Telegram
✅ Message sent successfully
```

## 🔧 Troubleshooting

### Issue: "No updates found"
**Solution**: Send a message to your bot first, then run the test.

### Issue: Screenshot not sent to Telegram
**Solution**: Make sure the chat ID is being set. Check the console output for "📱 Chat ID set: [number]"

### Issue: Bot not responding
**Solution**: 
1. Check if the bot is running
2. Make sure you're sending messages to the correct bot
3. Check the console for error messages

### Issue: API rate limits
**Solution**: Wait a few minutes and try again. The bot will still work for system commands even with API limits.

## 📱 Bot Commands to Test

### Screenshot Commands
```
screenshot          - Take screenshot and send to Telegram
take screenshot    - Same as above
```

### System Commands
```
system info        - Get system information
execute: dir       - Run directory listing
run command: ipconfig  - Run IP configuration
```

### File Operations
```
explorer           - Open file explorer
list files         - List current directory files
```

## 🎯 Expected Behavior

### When you send "screenshot":
1. ✅ Screenshot is taken
2. ✅ Screenshot is saved with timestamp
3. ✅ Screenshot is sent to your Telegram
4. ✅ You receive the screenshot in Telegram
5. ✅ Bot responds with success message

### When you send "system info":
1. ✅ System information is gathered
2. ✅ Information is sent to Telegram
3. ✅ Bot responds with system stats

### When you send "execute: dir":
1. ✅ Command is executed
2. ✅ Output is captured
3. ✅ Output is sent to Telegram
4. ✅ Bot responds with command output

## 🔍 Debug Information

The bot will show debug information in the console:
- `📱 Chat ID set: [number]` - Shows your chat ID is set
- `📤 Sending screenshot to Telegram chat ID: [number]` - Shows screenshot is being sent
- `✅ File sent to Telegram` - Shows successful Telegram upload
- `❌ Failed to send file: [error]` - Shows Telegram errors

## 🚀 Quick Test

1. **Start the bot**:
   ```bash
   python telegram_bot.py
   ```

2. **Send to your bot**:
   ```
   screenshot
   ```

3. **Check Telegram** - You should receive the screenshot

4. **Check console** - You should see success messages

## 🎉 Success Indicators

- ✅ Screenshot appears in your Telegram
- ✅ Console shows "✅ File sent to Telegram"
- ✅ Bot responds with success message
- ✅ No error messages in console

---

**🎯 If you're still having issues, please share the console output when you send "screenshot" to your bot!** 
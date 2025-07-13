# NOVA GUI Interface
import tkinter as tk
from tkinter import scrolledtext, ttk
import threading
import queue
import datetime
from core.thinker import think, init_memory, init_tasks
from interface.voice import speak, listen

class NovaUI:
    def __init__(self, root):
        self.root = root
        self.root.title("NOVA AI Interface")
        self.root.geometry("800x600")
        self.root.configure(bg="#1e1e2f")
        
        # Initialize NOVA systems
        init_memory()
        init_tasks()
        
        # Message queue for thread-safe updates
        self.message_queue = queue.Queue()
        self.root.after(100, self.check_queue)
        
        self.setup_ui()
        
    def setup_ui(self):
        # Main frame
        main_frame = tk.Frame(self.root, bg="#1e1e2f")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Title
        title_label = tk.Label(main_frame, text="🔵 NOVA AI INTERFACE", 
                              font=("Arial", 16, "bold"), 
                              bg="#1e1e2f", fg="#00ff88")
        title_label.pack(pady=(0, 10))
        
        # Chat area
        chat_frame = tk.Frame(main_frame, bg="#1e1e2f")
        chat_frame.pack(fill=tk.BOTH, expand=True)
        
        # Text area with custom styling
        self.text_area = scrolledtext.ScrolledText(
            chat_frame, 
            wrap=tk.WORD, 
            bg="#2d2d3f", 
            fg="#ffffff", 
            font=("Consolas", 11),
            insertbackground="#ffffff",
            selectbackground="#404060"
        )
        self.text_area.pack(fill=tk.BOTH, expand=True, padx=(0, 5))
        
        # Right sidebar for controls
        sidebar = tk.Frame(chat_frame, bg="#1e1e2f", width=200)
        sidebar.pack(side=tk.RIGHT, fill=tk.Y, padx=(5, 0))
        sidebar.pack_propagate(False)
        
        # Control buttons
        controls_frame = tk.Frame(sidebar, bg="#1e1e2f")
        controls_frame.pack(fill=tk.X, pady=5)
        
        # Voice button
        self.voice_btn = tk.Button(
            controls_frame, 
            text="🎤 Voice Input", 
            command=self.voice_input,
            bg="#4a4a6a",
            fg="#ffffff",
            font=("Arial", 10, "bold"),
            relief=tk.FLAT,
            padx=10,
            pady=5
        )
        self.voice_btn.pack(fill=tk.X, pady=2)
        
        # Send button
        self.send_btn = tk.Button(
            controls_frame, 
            text="▶️ Send", 
            command=self.send_message,
            bg="#00aa44",
            fg="#ffffff",
            font=("Arial", 10, "bold"),
            relief=tk.FLAT,
            padx=10,
            pady=5
        )
        self.send_btn.pack(fill=tk.X, pady=2)
        
        # Clear button
        self.clear_btn = tk.Button(
            controls_frame, 
            text="🗑️ Clear", 
            command=self.clear_chat,
            bg="#aa4444",
            fg="#ffffff",
            font=("Arial", 10, "bold"),
            relief=tk.FLAT,
            padx=10,
            pady=5
        )
        self.clear_btn.pack(fill=tk.X, pady=2)
        
        # Help button
        self.help_btn = tk.Button(
            controls_frame, 
            text="❓ Help", 
            command=self.show_help,
            bg="#4444aa",
            fg="#ffffff",
            font=("Arial", 10, "bold"),
            relief=tk.FLAT,
            padx=10,
            pady=5
        )
        self.help_btn.pack(fill=tk.X, pady=2)
        
        # Status frame
        status_frame = tk.Frame(main_frame, bg="#1e1e2f")
        status_frame.pack(fill=tk.X, pady=(10, 0))
        
        # Status label
        self.status_label = tk.Label(
            status_frame, 
            text="🟢 Ready", 
            bg="#1e1e2f", 
            fg="#00ff88",
            font=("Arial", 10)
        )
        self.status_label.pack(side=tk.LEFT)
        
        # Input area
        input_frame = tk.Frame(main_frame, bg="#1e1e2f")
        input_frame.pack(fill=tk.X, pady=(10, 0))
        
        # Entry with custom styling
        self.entry = tk.Entry(
            input_frame, 
            font=("Consolas", 12),
            bg="#2d2d3f",
            fg="#ffffff",
            insertbackground="#ffffff",
            relief=tk.FLAT,
            bd=2
        )
        self.entry.pack(fill=tk.X, side=tk.LEFT, expand=True)
        self.entry.bind("<Return>", self.send_message)
        self.entry.focus()
        
        # Quick commands frame
        quick_frame = tk.Frame(main_frame, bg="#1e1e2f")
        quick_frame.pack(fill=tk.X, pady=(5, 0))
        
        # Quick command buttons
        quick_commands = [
            ("🔧 Explorer", "explorer"),
            ("🌐 Chrome", "chrome"),
            ("📝 Code", "code"),
            ("📸 Screenshot", "screenshot"),
            ("📋 Tasks", "list tasks"),
            ("❓ Help", "help")
        ]
        
        for text, command in quick_commands:
            btn = tk.Button(
                quick_frame,
                text=text,
                command=lambda cmd=command: self.quick_command(cmd),
                bg="#3a3a5a",
                fg="#ffffff",
                font=("Arial", 9),
                relief=tk.FLAT,
                padx=8,
                pady=3
            )
            btn.pack(side=tk.LEFT, padx=2)
        
        # Welcome message
        self.add_message("🔵 NOVA ONLINE - Voice and Text Interface Ready!", "system")
        self.add_message("Type your message or click 🎤 for voice input.", "system")
        
    def add_message(self, message, sender="user"):
        """Add message to chat area with proper formatting"""
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        
        if sender == "user":
            prefix = f"[{timestamp}] 🧠 You: "
            color = "#88aaff"
        elif sender == "nova":
            prefix = f"[{timestamp}] 🤖 NOVA: "
            color = "#88ff88"
        else:  # system
            prefix = f"[{timestamp}] {message}"
            color = "#ffaa44"
            message = ""
        
        self.text_area.insert(tk.END, prefix)
        self.text_area.insert(tk.END, message + "\n\n")
        
        # Apply colors
        start = self.text_area.index("end-3c linestart")
        end = self.text_area.index("end-1c")
        self.text_area.tag_add(sender, start, end)
        self.text_area.tag_config(sender, foreground=color)
        
        self.text_area.see(tk.END)
        
    def send_message(self, event=None):
        """Send text message"""
        prompt = self.entry.get().strip()
        if not prompt:
            return
            
        self.entry.delete(0, tk.END)
        self.add_message(prompt, "user")
        
        # Process in thread to avoid blocking UI
        threading.Thread(target=self.process_message, args=(prompt,), daemon=True).start()
        
    def process_message(self, prompt):
        """Process message in background thread"""
        try:
            self.update_status("🔄 Thinking...")
            reply = think(prompt)
            self.message_queue.put(("nova", reply))
            self.update_status("🟢 Ready")
        except Exception as e:
            error_msg = f"Error: {str(e)}"
            self.message_queue.put(("nova", error_msg))
            self.update_status("🔴 Error")
            
    def voice_input(self):
        """Handle voice input"""
        self.voice_btn.config(state=tk.DISABLED)
        self.update_status("🎙️ Listening...")
        
        # Process voice in thread
        threading.Thread(target=self.process_voice, daemon=True).start()
        
    def process_voice(self):
        """Process voice input in background thread"""
        try:
            prompt = listen()
            if prompt:
                self.message_queue.put(("user", prompt))
                self.process_message(prompt)
            else:
                self.message_queue.put(("system", "No voice input detected."))
        except Exception as e:
            self.message_queue.put(("system", f"Voice error: {str(e)}"))
        finally:
            self.voice_btn.config(state=tk.NORMAL)
            self.update_status("🟢 Ready")
            
    def quick_command(self, command):
        """Execute quick command"""
        self.entry.delete(0, tk.END)
        self.entry.insert(0, command)
        self.send_message()
        
    def clear_chat(self):
        """Clear chat area"""
        self.text_area.delete(1.0, tk.END)
        self.add_message("Chat cleared.", "system")
        
    def show_help(self):
        """Show help information"""
        help_text = """🤖 NOVA Commands:

🔧 System Control:
- explorer/chrome/code (open apps)
- screenshot (take screenshot)
- shutdown [minutes] (shutdown computer)
- cancel shutdown (abort shutdown)
- list files [directory] (list files)
- create folder [name] (create folder)
- delete [file] (delete file/folder)

📝 Task Management:
- add task: description
- list tasks
- complete task: name

🔍 Research:
- research: query
- learn from: url | skillname
- learn api: url | skillname

⚡ Skills:
- create skill: name | code
- run skill: module.function(args)
- reload skills

🎙️ Voice Commands:
- Click 🎤 button to speak
- Type or speak naturally

💬 Chat: Just ask questions!"""
        
        self.add_message(help_text, "nova")
        
    def update_status(self, status):
        """Update status label"""
        self.message_queue.put(("status", status))
        
    def check_queue(self):
        """Check message queue for updates"""
        try:
            while True:
                msg_type, message = self.message_queue.get_nowait()
                
                if msg_type == "status":
                    self.status_label.config(text=message)
                else:
                    self.add_message(message, msg_type)
                    
        except queue.Empty:
            pass
        
        self.root.after(100, self.check_queue)

def main():
    root = tk.Tk()
    app = NovaUI(root)
    root.mainloop()

if __name__ == "__main__":
    main() 
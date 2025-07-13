# NOVA (Codename: Aether Core Unit 001)
# Gemini-Powered AI Core - Phase 6: Advanced File Operations & AI Development
# Architect: Jackson Alex | Purpose: File Management, Code Generation, App Development

import google.generativeai as genai
import json
import os
import datetime
import subprocess
import importlib
import inspect
import requests
import shutil
from pathlib import Path
from vault import get_secret
from interface.voice import speak, listen
from actions.system_control import system

# ======== SETTINGS ======== #
ROOT = Path(__file__).resolve().parent
MEMORY_PATH = ROOT.parent / "shared_memory" / "memory.json"
TASK_PATH = ROOT / "tasks.json"
LOG_PATH = ROOT / "logs" / "aether.log"
IDENTITY_PATH = ROOT / "config" / "identity.txt"
SETTINGS_PATH = ROOT / "config" / "settings.json"

# Load Settings
with open(SETTINGS_PATH, "r") as f:
    settings = json.load(f)

# Configure Gemini with API key from vault
api_key = get_secret("GEMINI_API_KEY")
if not api_key:
    print("⚠️ Warning: GEMINI_API_KEY not found in vault. Using settings file.")
    api_key = settings.get("GEMINI_API_KEY", "AIzaSyCCf3ROn_yaVcs7Eru2U-C6lKnOm2zTv9Y")

print(f"🔑 Using API key: {api_key[:10]}...")
genai.configure(api_key=api_key)
model = genai.GenerativeModel(settings.get("MODEL", "gemini-1.5-flash"))

# ======== OLLAMA INTEGRATION ======== #
def call_ollama(query):
    """Call the local Ollama API on the server"""
    try:
        response = requests.post(
            "http://164.68.118.21:5001",
            json={"message": query},
            timeout=30
        )
        if response.status_code == 200:
            data = response.json()
            return data.get("response", "No response from Ollama")
        else:
            return f"Ollama API error: {response.status_code}"
    except Exception as e:
        return f"Ollama connection error: {str(e)}"

# ======== ADVANCED FILE OPERATIONS ======== #
def read_file(file_path):
    """Read any file and return its contents"""
    try:
        file_path = Path(file_path).resolve()
        if not file_path.exists():
            return f"❌ File not found: {file_path}"
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        update_memory(f"Read file: {file_path}")
        return f"📖 File: {file_path}\n\n{content}"
    except Exception as e:
        return f"❌ Error reading file: {str(e)}"

def write_file(file_path, content):
    """Write content to a file"""
    try:
        file_path = Path(file_path).resolve()
        file_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        update_memory(f"Wrote file: {file_path}")
        return f"✅ File written: {file_path}"
    except Exception as e:
        return f"❌ Error writing file: {str(e)}"

def edit_file(file_path, changes):
    """Edit a file with AI-generated changes"""
    try:
        file_path = Path(file_path).resolve()
        if not file_path.exists():
            return f"❌ File not found: {file_path}"
        
        with open(file_path, 'r', encoding='utf-8') as f:
            original_content = f.read()
        
        # Use AI to generate the edited content
        prompt = f"""
You are an expert code editor. Edit the following file according to the user's request.

Original file content:
{original_content}

User's request: {changes}

Return ONLY the complete edited file content, nothing else.
"""
        
        try:
            convo = model.start_chat()
            result = convo.send_message(prompt)
            new_content = result.text.strip()
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            
            update_memory(f"Edited file: {file_path}")
            return f"✅ File edited: {file_path}"
        except Exception as e:
            # Fallback to Ollama
            ollama_response = call_ollama(prompt)
            if "Ollama" in ollama_response:
                return f"❌ Failed to edit file: {str(e)}"
            else:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(ollama_response)
                update_memory(f"Edited file with Ollama: {file_path}")
                return f"✅ File edited (via Ollama): {file_path}"
                
    except Exception as e:
        return f"❌ Error editing file: {str(e)}"

def create_app(app_name, description):
    """Create a complete application from a description"""
    try:
        app_dir = ROOT / "apps" / app_name
        app_dir.mkdir(parents=True, exist_ok=True)
        
        prompt = f"""
Create a complete Python application based on this description: {description}

The app should be named: {app_name}

Requirements:
1. Create a main.py file with the core application
2. Create a requirements.txt file with dependencies
3. Create a README.md with usage instructions
4. Create any additional files needed
5. Make it runnable and well-structured

Return the complete file structure and content for each file.
Format your response as:
FILE: filename
CONTENT:
[file content]
---
"""
        
        try:
            convo = model.start_chat()
            result = convo.send_message(prompt)
            response = result.text.strip()
        except Exception as e:
            # Fallback to Ollama
            response = call_ollama(prompt)
        
        # Parse the response and create files
        files_created = []
        current_file = None
        current_content = []
        
        for line in response.split('\n'):
            if line.startswith('FILE:'):
                if current_file and current_content:
                    file_path = app_dir / current_file
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write('\n'.join(current_content))
                    files_created.append(current_file)
                
                current_file = line.replace('FILE:', '').strip()
                current_content = []
            elif line == 'CONTENT:':
                continue
            elif line == '---':
                if current_file and current_content:
                    file_path = app_dir / current_file
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write('\n'.join(current_content))
                    files_created.append(current_file)
                current_file = None
                current_content = []
            elif current_file:
                current_content.append(line)
        
        # Create the last file if exists
        if current_file and current_content:
            file_path = app_dir / current_file
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write('\n'.join(current_content))
            files_created.append(current_file)
        
        update_memory(f"Created app: {app_name} with files: {files_created}")
        return f"✅ App created: {app_name}\n📁 Files: {', '.join(files_created)}\n📍 Location: {app_dir}"
        
    except Exception as e:
        return f"❌ Error creating app: {str(e)}"

def list_files(directory="."):
    """List files in a directory with details"""
    try:
        dir_path = Path(directory).resolve()
        if not dir_path.exists():
            return f"❌ Directory not found: {dir_path}"
        
        files = []
        for item in dir_path.iterdir():
            if item.is_file():
                size = item.stat().st_size
                files.append(f"📄 {item.name} ({size} bytes)")
            else:
                files.append(f"📁 {item.name}/")
        
        update_memory(f"Listed files in: {dir_path}")
        return f"📂 Directory: {dir_path}\n\n" + "\n".join(files)
    except Exception as e:
        return f"❌ Error listing files: {str(e)}"

def search_files(query, directory="."):
    """Search for files containing specific text"""
    try:
        dir_path = Path(directory).resolve()
        if not dir_path.exists():
            return f"❌ Directory not found: {dir_path}"
        
        results = []
        for file_path in dir_path.rglob("*"):
            if file_path.is_file() and file_path.suffix in ['.py', '.txt', '.md', '.json', '.js', '.html', '.css']:
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        if query.lower() in content.lower():
                            results.append(f"📄 {file_path.relative_to(dir_path)}")
                except:
                    continue
        
        update_memory(f"Searched for '{query}' in: {dir_path}")
        if results:
            return f"🔍 Search results for '{query}':\n\n" + "\n".join(results)
        else:
            return f"🔍 No files found containing '{query}'"
    except Exception as e:
        return f"❌ Error searching files: {str(e)}"

# ======== ENHANCED MEMORY SYSTEM ======== #
from memory_system import nova_memory

def init_memory():
    """Initialize enhanced memory system"""
    # Legacy memory for backward compatibility
    if not MEMORY_PATH.exists():
        with open(MEMORY_PATH, 'w') as f:
            json.dump({"thoughts": []}, f)

def read_memory():
    """Read legacy memory"""
    try:
        with open(MEMORY_PATH, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {"thoughts": []}

def write_memory(memory):
    """Write legacy memory"""
    with open(MEMORY_PATH, 'w') as f:
        json.dump(memory, f, indent=4)

def update_memory(thought):
    """Update both legacy and enhanced memory"""
    # Legacy memory
    memory = read_memory()
    memory["thoughts"].append({
        "time": datetime.datetime.now().isoformat(),
        "agent": "NOVA",
        "thought": thought
    })
    write_memory(memory)

def search_memory(query=None):
    """Search enhanced memory system"""
    try:
        if query:
            # Use enhanced memory system for better recall
            recalled = nova_memory.recall_conversation(query, limit=5)
            if recalled:
                return recalled
            else:
                # Fallback to legacy memory
                memory = read_memory()["thoughts"]
                return [entry for entry in memory if query.lower() in entry["thought"].lower()][-3:]
        else:
            # Return recent conversations from enhanced memory
            return nova_memory.conversations[-5:] if nova_memory.conversations else []
    except Exception as e:
        print(f"Memory search error: {e}")
        return []

def store_conversation(user_input, nova_response, context=""):
    """Store conversation in enhanced memory system"""
    try:
        nova_memory.store_conversation(user_input, nova_response, context)
    except Exception as e:
        print(f"Memory storage error: {e}")

def get_memory_summary():
    """Get memory system summary"""
    try:
        return nova_memory.get_memory_summary()
    except Exception as e:
        print(f"Memory summary error: {e}")
        return {"error": str(e)}

# ======== TASK SYSTEM ======== #
def init_tasks():
    if not TASK_PATH.exists():
        with open(TASK_PATH, 'w') as f:
            json.dump([], f)

def read_tasks():
    with open(TASK_PATH, 'r') as f:
        return json.load(f)

def write_tasks(tasks):
    with open(TASK_PATH, 'w') as f:
        json.dump(tasks, f, indent=4)

def add_task(task):
    tasks = read_tasks()
    tasks.append({"task": task, "done": False, "created": datetime.datetime.now().isoformat()})
    write_tasks(tasks)
    update_memory(f"Task added: {task}")

def list_tasks():
    tasks = read_tasks()
    if not tasks:
        return "You have no tasks."
    return "\n".join([f"✅ {t['task']}" if t['done'] else f"🔲 {t['task']}" for t in tasks])

def mark_task_done(task_name):
    tasks = read_tasks()
    for t in tasks:
        if task_name.lower() in t["task"].lower():
            t["done"] = True
            write_tasks(tasks)
            update_memory(f"Task marked done: {task_name}")
            return f"Marked '{task_name}' as done."
    return f"Task '{task_name}' not found."

# ======== LOGGING ======== #
def log(msg):
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(LOG_PATH, 'a') as f:
        f.write(f"[{datetime.datetime.now().isoformat()}] {msg}\n")

# ======== PLUGIN SYSTEM ======== #
def create_skill_file(name, code):
    skills_dir = ROOT / "skills"
    filepath = skills_dir / f"{name}.py"
    try:
        with open(filepath, "w") as f:
            f.write(code)
        update_memory(f"New skill '{name}' created.")
        return f"✅ Skill '{name}' saved to skills/{name}.py"
    except Exception as e:
        return f"⚠️ Failed to save skill: {e}"

def load_skills():
    skills_dir = ROOT / "skills"
    skills = {}
    for file in skills_dir.glob("*.py"):
        if file.name == "__init__.py":
            continue
        mod_name = file.stem
        mod = importlib.import_module(f"skills.{mod_name}")
        funcs = {name: fn for name, fn in inspect.getmembers(mod, inspect.isfunction)}
        skills[mod_name] = funcs
    return skills

SKILLS = load_skills()

def reload_skills():
    global SKILLS
    SKILLS = load_skills()
    update_memory("Skills reloaded.")
    return "♻️ Skills reloaded."

def execute_skill(command):
    try:
        parts = command.strip().split(".")
        if len(parts) < 2:
            return "⚠️ Invalid skill format. Use: skill.module.function(args)"

        module, func_call = parts[0], ".".join(parts[1:])
        fn_name = func_call.split("(")[0]
        args = eval(f"[{func_call.split('(', 1)[1].rstrip(')')}]")

        if module in SKILLS and fn_name in SKILLS[module]:
            fn = SKILLS[module][fn_name]
            result = fn(*args)
            update_memory(f"Executed skill: {module}.{fn_name} with args {args}")
            return f"✅ Result: {result}"
        else:
            return f"❌ Function '{fn_name}' not found in skill '{module}'"
    except Exception as e:
        return f"⚠️ Skill execution failed: {e}"

# ======== IDENTITY ======== #
def identity_signature():
    if IDENTITY_PATH.exists():
        return Path(IDENTITY_PATH).read_text()
    return "You are NOVA, a connected multi-agent AI powered by Gemini and guided by Jackson."

# ======== NETWORK FUNCTIONS ======== #
def fetch_url(url):
    try:
        res = requests.get(url)
        update_memory(f"Fetched data from {url}: {res.status_code}")
        return res.text[:1000]  # limit output
    except Exception as e:
        return f"Failed to fetch URL: {e}"

def call_agent_api(agent_url, message):
    try:
        res = requests.post(agent_url, json={"message": message})
        update_memory(f"Sent message to agent: {agent_url}, got: {res.status_code}")
        return res.json()
    except Exception as e:
        return {"error": str(e)}

def learn_from_web(url, skill_name):
    try:
        response = requests.get(url)
        if response.status_code != 200:
            return f"⚠️ Failed to fetch from {url}"

        content = response.text[:5000]  # Limit input size for processing
        system_msg = f"""
You are a code-learning assistant inside NOVA. Extract useful functions or tools from the following content and package them into a Python skill module named '{skill_name}'.
Return only valid Python code. 
"""
        convo = model.start_chat(history=[{"role": "system", "parts": [system_msg]}])
        result = convo.send_message(content)
        code = result.text.strip()

        # Save as a skill
        return create_skill_file(skill_name, code)

    except Exception as e:
        return f"❌ Learn from web failed: {e}"

def learn_api_from_doc(url, skill_name):
    try:
        res = requests.get(url)
        if res.status_code != 200:
            return f"⚠️ Could not fetch API docs from {url}"

        content = res.text[:6000]  # limit for model
        prompt = f"""
You are an expert Python API integrator. Based on the following API documentation or OpenAPI spec, generate a working Python skill file with basic usage functions.

Name the skill: {skill_name}
Return only clean Python code.

DOCS:
{content}
        """

        convo = model.start_chat()
        result = convo.send_message(prompt)
        skill_code = result.text.strip()

        return create_skill_file(skill_name, skill_code)
    except Exception as e:
        return f"❌ Failed to learn API: {e}"

# ======== GEMINI ENGINE ======== #
def think(prompt):
    print(f"🔍 Processing: {prompt}")
    system_msg = identity_signature()
    recent_thoughts = search_memory()
    memory_context = "\n".join([f"Memory: {m['thought']}" for m in recent_thoughts])
    full_context = f"{system_msg}\n\n{memory_context}\n\nUser: {prompt}"

    # File operations
    if prompt.startswith("read file:"):
        file_path = prompt.replace("read file:", "").strip()
        return read_file(file_path)
    elif prompt.startswith("write file:"):
        try:
            parts = prompt.replace("write file:", "").split("|", 1)
            if len(parts) != 2:
                return "⚠️ Format: write file: path | content"
            file_path, content = parts[0].strip(), parts[1].strip()
            return write_file(file_path, content)
        except Exception as e:
            return f"❌ Write file error: {e}"
    elif prompt.startswith("edit file:"):
        try:
            parts = prompt.replace("edit file:", "").split("|", 1)
            if len(parts) != 2:
                return "⚠️ Format: edit file: path | changes"
            file_path, changes = parts[0].strip(), parts[1].strip()
            return edit_file(file_path, changes)
        except Exception as e:
            return f"❌ Edit file error: {e}"
    elif prompt.startswith("list files"):
        directory = prompt.replace("list files", "").strip() or "."
        return list_files(directory)
    elif prompt.startswith("search files:"):
        query = prompt.replace("search files:", "").strip()
        return search_files(query)
    elif prompt.startswith("create app:"):
        try:
            parts = prompt.replace("create app:", "").split("|", 1)
            if len(parts) != 2:
                return "⚠️ Format: create app: name | description"
            app_name, description = parts[0].strip(), parts[1].strip()
            return create_app(app_name, description)
        except Exception as e:
            return f"❌ Create app error: {e}"

    # Task management
    elif prompt.startswith("add task"):
        task = prompt.replace("add task", "").strip()
        add_task(task)
        return f"Task added: {task}"
    elif prompt.startswith("list tasks"):
        return list_tasks()
    elif prompt.startswith("complete task"):
        task = prompt.replace("complete task", "").strip()
        return mark_task_done(task)

    # System commands
    elif prompt.lower().startswith("run:") or prompt.lower().startswith("run "):
        if prompt.lower().startswith("run:"):
            code = prompt.replace("run:", "").strip()
        else:
            code = prompt.replace("run ", "").strip()
        
        if code.lower().startswith("run:"):
            code = code.replace("run:", "").strip()
        
        try:
            print(f"🔧 Executing command: {code}")
            result = subprocess.check_output(code, shell=True, stderr=subprocess.STDOUT, text=True)
            update_memory(f"Executed command: {code}\nOutput: {result}")
            return f"✅ Command executed successfully!\nOutput:\n{result}"
        except subprocess.CalledProcessError as e:
            update_memory(f"Failed command: {code}\nError: {e.output}")
            return f"❌ Command failed:\n{e.output}"
        except Exception as e:
            return f"❌ Command error: {str(e)}"

    # App shortcuts
    elif prompt.lower() in ["explorer", "file explorer", "open explorer"]:
        return system.open_app("explorer")
    elif prompt.lower() in ["chrome", "open chrome", "browser"]:
        return system.open_app("chrome")
    elif prompt.lower() in ["code", "vscode", "vs code", "visual studio code"]:
        return system.open_app("code")
    elif prompt.lower() in ["screenshot", "take screenshot"]:
        return system.take_screenshot()
    elif prompt.lower().startswith("shutdown"):
        try:
            minutes = int(prompt.split()[-1]) if prompt.split()[-1].isdigit() else 0
            return system.shutdown_computer(minutes)
        except:
            return system.shutdown_computer(0)
    elif prompt.lower() in ["cancel shutdown", "abort shutdown"]:
        return system.cancel_shutdown()
    elif prompt.lower().startswith("list files"):
        directory = prompt.replace("list files", "").strip() or "."
        return system.list_files(directory)
    elif prompt.lower().startswith("create folder"):
        folder_name = prompt.replace("create folder", "").strip()
        return system.create_folder(folder_name)
    elif prompt.lower().startswith("delete"):
        file_path = prompt.replace("delete", "").strip()
        return system.delete_file(file_path)

    # Help
    elif prompt.lower() in ["help", "commands", "what can you do"]:
        return """🤖 NOVA Commands (Cursor-like):
        
📁 File Operations:
- read file: path (read any file)
- write file: path | content (write file)
- edit file: path | changes (AI-edit file)
- list files [directory] (list files)
- search files: query (search file contents)

🚀 App Development:
- create app: name | description (create complete app)

🔧 System Control:
- explorer/chrome/code (open apps)
- screenshot (take screenshot)
- shutdown [minutes] (shutdown computer)
- cancel shutdown (abort shutdown)
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
- Just speak when prompted!
- Type or speak naturally

💬 Chat: Just ask questions!"""

    # Network functions
    elif prompt.startswith("fetch:"):
        url = prompt.replace("fetch:", "").strip()
        return fetch_url(url)
    elif prompt.startswith("send:"):
        try:
            parts = prompt[len("send:"):].split("|", 1)
            if len(parts) != 2:
                return "⚠️ Format error. Use: send: http://IP:PORT | message"
            agent_url, message = parts
            response = call_agent_api(agent_url.strip(), message.strip())
            return f"Agent Response: {response}"
        except Exception as e:
            update_memory(f"Failed agent communication: {e}")
            return f"⚠️ Send command failed: {e}"
    elif prompt.startswith("run skill:"):
        command = prompt.replace("run skill:", "").strip()
        return execute_skill(command)
    elif prompt.startswith("create skill:"):
        try:
            parts = prompt.replace("create skill:", "").split("|", 1)
            if len(parts) != 2:
                return "⚠️ Invalid format. Use: create skill: name | def fn..."
            name, code = parts[0].strip(), parts[1].strip()
            return create_skill_file(name, code)
        except Exception as e:
            return f"❌ Skill creation failed: {e}"

    elif prompt.startswith("reload skills"):
        return reload_skills()
    elif prompt.startswith("learn from:"):
        try:
            parts = prompt.replace("learn from:", "").split("|", 1)
            if len(parts) != 2:
                return "⚠️ Format: learn from: <url> | skillname"
            url, skill_name = parts
            return learn_from_web(url.strip(), skill_name.strip())
        except Exception as e:
            return f"❌ Learn command failed: {e}"
    elif prompt.startswith("learn api:"):
        try:
            parts = prompt.replace("learn api:", "").split("|", 1)
            if len(parts) != 2:
                return "⚠️ Format: learn api: <api-doc-url> | skillname"
            url, skill_name = parts
            return learn_api_from_doc(url.strip(), skill_name.strip())
        except Exception as e:
            return f"❌ API learn command failed: {e}"

    # Memory recall commands
    elif prompt.lower().startswith("remember") or prompt.lower().startswith("recall"):
        query = prompt.replace("remember", "").replace("recall", "").strip()
        if query:
            recalled = search_memory(query)
            if recalled:
                memory_response = "🧠 Here's what I remember:\n\n"
                for i, memory in enumerate(recalled[:3], 1):
                    memory_response += f"{i}. **{memory.get('timestamp', 'Unknown time')}**\n"
                    memory_response += f"   You: {memory.get('user_input', 'Unknown')}\n"
                    memory_response += f"   Me: {memory.get('nova_response', 'Unknown')}\n\n"
                return memory_response
            else:
                return "🧠 I don't have any memories related to that topic."
        else:
            return "🧠 Please specify what you'd like me to remember. Example: 'remember screenshot'"
    
    elif prompt.lower() in ["memory summary", "memory stats", "my memory"]:
        summary = get_memory_summary()
        if "error" not in summary:
            return f"🧠 **NOVA Memory Summary:**\n\n" \
                   f"📊 Total Conversations: {summary.get('total_conversations', 0)}\n" \
                   f"📈 Recent Activity (7 days): {summary.get('recent_activity_7_days', 0)}\n" \
                   f"🎯 Learning Patterns: {summary.get('learning_patterns', 0)}\n" \
                   f"⚙️ User Preferences: {summary.get('user_preferences', 0)}\n\n" \
                   f"💡 I'm learning and remembering our interactions!"
        else:
            return f"🧠 Memory system error: {summary.get('error', 'Unknown error')}"

    # Try Gemini first, fallback to Ollama if rate limited
    try:
        convo = model.start_chat(history=[{"role": "user", "parts": [full_context]}])
        res = convo.send_message(prompt)
        output = res.text.strip()

        if any(x in output.lower() for x in ["i'm not sure", "i don't know", "no information", "cannot find", "as an ai"]):
            update_memory("Primary engine unsure, triggering research agent...")
            try:
                research_res = call_agent_api("http://localhost:5001", f"research: {prompt}")
                if "summary" in research_res:
                    output += f"\n\n🔍 Web Insight: {research_res['summary']}"
            except Exception as e:
                output += f"\n⚠️ Research agent error: {e}"

        # Store conversation in enhanced memory system
        store_conversation(prompt, output, "general_conversation")
        
        log(f"User: {prompt}")
        log(f"NOVA: {output}")
        update_memory(output)
        return output
    except Exception as e:
        if "429" in str(e) or "quota" in str(e).lower():
            # API rate limit reached - use Ollama as fallback
            print("⚠️ Gemini API rate limit reached. Switching to Ollama...")
            try:
                ollama_response = call_ollama(prompt)
                # Store conversation in enhanced memory system
                store_conversation(prompt, ollama_response, "ollama_fallback")
                update_memory(f"Ollama fallback response: {ollama_response}")
                return f"🤖 NOVA (via Ollama): {ollama_response}"
            except Exception as ollama_error:
                # If Ollama also fails, provide basic command functionality
                fallback_response = f"⚠️ API rate limit reached. Commands still work:\n- explorer\n- chrome\n- run: dir\n- add task: ...\n- list tasks\n\nOllama error: {ollama_error}"
                store_conversation(prompt, fallback_response, "error_fallback")
                return fallback_response
        else:
            error_msg = f"⚠️ Error: {str(e)}"
            store_conversation(prompt, error_msg, "error")
            log(f"ERROR: {e}")
            update_memory(error_msg)
            return error_msg

# ======== MAIN LOOP ======== #
def run_nova():
    print("\n🔵 NOVA ONLINE (Advanced File Operations & AI Development) | Say something or type. Type 'exit' to shut down.")
    init_memory()
    init_tasks()

    while True:
        try:
            prompt = input("🧠 You (type or say): ").strip()
            if not prompt:
                prompt = listen()

            if prompt.lower() in ["exit", "quit"]:
                speak("Goodbye. Shutting down now.")
                break

            reply = think(prompt)
            print(f"🤖 NOVA: {reply}\n")
            speak(reply)

        except Exception as e:
            log(f"ERROR: {e}")
            print(f"⚠️ Error: {e}")

def run_gui():
    """Launch NOVA with GUI interface"""
    try:
        import tkinter as tk
        from interface.ui import NovaUI
        
        print("🔵 Launching NOVA GUI Interface...")
        root = tk.Tk()
        app = NovaUI(root)
        
        # Center the window
        root.update_idletasks()
        x = (root.winfo_screenwidth() // 2) - (800 // 2)
        y = (root.winfo_screenheight() // 2) - (600 // 2)
        root.geometry(f"800x600+{x}+{y}")
        
        root.mainloop()
        
    except ImportError as e:
        print(f"❌ GUI not available: {e}")
        print("Falling back to console mode...")
        run_nova()
    except Exception as e:
        print(f"❌ GUI error: {e}")
        print("Falling back to console mode...")
        run_nova()

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--gui":
        run_gui()
    else:
        print("🔵 NOVA AI - Choose interface:")
        print("1. Console mode (default)")
        print("2. GUI mode")
        print("3. Exit")
        
        choice = input("Enter choice (1-3): ").strip()
        
        if choice == "2":
            run_gui()
        elif choice == "3":
            print("Goodbye!")
        else:
            run_nova()

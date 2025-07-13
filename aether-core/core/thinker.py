# Core thinking engine for NOVA
import google.generativeai as genai
import json
import os
import datetime
import subprocess
import importlib
import inspect
import requests
from pathlib import Path
from vault import get_secret
# from interface.voice import speak, listen
from actions.system_control import system

# ======== SETTINGS ======== #
ROOT = Path(__file__).resolve().parent.parent
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

# ======== MEMORY ======== #
def init_memory():
    if not MEMORY_PATH.exists():
        with open(MEMORY_PATH, 'w') as f:
            json.dump({"thoughts": []}, f)

def read_memory():
    try:
        with open(MEMORY_PATH, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        # Return default memory if file doesn't exist or is corrupted
        return {"thoughts": []}

def write_memory(memory):
    with open(MEMORY_PATH, 'w') as f:
        json.dump(memory, f, indent=4)

def update_memory(thought):
    memory = read_memory()
    memory["thoughts"].append({
        "time": datetime.datetime.now().isoformat(),
        "agent": "NOVA",
        "thought": thought
    })
    write_memory(memory)

def search_memory(query=None):
    try:
        memory = read_memory()["thoughts"]
        if query:
            return [entry for entry in memory if query.lower() in entry["thought"].lower()][-3:]
        return memory[-5:]
    except Exception as e:
        print(f"Memory search error: {e}")
        return []

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

def call_ollama(query):
    """Call the remote Ollama API on the VPS server with health check."""
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

# ======== GEMINI ENGINE ======== #
def think(prompt):
    print(f"🔍 Processing: {prompt}")
    system_msg = identity_signature()
    recent_thoughts = search_memory()
    memory_context = "\n".join([f"Memory: {m['thought']}" for m in recent_thoughts])
    full_context = f"{system_msg}\n\n{memory_context}\n\nUser: {prompt}"

    if prompt.startswith("add task"):
        task = prompt.replace("add task", "").strip()
        add_task(task)
        return f"Task added: {task}"
    elif prompt.startswith("list tasks"):
        return list_tasks()
    elif prompt.startswith("ask local:"):
        # Always use remote Ollama API for 'ask local:'
        query = prompt.replace("ask local:", "").strip()
        response = call_ollama(query)
        update_memory(f"Ollama answered: {response}")
        return response
    elif prompt.startswith("complete task"):
        task = prompt.replace("complete task", "").strip()
        return mark_task_done(task)
    elif prompt.lower().startswith("run:") or prompt.lower().startswith("run "):
        # Handle both "run: command" and "run command" formats
        if prompt.lower().startswith("run:"):
            code = prompt.replace("run:", "").strip()
        else:
            code = prompt.replace("run ", "").strip()
        
        # Remove any remaining "Run:" prefix if present
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
    elif prompt.lower() in ["explorer", "file explorer", "open explorer"]:
        return system.open_app("explorer")
    elif prompt.lower() in ["chrome", "open chrome", "browser"]:
        return system.open_app("chrome")
    elif prompt.lower() in ["code", "vscode", "vs code", "visual studio code"]:
        return system.open_app("code")
    elif prompt.lower() in ["screenshot", "take screenshot"]:
        return system.take_screenshot(send_to_telegram=True)
    elif prompt.lower() in ["system info", "systeminfo", "sysinfo"]:
        return system.get_system_info()
    elif prompt.lower().startswith("execute:") or prompt.lower().startswith("run command:"):
        # Extract command after "execute:" or "run command:"
        if prompt.lower().startswith("execute:"):
            command = prompt.replace("execute:", "").strip()
        elif prompt.lower().startswith("run command:"):
            command = prompt.replace("run command:", "").strip()
        else:
            command = prompt.strip()
        return system.execute_command(command)
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
    elif prompt.lower() in ["help", "commands", "what can you do"]:
        return """🤖 NOVA Commands:
        
🔧 System Control:
- explorer/chrome/code (open apps)
- screenshot (take screenshot + send to Telegram)
- system info (get system information)
- execute: command (run any system command)
- run command: command (alternative syntax)
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
- Just speak when prompted!
- Type or speak naturally

💬 Chat: Just ask questions!"""
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
        # Format: create skill: skillname | code
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

        log(f"User: {prompt}")
        log(f"NOVA: {output}")
        update_memory(output)
        return output
    except Exception as e:
        if "429" in str(e) or "quota" in str(e).lower():
            # Enhanced fallback mode when API is rate limited
            # Check if it's a system command that we can handle
            system_commands = [
                "screenshot", "take screenshot", "system info", "sysinfo", "systeminfo",
                "explorer", "chrome", "code", "help", "list tasks", "add task", "complete task"
            ]
            
            if any(cmd in prompt.lower() for cmd in system_commands):
                # Try to handle system commands even during API rate limits
                try:
                    if prompt.lower() in ["screenshot", "take screenshot"]:
                        return system.take_screenshot(send_to_telegram=True)
                    elif prompt.lower() in ["system info", "systeminfo", "sysinfo"]:
                        return system.get_system_info()
                    elif prompt.lower() in ["explorer", "file explorer", "open explorer"]:
                        return system.open_app("explorer")
                    elif prompt.lower() in ["chrome", "open chrome", "browser"]:
                        return system.open_app("chrome")
                    elif prompt.lower() in ["code", "vscode", "vs code", "visual studio code"]:
                        return system.open_app("code")
                    elif prompt.lower() in ["help", "commands", "what can you do"]:
                        return """🤖 NOVA Commands (API Rate Limited Mode):
                        
🔧 System Control:
- screenshot (take screenshot + send to Telegram)
- system info (get system information)
- explorer/chrome/code (open apps)
- execute: command (run any system command)
- run command: command (alternative syntax)

📝 Task Management:
- add task: description
- list tasks
- complete task: name

💬 Chat: System commands work even during API limits!"""
                    elif prompt.startswith("add task"):
                        task = prompt.replace("add task", "").strip()
                        add_task(task)
                        return f"Task added: {task}"
                    elif prompt.startswith("list tasks"):
                        return list_tasks()
                    elif prompt.startswith("complete task"):
                        task = prompt.replace("complete task", "").strip()
                        return mark_task_done(task)
                except Exception as sys_e:
                    return f"⚠️ System command failed: {str(sys_e)}"
            
            # Default fallback for non-system commands
            return f"⚠️ API rate limit reached. System commands still work:\n- screenshot\n- system info\n- explorer\n- execute: command\n- help"
        else:
            error_msg = f"⚠️ Error: {str(e)}"
            log(f"ERROR: {e}")
            update_memory(error_msg)
            return error_msg 
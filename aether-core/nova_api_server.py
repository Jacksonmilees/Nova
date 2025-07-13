#!/usr/bin/env python3
"""
NOVA API Server
Web-based interface for NOVA - accessible from anywhere
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os
import sys
from pathlib import Path

# Add the current directory to Python path
sys.path.append(str(Path(__file__).parent))

# Import NOVA's core functions
from main import think, init_memory, init_tasks, read_file, write_file, edit_file, create_app, list_files, search_files
from memory_system import nova_memory

app = Flask(__name__)
CORS(app)  # Allow cross-origin requests

# Initialize NOVA
init_memory()
init_tasks()

@app.route('/')
def home():
    """Home endpoint with NOVA info"""
    return jsonify({
        "status": "online",
        "name": "NOVA API Server",
        "version": "1.0",
        "capabilities": [
            "file_operations",
            "app_creation", 
            "task_management",
            "system_commands",
            "ai_chat"
        ],
        "endpoints": {
            "/": "This info",
            "/chat": "Send commands to NOVA",
            "/files/read": "Read files",
            "/files/write": "Write files", 
            "/files/edit": "Edit files with AI",
            "/files/list": "List files",
            "/files/search": "Search files",
            "/apps/create": "Create applications",
            "/tasks/add": "Add tasks",
            "/tasks/list": "List tasks",
            "/system/run": "Run system commands",
            "/memory/search": "Search memory",
            "/memory/store": "Store conversation",
            "/memory/summary": "Get memory summary",
            "/memory/preferences": "Get user preferences"
        }
    })

@app.route('/chat', methods=['POST'])
def chat():
    """Main NOVA chat endpoint"""
    try:
        data = request.get_json()
        if not data or 'message' not in data:
            return jsonify({"error": "No message provided"}), 400
        
        message = data['message']
        response = think(message)
        
        return jsonify({
            "success": True,
            "response": response,
            "command": message
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/files/read', methods=['POST'])
def read_file_endpoint():
    """Read a file"""
    try:
        data = request.get_json()
        if not data or 'path' not in data:
            return jsonify({"error": "No file path provided"}), 400
        
        file_path = data['path']
        response = read_file(file_path)
        
        return jsonify({
            "success": True,
            "response": response,
            "file_path": file_path
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/files/write', methods=['POST'])
def write_file_endpoint():
    """Write to a file"""
    try:
        data = request.get_json()
        if not data or 'path' not in data or 'content' not in data:
            return jsonify({"error": "No file path or content provided"}), 400
        
        file_path = data['path']
        content = data['content']
        response = write_file(file_path, content)
        
        return jsonify({
            "success": True,
            "response": response,
            "file_path": file_path
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/files/edit', methods=['POST'])
def edit_file_endpoint():
    """Edit a file with AI"""
    try:
        data = request.get_json()
        if not data or 'path' not in data or 'changes' not in data:
            return jsonify({"error": "No file path or changes provided"}), 400
        
        file_path = data['path']
        changes = data['changes']
        response = edit_file(file_path, changes)
        
        return jsonify({
            "success": True,
            "response": response,
            "file_path": file_path
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/files/list', methods=['POST'])
def list_files_endpoint():
    """List files in a directory"""
    try:
        data = request.get_json() or {}
        directory = data.get('directory', '.')
        response = list_files(directory)
        
        return jsonify({
            "success": True,
            "response": response,
            "directory": directory
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/files/search', methods=['POST'])
def search_files_endpoint():
    """Search files"""
    try:
        data = request.get_json()
        if not data or 'query' not in data:
            return jsonify({"error": "No search query provided"}), 400
        
        query = data['query']
        directory = data.get('directory', '.')
        response = search_files(query, directory)
        
        return jsonify({
            "success": True,
            "response": response,
            "query": query
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/apps/create', methods=['POST'])
def create_app_endpoint():
    """Create an application"""
    try:
        data = request.get_json()
        if not data or 'name' not in data or 'description' not in data:
            return jsonify({"error": "No app name or description provided"}), 400
        
        app_name = data['name']
        description = data['description']
        response = create_app(app_name, description)
        
        return jsonify({
            "success": True,
            "response": response,
            "app_name": app_name
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/tasks/add', methods=['POST'])
def add_task_endpoint():
    """Add a task"""
    try:
        data = request.get_json()
        if not data or 'task' not in data:
            return jsonify({"error": "No task description provided"}), 400
        
        task = data['task']
        response = think(f"add task: {task}")
        
        return jsonify({
            "success": True,
            "response": response,
            "task": task
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/tasks/list', methods=['GET'])
def list_tasks_endpoint():
    """List tasks"""
    try:
        response = think("list tasks")
        
        return jsonify({
            "success": True,
            "response": response
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/system/run', methods=['POST'])
def run_command_endpoint():
    """Run a system command"""
    try:
        data = request.get_json()
        if not data or 'command' not in data:
            return jsonify({"error": "No command provided"}), 400
        
        command = data['command']
        response = think(f"run: {command}")
        
        return jsonify({
            "success": True,
            "response": response,
            "command": command
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/memory/search', methods=['POST'])
def search_memory_endpoint():
    """Search memory for relevant conversations"""
    try:
        data = request.get_json()
        if not data or 'query' not in data:
            return jsonify({"error": "No search query provided"}), 400
        
        query = data['query']
        limit = data.get('limit', 5)
        results = nova_memory.recall_conversation(query, limit)
        
        return jsonify({
            "success": True,
            "results": results,
            "query": query,
            "count": len(results)
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/memory/store', methods=['POST'])
def store_memory_endpoint():
    """Store a conversation in memory"""
    try:
        data = request.get_json()
        if not data or 'user_input' not in data or 'nova_response' not in data:
            return jsonify({"error": "No user_input or nova_response provided"}), 400
        
        user_input = data['user_input']
        nova_response = data['nova_response']
        context = data.get('context', '')
        tags = data.get('tags', [])
        
        nova_memory.store_conversation(user_input, nova_response, context, tags)
        
        return jsonify({
            "success": True,
            "message": "Conversation stored in memory",
            "user_input": user_input
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/memory/summary', methods=['GET'])
def memory_summary_endpoint():
    """Get memory system summary"""
    try:
        summary = nova_memory.get_memory_summary()
        
        return jsonify({
            "success": True,
            "summary": summary
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/memory/preferences', methods=['GET'])
def get_preferences_endpoint():
    """Get user preferences"""
    try:
        user_id = request.args.get('user_id', 'jackson_alex')
        preferences = nova_memory.get_user_preferences(user_id)
        
        return jsonify({
            "success": True,
            "preferences": preferences,
            "user_id": user_id
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/memory/preferences', methods=['POST'])
def set_preferences_endpoint():
    """Set user preferences"""
    try:
        data = request.get_json()
        if not data or 'key' not in data or 'value' not in data:
            return jsonify({"error": "No key or value provided"}), 400
        
        key = data['key']
        value = data['value']
        user_id = data.get('user_id', 'jackson_alex')
        
        nova_memory.set_user_preference(key, value, user_id)
        
        return jsonify({
            "success": True,
            "message": "Preference set successfully",
            "key": key,
            "value": value,
            "user_id": user_id
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/status', methods=['GET'])
def status():
    """Check server status"""
    return jsonify({
        "status": "online",
        "nova_version": "Phase 6 - Advanced File Operations & AI Development",
        "capabilities": "File operations, app creation, task management, system commands, AI chat, memory management"
    })

if __name__ == '__main__':
    print("🚀 Starting NOVA API Server...")
    print("📡 Access NOVA from anywhere via HTTP requests!")
    print("🌐 Server will be available at: http://localhost:5000")
    print("📖 API Documentation available at: http://localhost:5000/")
    print("💡 Example: curl -X POST http://localhost:5000/chat -H 'Content-Type: application/json' -d '{\"message\": \"read file: main.py\"}'")
    
    app.run(host='0.0.0.0', port=5000, debug=True) 
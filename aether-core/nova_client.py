#!/usr/bin/env python3
"""
NOVA Client
Connect to NOVA from anywhere via HTTP
"""

import requests
import json
import sys
import os

class NovaClient:
    def __init__(self, server_url="http://localhost:5000"):
        self.server_url = server_url
        self.session = requests.Session()
    
    def _make_request(self, endpoint, data=None, method='POST'):
        """Make HTTP request to NOVA server"""
        url = f"{self.server_url}{endpoint}"
        
        try:
            if method == 'GET':
                response = self.session.get(url)
            else:
                response = self.session.post(url, json=data)
            
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": f"Connection failed: {str(e)}"}
        except json.JSONDecodeError:
            return {"error": "Invalid JSON response from server"}
    
    def chat(self, message):
        """Send a message to NOVA"""
        return self._make_request('/chat', {'message': message})
    
    def read_file(self, file_path):
        """Read a file"""
        return self._make_request('/files/read', {'path': file_path})
    
    def write_file(self, file_path, content):
        """Write to a file"""
        return self._make_request('/files/write', {'path': file_path, 'content': content})
    
    def edit_file(self, file_path, changes):
        """Edit a file with AI"""
        return self._make_request('/files/edit', {'path': file_path, 'changes': changes})
    
    def list_files(self, directory='.'):
        """List files in a directory"""
        return self._make_request('/files/list', {'directory': directory})
    
    def search_files(self, query, directory='.'):
        """Search files"""
        return self._make_request('/files/search', {'query': query, 'directory': directory})
    
    def create_app(self, name, description):
        """Create an application"""
        return self._make_request('/apps/create', {'name': name, 'description': description})
    
    def add_task(self, task):
        """Add a task"""
        return self._make_request('/tasks/add', {'task': task})
    
    def list_tasks(self):
        """List tasks"""
        return self._make_request('/tasks/list', method='GET')
    
    def run_command(self, command):
        """Run a system command"""
        return self._make_request('/system/run', {'command': command})
    
    def status(self):
        """Check server status"""
        return self._make_request('/status', method='GET')

def main():
    """Interactive NOVA client"""
    import argparse
    
    parser = argparse.ArgumentParser(description='NOVA Client - Connect to NOVA from anywhere')
    parser.add_argument('--server', default='http://localhost:5000', help='NOVA server URL')
    parser.add_argument('--command', help='Single command to execute')
    parser.add_argument('--file', help='Read file')
    parser.add_argument('--list', help='List files in directory')
    parser.add_argument('--search', help='Search files')
    parser.add_argument('--create-app', nargs=2, metavar=('NAME', 'DESCRIPTION'), help='Create app')
    parser.add_argument('--run', help='Run system command')
    parser.add_argument('--add-task', help='Add task')
    parser.add_argument('--list-tasks', action='store_true', help='List tasks')
    parser.add_argument('--status', action='store_true', help='Check server status')
    
    args = parser.parse_args()
    
    nova = NovaClient(args.server)
    
    # Check status first
    status = nova.status()
    if 'error' in status:
        print(f"❌ Cannot connect to NOVA server at {args.server}")
        print(f"Error: {status['error']}")
        print("\nMake sure NOVA API server is running:")
        print("python nova_api_server.py")
        return
    
    print(f"✅ Connected to NOVA at {args.server}")
    
    # Handle single commands
    if args.command:
        result = nova.chat(args.command)
        print(result.get('response', result.get('error', 'Unknown response')))
        return
    
    if args.file:
        result = nova.read_file(args.file)
        print(result.get('response', result.get('error', 'Unknown response')))
        return
    
    if args.list:
        result = nova.list_files(args.list)
        print(result.get('response', result.get('error', 'Unknown response')))
        return
    
    if args.search:
        result = nova.search_files(args.search)
        print(result.get('response', result.get('error', 'Unknown response')))
        return
    
    if args.create_app:
        name, description = args.create_app
        result = nova.create_app(name, description)
        print(result.get('response', result.get('error', 'Unknown response')))
        return
    
    if args.run:
        result = nova.run_command(args.run)
        print(result.get('response', result.get('error', 'Unknown response')))
        return
    
    if args.add_task:
        result = nova.add_task(args.add_task)
        print(result.get('response', result.get('error', 'Unknown response')))
        return
    
    if args.list_tasks:
        result = nova.list_tasks()
        print(result.get('response', result.get('error', 'Unknown response')))
        return
    
    if args.status:
        result = nova.status()
        print(json.dumps(result, indent=2))
        return
    
    # Interactive mode
    print("\n🤖 NOVA Client - Interactive Mode")
    print("Type 'help' for commands, 'exit' to quit")
    print("=" * 50)
    
    while True:
        try:
            command = input("\n🧠 NOVA> ").strip()
            
            if not command:
                continue
            
            if command.lower() in ['exit', 'quit', 'q']:
                print("👋 Goodbye!")
                break
            
            if command.lower() == 'help':
                print("""
🤖 NOVA Commands:
- read file: path
- write file: path | content  
- edit file: path | changes
- list files [directory]
- search files: query
- create app: name | description
- run: command
- add task: description
- list tasks
- status
- exit
                """)
                continue
            
            # Send command to NOVA
            result = nova.chat(command)
            response = result.get('response', result.get('error', 'Unknown response'))
            print(f"\n🤖 NOVA: {response}")
            
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == '__main__':
    main() 
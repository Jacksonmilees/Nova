# NOVA Memory System - Phase 7+
# Persistent Memory & Learning Engine
# Architect: Jackson Alex

import json
import datetime
import sqlite3
import hashlib
from pathlib import Path
from typing import Dict, List, Optional, Any
import pickle
import os

class NovaMemory:
    def __init__(self, memory_dir: str = "memory"):
        self.memory_dir = Path(memory_dir)
        self.memory_dir.mkdir(exist_ok=True)
        self.db_path = self.memory_dir / "nova_memory.db"
        self.conversations_path = self.memory_dir / "conversations.json"
        self.learning_path = self.memory_dir / "learning_data.json"
        self.identity_path = Path("config/identity.txt")
        
        self._init_database()
        self._load_conversations()
        self._load_learning_data()
        self._load_identity()
    
    def _init_database(self):
        """Initialize SQLite database for structured memory"""
        conn = sqlite3.connect(str(self.db_path))
        cursor = conn.cursor()
        
        # Conversations table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS conversations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT,
                timestamp TEXT,
                user_input TEXT,
                nova_response TEXT,
                context TEXT,
                memory_tags TEXT
            )
        ''')
        
        # Learning patterns table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS learning_patterns (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                pattern_type TEXT,
                pattern_data TEXT,
                frequency INTEGER DEFAULT 1,
                last_used TEXT,
                success_rate REAL DEFAULT 0.0
            )
        ''')
        
        # User preferences table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_preferences (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT,
                preference_key TEXT,
                preference_value TEXT,
                timestamp TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def _load_conversations(self):
        """Load conversation history"""
        if self.conversations_path.exists():
            try:
                with open(self.conversations_path, 'r', encoding='utf-8') as f:
                    self.conversations = json.load(f)
            except:
                self.conversations = []
        else:
            self.conversations = []
    
    def _load_learning_data(self):
        """Load learning patterns and preferences"""
        if self.learning_path.exists():
            try:
                with open(self.learning_path, 'r', encoding='utf-8') as f:
                    self.learning_data = json.load(f)
            except:
                self.learning_data = {"patterns": {}, "preferences": {}}
        else:
            self.learning_data = {"patterns": {}, "preferences": {}}
    
    def _load_identity(self):
        """Load NOVA identity information"""
        if self.identity_path.exists():
            try:
                with open(self.identity_path, 'r', encoding='utf-8') as f:
                    self.identity = f.read()
            except Exception as e:
                self.identity = "NOVA - Neural Operational Virtual Assistant"
                print(f"Error loading identity: {e}")
        else:
            self.identity = "NOVA - Neural Operational Virtual Assistant"
    
    def get_identity(self) -> str:
        """Get NOVA's identity information"""
        return self.identity
    
    def get_architect_info(self) -> Dict[str, Any]:
        """Extract architect information from identity"""
        architect_info = {
            "name": "Jackson Alex",
            "age": 22,
            "origin": "Kenya 🇰🇪",
            "academic_training": "BSc in Computer Science from Jomo Kenyatta University of Agriculture and Technology (JKUAT)",
            "disciplines": ["Artificial Intelligence", "Distributed Systems", "Full-Stack Engineering", "Applied Automation"],
            "titles": [
                "Founder & CEO, ImaraBuildor",
                "Founder, ImaraSend (Smart logistics & intelligent delivery systems)",
                "Visionary behind FundiSmart, HandyFix, and Nova Core Unit Series"
            ],
            "credentials": [
                "Builder of AI ecosystems that persist, self-learn, and operate cross-platform",
                "Architect of digital systems that remove friction between humans and machines",
                "Speaks code fluently — from backend logic to frontend UX flow",
                "Has designed platforms with integrated M-Pesa Push APIs, PayPal, LangChain, Firebase, Gemini, and GPT architectures",
                "Developer of server-grade tools deployed on Contabo, with local/remote AI control capability",
                "Uses Flutter, Python, React Native, MySQL, and cloud-native stacks to create AI-aware environments"
            ]
        }
        return architect_info
    
    def get_nova_purpose(self) -> Dict[str, Any]:
        """Get NOVA's purpose and capabilities"""
        purpose = {
            "core_nature": "thinking system",
            "vision": "eliminate repetitive interaction, fragmented workflows, and static logic trees",
            "capabilities": [
                "speak, observe, learn",
                "multi-agent system communication",
                "OS-level access",
                "internet-level intelligence", 
                "cloud-level persistence",
                "agent-level collaboration"
            ],
            "growth_methods": ["remembering", "adapting", "deciding"],
            "authorization": "respond only to Jackson Alex unless otherwise assigned by elevated directive"
        }
        return purpose
    
    def refresh_identity(self):
        """Refresh identity information from file"""
        self._load_identity()
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get complete NOVA system status"""
        memory_summary = self.get_memory_summary()
        architect_info = self.get_architect_info()
        nova_purpose = self.get_nova_purpose()
        
        return {
            "system": {
                "name": "NOVA",
                "full_name": "Neural Operational Virtual Assistant",
                "unit": "Unit 001",
                "initiative": "Aether Core Initiative",
                "phase": "Phase 7+",
                "status": "Operational"
            },
            "architect": architect_info,
            "purpose": nova_purpose,
            "memory": memory_summary,
            "identity_loaded": self.identity_path.exists(),
            "timestamp": datetime.datetime.now().isoformat()
        }
    
    def store_conversation(self, user_input: str, nova_response: str, context: str = "", tags: Optional[List[str]] = None):
        """Store a conversation interaction"""
        session_id = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        timestamp = datetime.datetime.now().isoformat()
        
        # Store in database
        conn = sqlite3.connect(str(self.db_path))
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO conversations (session_id, timestamp, user_input, nova_response, context, memory_tags)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (session_id, timestamp, user_input, nova_response, context, json.dumps(tags or [])))
        conn.commit()
        conn.close()
        
        # Store in JSON for quick access
        conversation = {
            "session_id": session_id,
            "timestamp": timestamp,
            "user_input": user_input,
            "nova_response": nova_response,
            "context": context,
            "tags": tags or []
        }
        self.conversations.append(conversation)
        
        # Save to file
        with open(self.conversations_path, 'w', encoding='utf-8') as f:
            json.dump(self.conversations, f, indent=2, ensure_ascii=False)
        
        # Learn from this interaction
        self._learn_from_interaction(user_input, nova_response, context)
    
    def _learn_from_interaction(self, user_input: str, nova_response: str, context: str):
        """Learn patterns from interactions"""
        # Extract key patterns
        patterns = self._extract_patterns(user_input, nova_response)
        
        for pattern_type, pattern_data in patterns.items():
            if pattern_type not in self.learning_data["patterns"]:
                self.learning_data["patterns"][pattern_type] = []
            
            # Check if pattern already exists
            existing = [p for p in self.learning_data["patterns"][pattern_type] 
                       if p["data"] == pattern_data]
            
            if existing:
                existing[0]["frequency"] += 1
                existing[0]["last_used"] = datetime.datetime.now().isoformat()
            else:
                self.learning_data["patterns"][pattern_type].append({
                    "data": pattern_data,
                    "frequency": 1,
                    "last_used": datetime.datetime.now().isoformat(),
                    "success_rate": 0.8  # Initial success rate
                })
        
        # Save learning data
        with open(self.learning_path, 'w', encoding='utf-8') as f:
            json.dump(self.learning_data, f, indent=2, ensure_ascii=False)
    
    def _extract_patterns(self, user_input: str, nova_response: str) -> Dict[str, Any]:
        """Extract learning patterns from interaction"""
        patterns = {}
        
        # Command patterns
        if any(cmd in user_input.lower() for cmd in ["screenshot", "take screenshot"]):
            patterns["screenshot_commands"] = {
                "trigger": "screenshot",
                "response_type": "system_action",
                "context": "user wants screenshot"
            }
        
        # File operation patterns
        if any(op in user_input.lower() for op in ["read file", "write file", "edit file"]):
            patterns["file_operations"] = {
                "trigger": "file_operation",
                "response_type": "file_action",
                "context": "user wants file operation"
            }
        
        # System command patterns
        if any(cmd in user_input.lower() for cmd in ["run:", "run ", "explorer", "chrome"]):
            patterns["system_commands"] = {
                "trigger": "system_command",
                "response_type": "system_action",
                "context": "user wants system command"
            }
        
        return patterns
    
    def recall_conversation(self, query: str, limit: int = 5) -> List[Dict]:
        """Recall relevant conversations based on query"""
        relevant = []
        
        for conv in reversed(self.conversations[-100:]):  # Last 100 conversations
            relevance_score = self._calculate_relevance(query, conv["user_input"])
            if relevance_score > 0.3:  # Threshold for relevance
                conv["relevance_score"] = relevance_score
                relevant.append(conv)
        
        # Sort by relevance and return top results
        relevant.sort(key=lambda x: x["relevance_score"], reverse=True)
        return relevant[:limit]
    
    def _calculate_relevance(self, query: str, stored_input: str) -> float:
        """Calculate relevance score between query and stored input"""
        query_words = set(query.lower().split())
        stored_words = set(stored_input.lower().split())
        
        if not query_words or not stored_words:
            return 0.0
        
        intersection = query_words.intersection(stored_words)
        union = query_words.union(stored_words)
        
        return len(intersection) / len(union) if union else 0.0
    
    def get_user_preferences(self, user_id: str = "jackson_alex") -> Dict[str, Any]:
        """Get user preferences"""
        conn = sqlite3.connect(str(self.db_path))
        cursor = conn.cursor()
        cursor.execute('''
            SELECT preference_key, preference_value FROM user_preferences 
            WHERE user_id = ? ORDER BY timestamp DESC
        ''', (user_id,))
        
        preferences = {}
        for row in cursor.fetchall():
            key, value = row
            if key not in preferences:  # Get most recent value
                preferences[key] = value
        
        conn.close()
        return preferences
    
    def set_user_preference(self, key: str, value: str, user_id: str = "jackson_alex"):
        """Set user preference"""
        conn = sqlite3.connect(str(self.db_path))
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO user_preferences (user_id, preference_key, preference_value, timestamp)
            VALUES (?, ?, ?, ?)
        ''', (user_id, key, value, datetime.datetime.now().isoformat()))
        conn.commit()
        conn.close()
    
    def get_learning_patterns(self, pattern_type: Optional[str] = None) -> Dict[str, Any]:
        """Get learning patterns"""
        if pattern_type:
            return self.learning_data["patterns"].get(pattern_type, [])
        return self.learning_data["patterns"]
    
    def get_memory_summary(self) -> Dict[str, Any]:
        """Get memory system summary"""
        conn = sqlite3.connect(str(self.db_path))
        cursor = conn.cursor()
        
        # Get conversation count
        cursor.execute('SELECT COUNT(*) FROM conversations')
        conversation_count = cursor.fetchone()[0]
        
        # Get recent activity
        cursor.execute('''
            SELECT COUNT(*) FROM conversations 
            WHERE timestamp > datetime('now', '-7 days')
        ''')
        recent_activity = cursor.fetchone()[0]
        
        conn.close()
        
        return {
            "nova_identity": "Neural Operational Virtual Assistant - Unit 001",
            "phase": "Phase 7+",
            "architect": "Jackson Alex",
            "total_conversations": conversation_count,
            "recent_activity_7_days": recent_activity,
            "learning_patterns": len(self.learning_data["patterns"]),
            "user_preferences": len(self.get_user_preferences()),
            "identity_loaded": self.identity_path.exists(),
            "memory_persistence": True
        }

# Initialize global memory instance
nova_memory = NovaMemory() 
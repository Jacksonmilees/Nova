#!/usr/bin/env python3
import requests
import time

def test_ollama_api():
    """Test the Ollama API connection"""
    print("🧪 Testing Ollama API connection...")
    
    try:
        # Test with a simple message
        response = requests.post(
            "http://164.68.118.21:5001",
            json={"message": "Hello, this is a test"},
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Ollama API is working!")
            print(f"Response: {data.get('response', 'No response')}")
            return True
        else:
            print(f"❌ API Error: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except requests.exceptions.Timeout:
        print("❌ Connection timed out - Ollama may be loading or busy")
        return False
    except requests.exceptions.ConnectionError:
        print("❌ Connection failed - Flask server may not be running")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_nova_ollama():
    """Test NOVA's Ollama integration"""
    print("\n🧠 Testing NOVA's Ollama integration...")
    
    try:
        # Test the ask local: functionality
        response = requests.post(
            "http://164.68.118.21:8000/api/think",
            json={"prompt": "ask local: What is 2+2?"},
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            print("✅ NOVA Ollama integration is working!")
            print(f"Response: {data.get('response', 'No response')}")
            return True
        else:
            print(f"❌ NOVA API Error: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ NOVA test failed: {e}")
        return False

if __name__ == "__main__":
    print("🔍 Ollama Status Check")
    print("=" * 40)
    
    # Test 1: Direct Ollama API
    ollama_ok = test_ollama_api()
    
    # Test 2: NOVA Integration
    nova_ok = test_nova_ollama()
    
    print("\n📊 Summary:")
    print(f"Ollama API: {'✅ Working' if ollama_ok else '❌ Failed'}")
    print(f"NOVA Integration: {'✅ Working' if nova_ok else '❌ Failed'}")
    
    if ollama_ok and nova_ok:
        print("\n🎉 Everything is working! You can now use 'ask local:' commands.")
    else:
        print("\n⚠️ Some components need attention. Check the logs above.") 
import json
from pathlib import Path

VAULT_PATH = Path(__file__).resolve().parent / ".vault.json"

def load_vault():
    if not VAULT_PATH.exists():
        return {}
    with open(VAULT_PATH, "r") as f:
        return json.load(f)

def get_secret(key):
    secrets = load_vault()
    return secrets.get(key, None) 
import json
from pathlib import Path

def get_secret(key):
    path = Path(__file__).resolve().parent / "keys.json"
    if not path.exists():
        raise FileNotFoundError("vault/keys.json not found.")
    with open(path, "r") as f:
        secrets = json.load(f)
    return secrets.get(key) 
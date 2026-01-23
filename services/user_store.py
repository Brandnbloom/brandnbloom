import json
from pathlib import Path

DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)

USERS_FILE = DATA_DIR / "users.json"

def _load_users():
    if USERS_FILE.exists():
        return json.loads(USERS_FILE.read_text())
    return {}

def _save_users(users):
    USERS_FILE.write_text(json.dumps(users, indent=2))

def create_user(name, email):
    users = _load_users()
    user_id = email.lower()
    if user_id in users:
        return user_id  # already exists
    users[user_id] = {"name": name, "email": email}
    _save_users(users)
    return user_id

def get_user(user_id):
    users = _load_users()
    return users.get(user_id)

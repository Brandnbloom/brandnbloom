import json
from datetime import datetime
from pathlib import Path

DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)

def _file(user_id):
    return DATA_DIR / f"{user_id}_insights.json"

def save_insight(user_id, tool, data):
    record = {
        "tool": tool,
        "data": data,
        "timestamp": datetime.utcnow().isoformat()
    }

    file = _file(user_id)

    if file.exists():
        existing = json.loads(file.read_text())
    else:
        existing = []

    existing.append(record)
    file.write_text(json.dumps(existing, indent=2))

def load_insights(user_id):
    file = _file(user_id)
    if not file.exists():
        return []
    return json.loads(file.read_text())



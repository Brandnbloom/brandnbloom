import json
import os

DATA_FILE = "data/brand_insights.json"

def save_insights(insights):
    os.makedirs("data", exist_ok=True)
    with open(DATA_FILE, "w") as f:
        json.dump(insights, f)

def load_insights():
    if not os.path.exists(DATA_FILE):
        return None
    with open(DATA_FILE, "r") as f:
        return json.load(f)

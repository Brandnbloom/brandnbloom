import json
import os

DATA_DIR = "data"
DATA_FILE = os.path.join(DATA_DIR, "brand_insights.json")


def _ensure_data_file():
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)

    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, "w") as f:
            json.dump({}, f)


def load_insights():
    _ensure_data_file()
    with open(DATA_FILE, "r") as f:
        return json.load(f)


def save_insights(tool_name, insights):
    _ensure_data_file()

    data = load_insights()
    data[tool_name] = insights

    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

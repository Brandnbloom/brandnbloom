# Utility functions for usage tracking
import json
from pathlib import Path

# Store usage in a JSON file
USAGE_FILE = Path("usage.json")

# Load or create empty usage file
def load_usage():
    if USAGE_FILE.exists():
        with open(USAGE_FILE, "r") as f:
            return json.load(f)
    return {}

# Save usage to file
def save_usage(data):
    with open(USAGE_FILE, "w") as f:
        json.dump(data, f)

# Check if user can use the tool (3 free tries)
def can_use_tool(user_email):
    usage = load_usage()
    count = usage.get(user_email, 0)
    return count < 3, 3 - count

# Increase usage count
def increment_usage(user_email):
    usage = load_usage()
    usage[user_email] = usage.get(user_email, 0) + 1
    save_usage(usage)

import json
import os

# File to store usage tracking
USAGE_FILE = "usage.json"

# Load existing usage data or create new file
def load_usage():
    if not os.path.exists(USAGE_FILE):
        with open(USAGE_FILE, "w") as f:
            json.dump({}, f)
    with open(USAGE_FILE, "r") as f:
        return json.load(f)

# Save updated usage data
def save_usage(data):
    with open(USAGE_FILE, "w") as f:
        json.dump(data, f, indent=2)

# Check if user can still use the tool (limit: 3)
def can_use_tool(email):
    usage_data = load_usage()
    if email not in usage_data:
        usage_data[email] = 0
    return usage_data[email] < 3

# Increase usage count by 1
def increment_usage(email):
    usage_data = load_usage()
    usage_data[email] = usage_data.get(email, 0) + 1
    save_usage(usage_data)

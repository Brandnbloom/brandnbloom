import datetime

INSIGHTS_DB = {}  # later this becomes real DB

def save_insight(user_id, tool, data):
    entry = {
        "tool": tool,
        "data": data,
        "timestamp": datetime.datetime.utcnow().isoformat()
    }

    INSIGHTS_DB.setdefault(user_id, []).append(entry)
    return entry

def get_insights(user_id):
    return INSIGHTS_DB.get(user_id, [])

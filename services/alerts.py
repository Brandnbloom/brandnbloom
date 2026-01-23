from services.storage import load_insights

def check_alert():
    data = load_insights()
    if not data:
        return None

    if data["negative"] >= 0.3 * data["total"]:
        return "⚠️ High negative sentiment detected"
    return None

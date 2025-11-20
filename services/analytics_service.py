# services/analytics_service.py

from db import get_session
from models import Event
from sqlmodel import text
from datetime import datetime
import pandas as pd
import json

# PDF generation (optional)
try:
    import pdfkit
    PDF_ENABLED = True
except Exception:
    PDF_ENABLED = False


# -----------------------------------
# 1. AGGREGATE METRICS
# -----------------------------------
def aggregate_metrics(q: dict = None):
    """
    Aggregate basic counts of events by type.
    Returns: {"summary": [{"type": "...", "cnt": N}, ...]}
    """
    with get_session() as s:
        rows = s.exec(
            text("SELECT type, COUNT(*) AS cnt FROM event GROUP BY type")
        ).all()
        results = [{"type": r[0], "count": r[1]} for r in rows]
        return {"summary": results}


# -----------------------------------
# 2. PDF REPORT
# -----------------------------------
def generate_pdf_report():
    """Generate a simple PDF analytics report."""
    html = f"""
    <h1>Analytics Report</h1>
    <p>Generated at: {datetime.utcnow().isoformat()}</p>
    """

    pdf_path = "/tmp/analytics_report.pdf"

    if not PDF_ENABLED:
        return {
            "error": "pdfkit not installed",
            "html": html,
            "pdf_path": None
        }

    pdfkit.from_string(html, pdf_path)
    return {
        "pdf_path": pdf_path,
        "html": html
    }


# -----------------------------------
# 3. ALERTS (In-Memory)
# -----------------------------------
alerts_store = []


def list_alerts():
    return alerts_store


def create_alert(payload: dict):
    alerts_store.append({
        "id": len(alerts_store) + 1,
        "payload": payload,
        "created_at": datetime.utcnow().isoformat()
    })
    return {"ok": True}


# -----------------------------------
# 4. EVENT ANALYTICS (User-level)
# -----------------------------------

# In-memory analytics store
analytics_db = {}


def log_event(user_id: int, event_name: str, value: float):
    """
    Logs a user analytics event.
    Stored in a simple in-memory dict.
    """
    if user_id not in analytics_db:
        analytics_db[user_id] = []

    event = {
        "event_name": event_name,
        "value": float(value),
        "timestamp": datetime.utcnow().isoformat()
    }

    analytics_db[user_id].append(event)
    return event


def get_user_analytics(user_id: int):
    """Returns user analytics list."""
    return analytics_db.get(user_id, [])


# -----------------------------------
# 5. USER ANALYTICS REPORT
# -----------------------------------
def generate_user_analytics_report(user_id: int):
    """
    Returns a JSON analytics report for a user.
    """
    events = analytics_db.get(user_id, [])

    total_value = sum(e["value"] for e in events)
    total_events = len(events)

    return {
        "user_id": user_id,
        "total_events": total_events,
        "total_value": total_value,
        "events": events,
    }

# services/analytics_service.py
from db import get_session
from models import Event
import pandas as pd
import json
import pdfkit
from datetime import datetime

def aggregate_metrics(q):
    # For demo, return counts from Event table
    with get_session() as s:
        rows = s.exec("SELECT type, COUNT(*) as cnt FROM event GROUP BY type").all()
        return {"summary": rows}

def generate_report(q):
    # q: {since, until, format}
    # Demo: produce a simple HTML -> PDF
    html = f"<h1>Report</h1><p>Generated at {datetime.utcnow().isoformat()}</p>"
    pdf_path = "/tmp/report.pdf"
    pdfkit.from_string(html, pdf_path)
    return {"report_path": pdf_path}

alerts_store = []

def list_alerts():
    return alerts_store

def create_alert(payload):
    alerts_store.append(payload)
    return {"ok": True}

# Simulated in-memory data; replace with DB queries in production
analytics_db = {}

def log_event(user_id: int, event_name: str, value: float):
    if user_id not in analytics_db:
        analytics_db[user_id] = []
    event = {"event_name": event_name, "value": value}
    analytics_db[user_id].append(event)
    return event

def get_user_analytics(user_id: int):
    return analytics_db.get(user_id, [])

def generate_report(user_id: int):
    events = analytics_db.get(user_id, [])
    total = sum(e["value"] for e in events)
    report = {
        "total_events": len(events),
        "total_value": total,
        "events": events
    }
    return report

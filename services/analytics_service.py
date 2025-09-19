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

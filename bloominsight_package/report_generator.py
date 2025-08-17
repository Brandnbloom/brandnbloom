from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from db import Database
import os
import io
from datetime import datetime

def create_weekly_pdf(username, out_path="reports/report.pdf"):
    db = Database(os.environ.get("DATABASE_PATH","data/bloominsight.db"))
    rows = db.get_history(username, limit=20)
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    c = canvas.Canvas(out_path, pagesize=A4)
    width, height = A4
    c.setFont("Helvetica-Bold", 16)
    c.drawString(40, height-60, f"BloomInsight Weekly Audit - {username}")
    y = height-100
    for fetched_at, profile_json, posts_json in rows[:8]:
        c.setFont("Helvetica", 9)
        c.drawString(40, y, f"Snapshot at: {fetched_at}")
        y -= 14
        if y < 120:
            c.showPage()
            y = height-80
    c.save()
    return out_path

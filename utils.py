import os
import json
import streamlit as st
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import smtplib

USAGE_LIMIT = 3
USAGE_FILE = "usage.json"

def load_usage():
    if not os.path.exists(USAGE_FILE):
        return {}
    with open(USAGE_FILE, "r") as f:
        return json.load(f)

def save_usage(usage):
    with open(USAGE_FILE, "w") as f:
        json.dump(usage, f, indent=4)

def can_use_tool(user_email, tool_name):
    usage = load_usage() 
    count = usage.get(tool_name, 0)
    return count < 3

def increment_usage(user_email, tool_name):
    usage = load_usage()
    if user_email not in usage:
        usage[user_email] = {}
    if tool_name not in usage[user_email]:
        usage[user_email][tool_name] = 0
    usage[user_email][tool_name] += 1
    save_usage(usage)

def send_email_with_pdf(subject, recipient, content):
    msg = MIMEMultipart()
    msg["From"] = os.getenv("EMAIL_USER")
    msg["To"] = recipient
    msg["Subject"] = subject

    body = MIMEText("Hi,\n\nPlease find your AI-generated report attached.\n\nRegards,\nTeam Brand n Bloom", "plain")
    msg.attach(body)

    # ✅ Generate PDF
    pdf_path = "report.pdf"
    c = canvas.Canvas(pdf_path, pagesize=letter)
    width, height = letter
    lines = content.split("\n")
    y = height - 50
    for line in lines:
        c.drawString(50, y, line.strip())
        y -= 15
        if y < 50:
            c.showPage()
            y = height - 50
    c.save()

    with open(pdf_path, "rb") as f:
        part = MIMEApplication(f.read(), Name="report.pdf")
        part["Content-Disposition"] = 'attachment; filename="report.pdf"'
        msg.attach(part)

    try:
        with smtplib.SMTP_SSL("smtp.zoho.in", 465) as server:
            server.login(os.getenv("EMAIL_USER"), os.getenv("EMAIL_PASS"))
            server.send_message(msg)
        st.success("📧 Report sent to your email!")
    except Exception as e:
        st.error(f"Email failed: {e}")

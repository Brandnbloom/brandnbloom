import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import streamlit as st

USAGE_FILE = "usage_counts.txt"

def can_use_tool(tool_name):
    if not os.path.exists(USAGE_FILE):
        return True
    with open(USAGE_FILE, "r") as f:
        for line in f:
            name, count = line.strip().split(":")
            if name == tool_name and int(count) >= 3:
                return False
    return True

def increment_usage(tool_name):
    counts = {}
    if os.path.exists(USAGE_FILE):
        with open(USAGE_FILE, "r") as f:
            for line in f:
                name, count = line.strip().split(":")
                counts[name] = int(count)
    counts[tool_name] = counts.get(tool_name, 0) + 1
    with open(USAGE_FILE, "w") as f:
        for name, count in counts.items():
            f.write(f"{name}:{count}\n")

def send_email_with_pdf(subject, recipient, content):
    msg = MIMEMultipart()
    msg["From"] = os.getenv("EMAIL_USER")
    msg["To"] = recipient
    msg["Subject"] = subject

    body = MIMEText("Hi,\n\nPlease find your AI-generated report attached.\n\nRegards,\nTeam Brand n Bloom", "plain")
    msg.attach(body)

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

    try:
        with smtplib.SMTP_SSL("smtp.zoho.in", 465) as server:
            server.login(os.getenv("EMAIL_USER"), os.getenv("EMAIL_PASS"))
            server.send_message(msg)
        st.success("📧 Report sent to your email!")
    except Exception as e:
        st.error(f"Email failed: {e}")

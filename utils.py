import json
import os
import streamlit as st
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

# ---------- USAGE LIMIT FUNCTIONS ----------
USAGE_FILE = "usage.json"
MAX_FREE_USES = 3

def load_usage():
    if os.path.exists(USAGE_FILE):
        with open(USAGE_FILE, "r") as f:
            return json.load(f)
    return {}

def save_usage(data):
    with open(USAGE_FILE, "w") as f:
        json.dump(data, f)

def can_use_tool(tool_name):
    usage = load_usage()
    user_ip = st.session_state.get("user_ip", st.experimental_get_query_params().get("ip", ["anon"])[0])
    count = usage.get(user_ip, {}).get(tool_name, 0)
    return count < MAX_FREE_USES

def increment_usage(tool_name):
    usage = load_usage()
    user_ip = st.session_state.get("user_ip", st.experimental_get_query_params().get("ip", ["anon"])[0])
    if user_ip not in usage:
        usage[user_ip] = {}
    usage[user_ip][tool_name] = usage[user_ip].get(tool_name, 0) + 1
    save_usage(usage)

# ---------- STRIPE PLACEHOLDER ----------
def show_stripe_buttons():
    st.warning("🔒 You've reached the limit of 3 free uses for this tool.")
    st.markdown("""
    #### 🚀 Unlock Unlimited Access
    - $5/month 🌱
    - $50/year 🌸
    
    *Payment options coming soon.*
    """)

    st.button("🔁 Try Again Later")

# ---------- EMAIL WITH PDF ----------
def send_email_with_pdf(subject, recipient, content):
    msg = MIMEMultipart()
    msg["From"] = os.getenv("EMAIL_USER")
    msg["To"] = recipient
    msg["Subject"] = subject

    body = MIMEText("Hi,\n\nPlease find your AI-generated report attached.\n\nRegards,\nTeam Brand n Bloom", "plain")
    msg.attach(body)

    # Create PDF with reportlab
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

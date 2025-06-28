import json
import os
import streamlit as st
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import streamlit as st


# ----- Usage Tracker -----
USAGE_FILE = "usage.json"

def load_usage():
    if os.path.exists(USAGE_FILE):
        with open(USAGE_FILE, "r") as f:
            return json.load(f)
    return {}

def save_usage(usage_data):
    with open(USAGE_FILE, "w") as f:
        json.dump(usage_data, f)

def can_use_tool(tool_name):
    usage = load_usage()
    count = usage.get(tool_name, 0)
    return count < 3

def increment_usage(tool_name):
    usage = load_usage()
    usage[tool_name] = usage.get(tool_name, 0) + 1
    save_usage(usage)

# ----- Stripe Button -----
def show_stripe_buttons():
    st.warning("🔒 Free limit reached. Please subscribe to continue.")
    st.markdown("💳 $5/month or $50/year to unlock unlimited access.")
    st.link_button("Subscribe Monthly", "https://buy.stripe.com/test_xyz123month")
    st.link_button("Subscribe Yearly", "https://buy.stripe.com/test_abc456year")

# ----- Email PDF -----
def send_email_with_pdf(subject, recipient, content):
    msg = MIMEMultipart()
    msg["From"] = os.getenv("EMAIL_USER")
    msg["To"] = recipient
    msg["Subject"] = subject

    body = MIMEText("Hi,\n\nPlease find your AI-generated report attached.\n\nRegards,\nTeam Brand n Bloom", "plain")
    msg.attach(body)

    pdf_path = "report.pdf"
    with open(pdf_path, "w") as f:
        f.write(content)

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

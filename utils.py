import os
import json
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import streamlit as st

# ---------- 📊 Usage Limit ----------
USAGE_FILE = "usage.json"

def load_usage():
    if os.path.exists(USAGE_FILE):
        with open(USAGE_FILE, "r") as f:
            return json.load(f)
    return {}

def save_usage(data):
    with open(USAGE_FILE, "w") as f:
        json.dump(data, f)

def can_use_tool(email):
    usage_data = load_usage()
    return usage_data.get(email, 0) < 3  # 3 free uses

def increment_usage(email):
    usage_data = load_usage()
    usage_data[email] = usage_data.get(email, 0) + 1
    save_usage(usage_data)

# ---------- 💌 Email with PDF ----------
def send_email_with_pdf(subject, recipient, content):
    msg = MIMEMultipart()
    msg["From"] = os.getenv("EMAIL_USER")
    msg["To"] = recipient
    msg["Subject"] = subject

    body = MIMEText("Hi,\n\nPlease find your AI-generated report attached.\n\nRegards,\nTeam Brand n Bloom", "plain")
    msg.attach(body)

    # ✅ Generate PDF from content
    pdf_path = "report.pdf"
    c = canvas.Canvas(pdf_path, pagesize=letter)
    width, height = letter
    y = height - 50
    for line in content.split("\n"):
        c.drawString(50, y, line.strip())
        y -= 15
        if y < 50:
            c.showPage()
            y = height - 50
    c.save()

    # ✅ Attach PDF
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
        st.error(f"❌ Email failed: {e}")

# ---------- 💳 Stripe Payment Option ----------
def show_stripe_buttons():
    st.info("⚠️ You’ve used your 3 free attempts. To continue, please subscribe.")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown(
            "[Subscribe Monthly – $5](https://buy.stripe.com/test_a1b2c3monthly)",  # Replace with real link
            unsafe_allow_html=True,
        )
    with col2:
        st.markdown(
            "[Subscribe Yearly – $50](https://buy.stripe.com/test_a1b2c3yearly)",   # Replace with real link
            unsafe_allow_html=True,
        )

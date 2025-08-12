import os
import smtplib
import json
import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import streamlit as st

USAGE_FILE = "usage_counts.txt"

# ✅ Styling
def apply_custom_css():
    st.markdown("""
        <style>
        html, body, [class*="css"] {
            font-family: 'Segoe UI', sans-serif;
            background-color: #FAF5FF;
        }
        .stApp {
            background-color: #ffffff;
            padding: 1rem;
        }
        h1, h2, h3 {
            color: #8A4FFF;
        }
        .css-1v3fvcr {  /* Sidebar title */
            color: #8A4FFF;
            font-weight: bold;
        }
        .stButton>button {
            background-color: #8A4FFF;
            color: white;
            border-radius: 8px;
            border: none;
            padding: 0.5rem 1rem;
        }
        .stButton>button:hover {
            background-color: #6D28D9;
        }
        </style>
    """, unsafe_allow_html=True)

# ✅ Tool cards layout
def responsive_cards_css():
    st.markdown("""
    <style>
    .tool-card-container {
        display: flex;
        flex-wrap: wrap;
        justify-content: space-between;
        gap: 20px;
    }
    .tool-card {
        background-color: #f8f3ff;
        border-radius: 12px;
        padding: 20px;
        width: 100%;
        max-width: 350px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
        flex: 1;
    }
    .tool-card:hover {
        transform: scale(1.02);
        background-color: #efe7fd;
    }
    @media (max-width: 768px) {
        .tool-card-container {
            flex-direction: column;
        }
    }
    </style>
    """, unsafe_allow_html=True)

# ✅ Old anonymous usage logic (optional fallback)
def can_use_tool_old(tool_name):
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

# ✅ Email report with PDF
def send_email_with_pdf(subject, recipient, content):
    msg = MIMEMultipart()
    msg["From"] = os.getenv("EMAIL_USER")
    msg["To"] = recipient
    msg["Subject"] = subject

    body = MIMEText(
        "Hi,\n\nPlease find your AI-generated report attached.\n\nRegards,\nTeam Brand n Bloom",
        "plain"
    )
    msg.attach(body)

    # Create PDF
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
        attachment = MIMEApplication(f.read(), _subtype="pdf")
        attachment.add_header('Content-Disposition', 'attachment', filename="report.pdf")
        msg.attach(attachment)

    try:
        with smtplib.SMTP_SSL("smtp.zoho.in", 465) as server:
            server.login(os.getenv("EMAIL_USER"), os.getenv("EMAIL_PASS"))
            server.send_message(msg)
        st.success("📧 Report sent to your email!")
    except Exception as e:
        st.error(f"Email failed: {e}")

# ✅ Load JSON usage data for per-user limits
def load_usage():
    if os.path.exists("usage_data.json"):
        with open("usage_data.json", "r") as f:
            return json.load(f)
    return {}

def save_usage(data):
    with open("usage_data.json", "w") as f:
        json.dump(data, f)

# ✅ Alert for high daily usage
def check_usage_and_alert():
    today = datetime.date.today().isoformat()
    usage_data = load_usage()
    total_today = sum(
        usage_data.get(tool, {}).get(today, {}).get(email, 0)
        for tool in usage_data
        for email in usage_data[tool].get(today, {})
    )

    if total_today > 50:
        subject = "🚨 Brand n Bloom High Traffic Alert"
        content = f"Hi Shreya,\n\nToday you had {total_today} total tool usages.\n\nCheck your analytics for insights.\n\n– Brand n Bloom Bot 🌸"
        send_alert_email(subject, content)

def send_alert_email(subject, content):
    msg = MIMEMultipart()
    msg["From"] = os.getenv("EMAIL_USER")
    msg["To"] = os.getenv("ALERT_EMAIL")
    msg["Subject"] = subject
    msg.attach(MIMEText(content, "plain"))

    try:
        with smtplib.SMTP_SSL("smtp.zoho.in", 465) as server:
            server.login(os.getenv("EMAIL_USER"), os.getenv("EMAIL_PASS"))
            server.send_message(msg)
        print("✅ Alert email sent")
    except Exception as e:
        print(f"❌ Failed to send alert: {e}")

# ✅ Subscription check
def is_subscribed_user(email):
    try:
        with open("subscribers.json", "r") as f:
            data = json.load(f)
            return email in data.get("subscribers", [])
    except:
        return False

# ✅ New per-user daily usage limit logic
def can_use_tool(email, tool_name):
    if is_subscribed_user(email):
        return True  # Unlimited for subscribed users

    usage_data = load_usage()
    today = datetime.date.today().isoformat()

    if tool_name not in usage_data:
        usage_data[tool_name] = {}

    if today not in usage_data[tool_name]:
        usage_data[tool_name][today] = {}

    if email not in usage_data[tool_name][today]:
        usage_data[tool_name][today][email] = 0

    return usage_data[tool_name][today][email] < 3

def increment_user_usage(email, tool_name):
    usage_data = load_usage()
    today = datetime.date.today().isoformat()

    usage_data.setdefault(tool_name, {}).setdefault(today, {}).setdefault(email, 0)
    usage_data[tool_name][today][email] += 1

    save_usage(usage_data)

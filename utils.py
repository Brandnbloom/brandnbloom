import os
import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from dotenv import load_dotenv
import requests

def get_instagram_data(username):
    api_url = f"https://myinstascraper.onrender.com/user/{username}"
    response = requests.get(api_url)
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": "Could not fetch data"}

# Load environment variables from .env file
load_dotenv()

# ------------- 1️⃣ USAGE TRACKER ----------------
# This will store how many times a tool was used
usage_file = "usage.json"

def _load_usage():
    """Reads the usage data from file, or creates an empty one if not present."""
    if not os.path.exists(usage_file):
        with open(usage_file, "w") as f:
            json.dump({}, f)
    with open(usage_file, "r") as f:
        return json.load(f)

def _save_usage(data):
    """Saves updated usage data back to file."""
    with open(usage_file, "w") as f:
        json.dump(data, f, indent=4)

def can_use_tool(user_email, tool_name):
    usage_data = get_usage_data(user_email)  # however you fetch it
    limit = get_tool_limit(tool_name)        # however you fetch the limit
    try:
        limit = int(limit)  # make sure limit is a number
    except ValueError:
        limit = 0           # if it's not a number, default to 0
    return usage_data.get(tool_name, 0) < limit

def increment_usage(tool_name):
    """
    Adds +1 to the usage count for a tool.
    """
    usage_data = _load_usage()
    usage_data[tool_name] = usage_data.get(tool_name, 0) + 1
    _save_usage(usage_data)

# ------------- 2️⃣ EMAIL SENDER ----------------
def send_email_with_pdf(to_email, subject, body, pdf_path):
    """
    Sends an email with a PDF attachment.
    Needs EMAIL_USER and EMAIL_PASS in .env file.
    """
    email_user = os.getenv("EMAIL_USER")
    email_pass = os.getenv("EMAIL_PASS")

    if not email_user or not email_pass:
        raise ValueError("EMAIL_USER and EMAIL_PASS must be set in .env")

    # Create email
    msg = MIMEMultipart()
    msg["From"] = email_user
    msg["To"] = to_email
    msg["Subject"] = subject

    # Add text body
    msg.attach(MIMEText(body, "plain"))

    # Attach PDF
    with open(pdf_path, "rb") as f:
        pdf_attachment = MIMEApplication(f.read(), _subtype="pdf")
        pdf_attachment.add_header("Content-Disposition", "attachment", filename=os.path.basename(pdf_path))
        msg.attach(pdf_attachment)

    # Send email
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(email_user, email_pass)
        server.send_message(msg)

    print(f"✅ Email sent to {to_email} with {pdf_path}")

# ------------- 3️⃣ HELPER FOR STATIC FILES ----------------
def inject_pwa_tags():
    """
    Injects PWA manifest & service worker tags into Streamlit HTML.
    Use in app.py → st.markdown(inject_pwa_tags(), unsafe_allow_html=True)
    """
    return """
    <link rel="manifest" href="manifest.json">
    <script>
      if ('serviceWorker' in navigator) {
        navigator.serviceWorker.register('service-worker.js')
          .then(() => console.log('Service Worker Registered'));
      }
    </script>
    """

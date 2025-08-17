# report_api.py
from flask import Flask, request, jsonify
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

from scraper import scrape_instagram_data
from report_generator import create_full_report_pdf

app = Flask(__name__)

# ----------------- EMAIL SETTINGS -----------------
EMAIL_SENDER = os.getenv("EMAIL_SENDER", "your_email@example.com")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD", "your_password")
EMAIL_RECEIVER = os.getenv("EMAIL_RECEIVER", "client_email@example.com")
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

# ----------------- EMAIL SENDER -----------------
def send_email_with_report(pdf_path):
    try:
        msg = MIMEMultipart()
        msg["From"] = EMAIL_SENDER
        msg["To"] = EMAIL_RECEIVER
        msg["Subject"] = "Weekly BloomInsight Instagram Report"

        body = "Hello,\n\nPlease find attached the latest Instagram analytics report.\n\nRegards,\nBloomInsight"
        msg.attach(MIMEText(body, "plain"))

        with open(pdf_path, "rb") as f:
            from email.mime.application import MIMEApplication
            part = MIMEApplication(f.read(), Name="Instagram_Report.pdf")
            part["Content-Disposition"] = 'attachment; filename="Instagram_Report.pdf"'
            msg.attach(part)

        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        server.sendmail(EMAIL_SENDER, EMAIL_RECEIVER, msg.as_string())
        server.quit()

        print("✅ Email sent successfully.")
    except Exception as e:
        print(f"❌ Error sending email: {e}")

# ----------------- REPORT BUILDER -----------------
def build_and_send_report():
    print("📊 Running scheduled report...")
    data = scrape_instagram_data()
    pdf_path = create_full_report_pdf(data)
    send_email_with_report(pdf_path)

# ----------------- FLASK ROUTE -----------------
@app.route("/send-reports", methods=["GET"])
def send_reports():
    build_and_send_report()
    return jsonify({"status": "Report generated and sent!"})

# ----------------- SCHEDULER -----------------
scheduler = BackgroundScheduler()
scheduler.add_job(build_and_send_report, "interval", weeks=1, next_run_time=datetime.now())
scheduler.start()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)

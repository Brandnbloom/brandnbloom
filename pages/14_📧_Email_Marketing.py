import streamlit as st
from utils.ui import inject_css, dark_mode_toggle
from emailer.mailer import send_email
from emailer.mailerlite_adapter import send_campaign

inject_css(); dark_mode_toggle()
st.title("📧 Automated Email Marketing")

recipient = st.text_input("Test recipient email")
subject = st.text_input("Subject", "Hello from Brand N Bloom")
html = st.text_area("HTML content", "<h3>Hi — this is a test</h3><p>Track performance</p>")
use_mailerlite = st.checkbox("Use MailerLite (requires API key)", value=False)
if st.button("Send Test"):
    if use_mailerlite:
        try:
            code, text = send_campaign(subject, html)
            st.success(f"MailerLite response: {code}")
            st.write(text)
        except Exception as e:
            st.error(str(e))
    else:
        try:
            send_email(recipient or "demo@example.com", subject, html)
            st.success("Email sent via SMTP (or simulated).")
        except Exception as e:
            st.error(str(e))

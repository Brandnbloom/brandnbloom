import streamlit as st
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

st.set_page_config(page_title="Contact Us - Brand n Bloom", layout="centered")

# 🌸 Page Title
st.title("📬 Contact Us")
st.markdown("We're here to help you bloom 🌸 — whether you have a question, a suggestion, or need support.")

# 🌿 Contact Form
with st.form("contact_form"):
    name = st.text_input("👤 Your Name")
    email = st.text_input("📧 Your Email")
    subject = st.text_input("📝 Subject")
    message = st.text_area("💬 Your Message")

    submitted = st.form_submit_button("Send Message")

    if submitted:
        if name and email and message:
            try:
                msg = MIMEMultipart()
                msg["From"] = os.getenv("EMAIL_USER")
                msg["To"] = os.getenv("EMAIL_USER")  # Send to yourself
                msg["Subject"] = f"New Contact Message from {name}: {subject}"

                body = f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}"
                msg.attach(MIMEText(body, "plain"))

                with smtplib.SMTP_SSL("smtp.zoho.in", 465) as server:
                    server.login(os.getenv("EMAIL_USER"), os.getenv("EMAIL_PASS"))
                    server.send_message(msg)

                st.success("✅ Your message has been sent successfully!")
            except Exception as e:
                st.error(f"❌ Failed to send message: {e}")
        else:
            st.warning("⚠️ Please fill out all fields.")

# 📍 (Optional) Google Map Embed
st.markdown("""
### 📍 Our Location
<iframe src="https://www.google.com/maps/embed?..." width="100%" height="250" style="border:0;" allowfullscreen="" loading="lazy"></iframe>
""", unsafe_allow_html=True)

# 🛡️ Add a meta tag if needed for SEO
st.markdown("""
<!-- Meta tag for SEO -->
<meta name="description" content="Contact Brand n Bloom - Get in touch with our AI branding team.">
""", unsafe_allow_html=True)

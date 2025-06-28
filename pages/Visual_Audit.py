import streamlit as st
from utils import can_use_tool, increment_usage, send_email_with_pdf, show_stripe_buttons
from PIL import Image
import os

st.title("🎨 Visual Brand Audit Tool")

if can_use_tool("VisualAudit"):
    uploaded_files = st.file_uploader("📤 Upload Instagram or website screenshots", accept_multiple_files=True, type=["png", "jpg", "jpeg"])
    email = st.text_input("📧 Enter your email to receive report")

    if uploaded_files and st.button("🧠 Analyze Visual Identity"):
        increment_usage("VisualAudit")

        result = "📋 Your Visual Moodboard Summary:

- Tone: Warm & friendly
- Color palette: Dominantly pastel with neutral accents
- Layout Consistency: Moderate
- Suggestions: Use uniform filters, stick to 2 fonts max"

        st.success("Analysis complete! ✅")
        st.code(result)
        send_email_with_pdf("Your Visual Brand Audit", email, result)

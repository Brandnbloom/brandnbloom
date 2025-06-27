import streamlit as st
import os
import openai
from utils import can_use_tool, increment_usage, show_stripe_buttons, send_email_with_pdf

# ✅ API Key Fallback
if "OPENROUTER_API_KEY" not in os.environ:
    st.error("❌ Missing environment variable: OPENROUTER_API_KEY")
    st.stop()
else:
    openai.api_key = os.environ["OPENROUTER_API_KEY"]

st.title("🌸 BloomScore – Brand Health Audit")

# ✅ Check Usage Limit
if not can_use_tool("bloomscore"):
    show_stripe_buttons()
    st.stop()

# ✅ Input Form
with st.form("bloomscore_form"):
    st.markdown("Enter your brand’s Instagram handles or website URLs:")
    brand1 = st.text_input("Brand 1", "")
    brand2 = st.text_input("Brand 2", "")
    brand3 = st.text_input("Brand 3", "")
    email = st.text_input("Your Email")
    submit = st.form_submit_button("Generate Report")

if submit and all([brand1, brand2, brand3, email]):
    with st.spinner("Generating your AI-powered brand score report..."):
        prompt = f"""
        Compare the following 3 restaurant brands based on their online presence.
        - Instagram or website link 1: {brand1}
        - Link 2: {brand2}
        - Link 3: {brand3}
        
        Provide insights in the following format:
        1. Content Themes
        2. Posting Frequency
        3. Hashtag Strategy
        4. Visual Tone
        5. Follower Quality
        6. Final Score out of 100 for each
        
        Return this in a short, clean summary format.
        """

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
        )

        ai_report = response.choices[0].message.content

        st.success("Report generated!")
        st.markdown(ai_report)

        # Send to email as PDF
        send_email_with_pdf(subject="🌸 BloomScore Report", recipient=email, content=ai_report)

        increment_usage("bloomscore")

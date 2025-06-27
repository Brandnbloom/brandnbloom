import streamlit as st
import os
import openai
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from utils import can_use_tool, increment_usage

# Streamlit config
st.set_page_config(page_title="🌸 BloomScore - Brand n Bloom", layout="wide")
st.title("🌸 BloomScore – Brand Audit Tool")

# OpenRouter setup
openai.api_base = "https://openrouter.ai/api/v1"
openai.api_key = os.environ["OPENROUTER_API_KEY"]

# PDF generator
def generate_pdf(text):
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter
    y = height - 40
    for line in text.split('\n'):
        if y < 40:
            pdf.showPage()
            y = height - 40
        pdf.drawString(40, y, line.strip())
        y -= 15
    pdf.save()
    buffer.seek(0)
    return buffer

# User form
with st.form("bloomscore_form"):
    insta_url = st.text_input("📷 Instagram Profile URL")
    website_url = st.text_input("🌐 Website URL")
    industry = st.selectbox("🍽️ Restaurant Type", ["Cafe", "Fine Dining", "Fast Food", "Cloud Kitchen", "Bakery", "Bar"])
    user_email = st.text_input("📧 Email (required to generate report)")
    submitted = st.form_submit_button("Generate BloomScore")

# Logic
if submitted:
    if not user_email:
        st.warning("⚠️ Please enter your email to continue.")
    elif not can_use_tool(user_email):
        st.error("❌ You’ve used your 3 free reports.")
        st.markdown("💳 [Click here to subscribe for unlimited access](https://buy.stripe.com/test_00g12345678abcdeEF)")
        st.info("₹400/month or ₹4000/year. UPI, Cards, Wallets accepted.")
    else:
        increment_usage(user_email)
        with st.spinner("🌿 Generating your BloomScore..."):
            prompt = f"""
You are a digital brand strategist.

Based on:
- Instagram: {insta_url}
- Website: {website_url}
- Industry: {industry}

Give:
1. First impressions
2. Instagram content & tone
3. Hashtag insights
4. UX estimation
5. Score out of 10
6. 3 brand improvement tips
"""
            try:
                response = openai.ChatCompletion.create(
                    model="openrouter/openai/gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are a brand audit expert."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.7
                )
                result = response.choices[0].message.content
                st.success("✅ BloomScore Ready!")
                st.markdown(result)

                pdf = generate_pdf(result)
                st.download_button("📄 Download PDF", pdf, "bloomscore.pdf", "application/pdf")

            except Exception as e:
                st.error(f"⚠️ Error: {e}")

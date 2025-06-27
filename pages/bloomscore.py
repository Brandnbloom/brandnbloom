import streamlit as st
import os
from openai import OpenAI
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# Streamlit config
st.set_page_config(page_title="🌸 BloomScore - Brand n Bloom", layout="wide")
st.title("🌸 BloomScore – Brand Audit Tool")
st.markdown("Enter your restaurant’s social media or website and let AI score your brand’s online presence.")

# OpenAI client setup
client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

# PDF Generator
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

# --- Form Input ---
with st.form("bloomscore_form"):
    insta_url = st.text_input("📷 Instagram Profile URL")
    website_url = st.text_input("🌐 Website URL")
    industry = st.selectbox("Restaurant Category", ["Fine Dining", "Cafe", "Fast Food", "Cloud Kitchen", "Bakery", "Bar"])
    user_email = st.text_input("📧 Your Email (optional for emailing report)")
    user_name = st.text_input("🧑‍🍳 Your Name (for personalization)", placeholder="Optional")
    submitted = st.form_submit_button("Generate BloomScore")

# --- GPT Analysis ---
if submitted:
    with st.spinner("Auditing your brand..."):
        prompt = f"""
You are a branding expert for hospitality businesses. Based on the following inputs:

- Instagram: {insta_url}
- Website: {website_url}
- Category: {industry}

Perform a full brand presence audit including:
1. First impression (consistency, logo, design)
2. Instagram content style (reels vs static, tone)
3. Use of hashtags and captions
4. Follower quality (assume public stats)
5. Website speed, UX, SEO structure (estimate)
6. Overall branding score (out of 10)
7. Actionable tips to improve

Format output in clean, easy-to-read points.
"""

        try:
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a digital brand strategist."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7
            )

            output = response.choices[0].message.content
            st.success("✅ BloomScore Audit Ready!")
            st.markdown("### 📋 Audit Summary:\n")
            st.markdown(output)

            pdf_buffer = generate_pdf(output)
            st.download_button(
                label="📄 Download BloomScore PDF",
                data=pdf_buffer,
                file_name="bloomscore_report.pdf",
                mime="application/pdf"
            )

        except Exception as e:
            st.error(f"⚠️ Error: {e}")

import streamlit as st
import os
from openai import OpenAI
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# Streamlit page config
st.set_page_config(page_title="🌸 BloomScore - Brand n Bloom", layout="wide")
st.title("🌸 BloomScore – Brand Audit Tool")
st.markdown("Enter your restaurant’s social media or website and let AI score your brand’s online presence.")

# OpenAI client
client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

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

# --- Input form ---
with st.form("bloomscore_form"):
    insta_url = st.text_input("📷 Instagram Profile URL")
    website_url = st.text_input("🌐 Website URL")
    industry = st.selectbox("Restaurant Category", ["Fine Dining", "Cafe", "Fast Food", "Cloud Kitchen", "Bakery", "Bar"])
    user_email = st.text_input("📧 Your Email (optional for emailing report)")
    user_name = st.text_input("🧑‍🍳 Your Name (for personalization)", placeholder="Optional")
    submitted = st.form_submit_button("Generate BloomScore")

# --- AI Audit Logic ---
if submitted:
    with st.spinner("Auditing your brand..."):
        prompt = f"""
You are a digital branding expert for restaurants.

Based on the following:

- Instagram: {insta_url}
- Website: {website_url}
- Category: {industry}

Give a complete brand presence audit, including:

1. First impression (logo, visuals, consistency)
2. Instagram content tone, format & hashtags
3. Follower quality (assume publicly available info)
4. Website usability, speed, and mobile experience (estimated)
5. Overall brand consistency and memorability
6. Final score out of 10 with reasoning
7. 3 quick action tips to improve visibility

Keep the tone friendly and actionable.
"""

        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",  # ✅ Updated model
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

            # PDF generation
            pdf_buffer = generate_pdf(output)
            st.download_button(
                label="📄 Download BloomScore PDF",
                data=pdf_buffer,
                file_name="bloomscore_report.pdf",
                mime="application/pdf"
            )

        except Exception as e:
            st.error(f"⚠️ Error: {e}")

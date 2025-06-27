import streamlit as st
import os
import openai
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# Streamlit page config
st.set_page_config(page_title="🌸 BloomScore - Brand n Bloom", layout="wide")
st.title("🌸 BloomScore – Brand Audit Tool")
st.markdown("Enter your restaurant’s social media or website and let AI score your brand’s online presence.")

# Use OpenRouter instead of OpenAI directly
openai.api_base = "https://openrouter.ai/api/v1"
openai.api_key = os.environ["OPENROUTER_API_KEY"]

# PDF generation function
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

# Input Form
with st.form("bloomscore_form"):
    insta_url = st.text_input("📷 Instagram Profile URL")
    website_url = st.text_input("🌐 Website URL")
    industry = st.selectbox("Restaurant Category", ["Fine Dining", "Cafe", "Fast Food", "Cloud Kitchen", "Bakery", "Bar"])
    user_email = st.text_input("📧 Your Email (optional)")
    user_name = st.text_input("🧑‍🍳 Your Name (optional)")
    submitted = st.form_submit_button("Generate BloomScore")

# Run audit
if submitted:
    with st.spinner("🌿 Auditing your digital brand presence..."):
        prompt = f"""
You are a digital brand strategist for restaurants.

Based on this data:
- Instagram: {insta_url}
- Website: {website_url}
- Category: {industry}

Provide:
1. First impression (logo, visuals, design consistency)
2. Instagram tone, content types & hashtag usage
3. Assumed follower quality (based on industry norm)
4. Estimated website UX & mobile performance
5. Overall branding memorability score out of 10
6. 3 actionable improvements

Use friendly, creative, and marketing-savvy language.
"""

        try:
            response = openai.ChatCompletion.create(
                model="openrouter/openai/gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a branding expert specializing in restaurants."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7
            )

            output = response.choices[0].message.content
            st.success("✅ BloomScore Report Ready!")
            st.markdown("### 🌼 Results:\n")
            st.markdown(output)

            # PDF
            pdf_buffer = generate_pdf(output)
            st.download_button(
                label="📄 Download BloomScore PDF",
                data=pdf_buffer,
                file_name="bloomscore_report.pdf",
                mime="application/pdf"
            )

        except Exception as e:
            st.error(f"⚠️ Error: {e}")

import streamlit as st
import os
from openai import OpenAI
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# Page setup
st.set_page_config(page_title="DinePsych AI - Brand n Bloom", layout="wide")
st.title("🧠 DinePsych AI — Behavioral Marketing Insights")
st.markdown("Let our AI analyze your ideal customer behavior & psychology to refine your restaurant's strategy.")

# OpenAI Client (new SDK)
client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

# PDF Generation Function
def generate_pdf(text):
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter
    y = height - 40
    for line in text.split('\n'):
        if y < 40:
            p.showPage()
            y = height - 40
        p.drawString(40, y, line.strip())
        y -= 15
    p.save()
    buffer.seek(0)
    return buffer

# --- Input Form ---
with st.form("behavior_form"):
    restaurant_type = st.selectbox("Type of Restaurant", ["Fine Dining", "Cafe", "Quick Service", "Cloud Kitchen", "Bar"])
    audience = st.text_input("Target Audience (e.g. Gen Z, Office-goers, Parents)")
    location = st.text_input("City / Area")
    aov = st.text_input("Avg Order Value (₹)", placeholder="e.g. 700")
    peak_hours = st.text_input("Peak Hours (e.g. 12-2pm, 7-10pm)")
    common_feedback = st.text_area("Common Customer Feedback Themes (Optional)")
    user_email = st.text_input("📧 Enter your email to receive the report (Optional)")
    user_name = st.text_input("🧑‍🍳 Your Name (for personalization)", placeholder="Optional")

    submitted = st.form_submit_button("Generate Insights")

# --- GPT + PDF Output ---
if submitted:
    with st.spinner("Analyzing customer psychology..."):
        prompt = f"""
You are a behavioral marketing strategist for restaurants.

Based on the following:

- Type of restaurant: {restaurant_type}
- Audience: {audience}
- Location: {location}
- Average order value: ₹{aov}
- Peak hours: {peak_hours}
- Feedback themes: {common_feedback}

Generate an in-depth analysis:
1. Ideal customer persona & emotional drivers
2. Marketing tone & style that appeals
3. Visual aesthetics for ads/menu
4. Instagram content suggestions
5. Promotions that would convert
"""

        try:
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are an expert in restaurant consumer psychology and marketing."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7
            )

            output = response.choices[0].message.content
            st.success("✅ Insights Ready!")
            st.markdown("### 📋 Results:\n")
            st.markdown(output)

            # Generate PDF + Download
            pdf_buffer = generate_pdf(output)
            st.download_button(
                label="📄 Download PDF Report",
                data=pdf_buffer,
                file_name="dinepsych_ai_report.pdf",
                mime="application/pdf"
            )

        except Exception as e:
            st.error(f"⚠️ Error: {e}")

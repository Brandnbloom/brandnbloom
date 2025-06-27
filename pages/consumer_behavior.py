import streamlit as st
import os
import openai
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# Set page config
st.set_page_config(page_title="DinePsych AI - Brand n Bloom", layout="wide")
st.title("🧠 DinePsych AI — Behavioral Marketing Tool")
st.markdown("Let AI decode your ideal customer's psychology and help optimize your strategy.")

# Use OpenRouter instead of OpenAI directly
openai.api_base = "https://openrouter.ai/api/v1"
openai.api_key = os.environ["OPENROUTER_API_KEY"]

# Function to generate a PDF from the output
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

# --- Input form ---
with st.form("behavior_form"):
    restaurant_type = st.selectbox("Type of Restaurant", ["Fine Dining", "Cafe", "Quick Service", "Cloud Kitchen", "Bar"])
    audience = st.text_input("Target Audience (e.g. Gen Z, Office-goers, Parents)")
    location = st.text_input("City / Area")
    aov = st.text_input("Avg Order Value (₹)", placeholder="e.g. 700")
    peak_hours = st.text_input("Peak Hours (e.g. 12-2pm, 7-10pm)")
    common_feedback = st.text_area("Common Customer Feedback Themes (Optional)")
    user_email = st.text_input("📧 Your Email (Optional)")
    user_name = st.text_input("🧑‍🍳 Your Name (Optional)", placeholder="Optional")
    submitted = st.form_submit_button("Generate Insights")

# --- Run AI and show output ---
if submitted:
    with st.spinner("🔍 Analyzing customer psychology..."):
        prompt = f"""
You are a restaurant marketing expert with a focus on consumer psychology.

Based on the following details:
- Restaurant type: {restaurant_type}
- Audience: {audience}
- Location: {location}
- Avg Order Value: ₹{aov}
- Peak Hours: {peak_hours}
- Feedback: {common_feedback}

Create a report including:
1. Customer behavior patterns & emotional motivators
2. Ideal brand tone and design cues
3. Suggested Instagram content types
4. Promotion styles that would work
5. One-line customer persona summary
"""

        try:
            response = openai.ChatCompletion.create(
                model="openrouter/openai/gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a restaurant marketing and behavioral expert."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7
            )

            output = response.choices[0].message.content
            st.success("✅ Insight Report Ready!")
            st.markdown("### 📋 Results:\n")
            st.markdown(output)

            # PDF generation
            pdf_buffer = generate_pdf(output)
            st.download_button(
                label="📄 Download DinePsych Report",
                data=pdf_buffer,
                file_name="dinepsych_report.pdf",
                mime="application/pdf"
            )

        except Exception as e:
            st.error(f"⚠️ Error: {e}")

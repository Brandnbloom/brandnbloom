import streamlit as st
import openai
import io, json
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from utils import can_use_tool, increment_usage

# 🔐 Streamlit Secrets
openai.api_key = st.secrets["OPENAI_API_KEY"]

# 🌸 Title
st.set_page_config(page_title="DinePsych AI", layout="centered")
st.title("🍽️ DinePsych AI — Customer Behavior Analyzer")

# ✅ Usage Check
user_email = "guest@example.com"
allowed, remaining = can_use_tool(user_email)
if not allowed:
    st.warning("You've used all 3 free tries! Please upgrade via PayPal to continue.")
    st.markdown("[Upgrade here](https://www.paypal.com/brandnbloom)")
    st.stop()

# 📝 Form Input
with st.form("behavior_form"):
    st.subheader("🔍 Describe Your Customer")
    name = st.text_input("Customer's Name or Initials (optional)")
    customer_type = st.selectbox("Type of Customer", ["First-time", "Occasional", "Regular", "Loyal"])
    order_behavior = st.text_area("Typical Orders or Patterns (e.g., Only visits on offers, loves trying new dishes)")
    social_behavior = st.radio("Engages on Instagram?", ["Yes", "No"])
    feedback = st.text_area("Paste review or feedback (if any)")
    submitted = st.form_submit_button("🧠 Analyze Behavior")

# 🧠 GPT-Based Analysis
if submitted:
    increment_usage(user_email)
    st.info("Analyzing with AI...")

    prompt = f"""
    Analyze this restaurant customer based on behavior:
    - Type: {customer_type}
    - Order Style: {order_behavior}
    - Social Engagement: {social_behavior}
    - Feedback: {feedback}

    Classify personality (e.g. loyalist, adventurer, price-sensitive, visual-lover) and give restaurant-specific strategies:
    - Personality Type:
    - Suggested Engagement:
    - What to Avoid:
    - Loyalty Strategy:
    """

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )

    ai_output = response['choices'][0]['message']['content']
    st.success("🎯 Behavioral Analysis")
    st.markdown(ai_output)

    # 📄 PDF Export
    buffer = io.BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=letter)
    pdf.drawString(50, 750, "🍽️ DinePsych AI Report")
    pdf.drawString(50, 730, f"Customer Type: {customer_type}")
    pdf.drawString(50, 710, f"Instagram Engagement: {social_behavior}")
    pdf.drawString(50, 690, f"Order Behavior: {order_behavior[:60]}...")
    pdf.drawString(50, 670, f"Feedback: {feedback[:60]}...")
    pdf.drawString(50, 640, "AI Analysis Summary:")
    text_lines = ai_output.split("\n")
    y = 620
    for line in text_lines:
        if y < 100: break
        pdf.drawString(60, y, line.strip()[:100])
        y -= 20
    pdf.save()
    buffer.seek(0)

    st.download_button("📥 Download PDF Report", buffer, file_name=f"{name or 'customer'}_DinePsych.pdf", mime="application/pdf")

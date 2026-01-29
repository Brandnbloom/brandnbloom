import streamlit as st
from services.storage import load_insights
import pandas as pd

sample_data = pd.DataFrame({
    "customer_id": [1,2,3],
    "recency": [10, 20, 5],
    "frequency": [3, 1, 5],
    "monetary": [200, 150, 500],
    "churn": [0, 1, 0]
})

st.download_button(
    "📥 Download Sample Data",
    data=sample_data.to_csv(index=False),
    file_name="sample_data.csv",
    mime="text/csv"
)

def generate_caption(data, tone):
    if data["negative"] > data["positive"]:
        base = "We heard your feedback and are improving."
    else:
        base = "Thanks for trusting our brand."

    tones = {
        "Friendly": base + " 💛 Stay connected!",
        "Professional": base + " We value our community.",
        "Bold": base + " Big improvements coming soon."
    }

    return tones[tone]

def run():
    data = load_insights()

if not data:
    st.warning("Run at least one tool first.")
    return

st.subheader("AI Caption Generator")

tone = st.selectbox("Tone", ["Professional", "Friendly", "Bold"])

for tool, insights in data.items():
    caption = f"""
Based on our {tool} analysis, we found {insights}.
Here’s what that means for your brand.
"""

    st.text_area(f"Caption from {tool}", caption.strip(), height=120)

"Bold"])

    if st.button("Generate Caption"):
        caption = generate_caption(data, tone)
        st.text_area("Generated Caption", caption, height=120)

  # ---------------- Check usage ----------------
    from streamlit_app import check_usage
    if not check_usage("Insights caption"):
        st.stop()  # Stop the tool if free limit reached

    # ---------------- Tool logic ----------------
    uploaded_file = st.file_uploader("Upload Customer Data", type=['csv'])
    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        st.success("Data loaded successfully!")
        # Your Insights caption logic here...


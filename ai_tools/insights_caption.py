import streamlit as st
from services.storage import load_insights

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

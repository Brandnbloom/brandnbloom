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
    st.markdown("## ✨ Insights → AI Captions")

    data = load_insights()

    if not data:
        st.warning("Run Consumer Behavior analysis first.")
        return

    tone = st.selectbox("Caption Tone", ["Friendly", "Professional", "Bold"])

    if st.button("Generate Caption"):
        caption = generate_caption(data, tone)
        st.text_area("Generated Caption", caption, height=120)

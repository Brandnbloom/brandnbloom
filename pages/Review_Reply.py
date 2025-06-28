import streamlit as st
from utils import can_use_tool, increment_usage

st.title("💬 Review Reply Assistant")

if can_use_tool("ReviewReply"):
    review_text = st.text_area("📥 Paste a customer review (positive/negative)")
    tone = st.selectbox("Tone of reply", ["Grateful", "Apologetic", "Witty"])
    email = st.text_input("📧 Your Email (optional)")

    if st.button("Generate Reply"):
        increment_usage("ReviewReply")

        # Mock reply generator
        if "bad" in review_text.lower():
            response = "We’re really sorry to hear that! 🙏 Your feedback helps us improve."
        else:
            response = "Thank you so much for your kind words! 😊 We’re thrilled to serve you again!"

        st.code(f"Tone: {tone}\nReply: {response}")
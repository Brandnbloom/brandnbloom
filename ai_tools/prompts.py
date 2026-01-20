# ai_tools/prompts.py
import streamlit as st

def run():
    st.markdown("## ✍️ Prompt Generator")

    goal = st.selectbox(
        "What do you want to generate?",
        [
            "Instagram caption",
            "Email subject line",
            "Ad copy",
            "Product description"
        ]
    )

    if st.button("Generate Prompt"):
        st.success("Prompt ready")
        st.code(f"Write a high-converting {goal.lower()} for a premium brand.")

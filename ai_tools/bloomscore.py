# ai_tools/bloomscore.py
import streamlit as st

def run():
    st.markdown("## 🔬 BloomScore")
    st.write("Instant brand health score")

    handle = st.text_input("Instagram handle (without @)", "brandnbloom")

    if st.button("Compute BloomScore"):
        score = 78  # demo value

        if score >= 80:
            bucket = "Excellent"
        elif score >= 60:
            bucket = "Good"
        elif score >= 40:
            bucket = "Average"
        else:
            bucket = "Needs Improvement"

        st.metric("BloomScore", score)
        st.write("Category:", bucket)

        st.json({
            "engagement": "Good",
            "posting consistency": "Average",
            "growth": "Moderate"
        })

import streamlit as st
from services.storage import load_insights

def run():
    st.markdown("## 📊 Brand Intelligence Dashboard")

    insights = load_insights()

    if not insights:
        st.warning("No data available yet.")
        return

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Responses", insights["total"])
    c2.metric("Positive", insights["positive"])
    c3.metric("Neutral", insights["neutral"])
    c4.metric("Negative", insights["negative"])

    if insights["negative"] > insights["positive"]:
        st.error("⚠️ Customer dissatisfaction detected")
    else:
        st.success("💚 Brand sentiment is healthy")

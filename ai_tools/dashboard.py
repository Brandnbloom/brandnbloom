import streamlit as st

def run():
    st.markdown("## 📊 Brand Dashboard")

    insights = st.session_state.get("consumer_insights")

    if not insights:
        st.warning("No consumer data found yet.")
        return

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Total Responses", insights["total_responses"])
    c2.metric("Positive", insights["positive"])
    c3.metric("Neutral", insights["neutral"])
    c4.metric("Negative", insights["negative"])

    st.success("Dashboard updated with real consumer data")

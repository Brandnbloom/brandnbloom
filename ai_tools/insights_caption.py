import streamlit as st

def generate_caption(insights, tone):
    if insights["negative"] > insights["positive"]:
        base = "We hear you. We're improving based on your feedback."
    else:
        base = "Thanks for loving our brand! More value coming your way."

    if tone == "Friendly":
        return base + " 💛 Stay tuned!"
    elif tone == "Professional":
        return base + " We appreciate your trust."
    else:
        return base

def run():
    st.markdown("## ✨ Insights → AI Captions")

    insights = st.session_state.get("consumer_insights")

    if not insights:
        st.warning("Analyze consumer behavior first.")
        return

    tone = st.selectbox(
        "Select tone",
        ["Friendly", "Professional", "Neutral"]
    )

    if st.button("Generate Caption"):
        caption = generate_caption(insights, tone)

        st.markdown("### 📝 Generated Caption")
        st.text_area("", caption, height=100)

        st.success("Caption generated from real insights")

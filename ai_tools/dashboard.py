import streamlit as st
from services.insights_store import load_insights
from services.caption_engine import generate_caption

def run():
    st.markdown("## 📊 Insight Dashboard")

    user_id = st.session_state.get("user_id", "guest")
    insights = load_insights(user_id)

    if not insights:
        st.info("No insights yet. Use tools to generate intelligence.")
        return

    for record in reversed(insights):
        with st.expander(
            f"🔹 {record['tool']} • {record['timestamp'][:19]}"
        ):
            st.json(record["data"])

            if st.button(
                f"Generate Caption from {record['tool']}",
                key=f"{record['tool']}_{record['timestamp']}"
            ):
                caption = generate_caption(
                    insight=record["data"],
                    tone="friendly",
                    platform="Instagram"
                )
                st.text_area("Caption", caption, height=180)


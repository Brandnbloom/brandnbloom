import streamlit as st
from services.insights_store import load_insights
from services.caption_engine import generate_caption
import pandas as pd

def run():
    st.markdown("## 📊 Insight Dashboard")

    user_id = st.session_state.get("user_id", "guest")
    insights = load_insights(user_id)

    if not insights:
        st.info("No insights yet. Use tools to generate intelligence.")
        return

    # Convert to DataFrame for export
    df = pd.DataFrame([
        {
            "Tool": r["tool"],
            "Timestamp": r["timestamp"],
            "Data": r["data"]
        } for r in insights
    ])

    st.download_button(
        "📥 Export Insights (JSON)",
        data=df.to_json(orient="records", indent=2),
        file_name="insights.json",
        mime="application/json"
    )

    st.download_button(
        "📥 Export Insights (CSV)",
        data=df.to_csv(index=False),
        file_name="insights.csv",
        mime="text/csv"
    )

    # Display insights
    for record in reversed(insights):
        with st.expander(f"🔹 {record['tool']} • {record['timestamp'][:19]}"):
            st.json(record["data"])

            # Auto-generated caption
            caption = generate_caption(
                insight=record["data"],
                tone="friendly",
                platform="Instagram"
            )
            st.text_area("Caption", caption, height=180)

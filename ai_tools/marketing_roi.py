import streamlit as st
from services.google_analytics_api import get_ga4_metrics
from utils.dashboard import save_to_dashboard
from utils.visualization import visualize_data
from services.openai_api import generate_ai_caption

def run():
    st.subheader("📊 Google Analytics Insights")

    df = get_ga4_metrics()
    st.dataframe(df)

    save_to_dashboard("ga4_metrics", df)
    visualize_data("ga4_metrics", df)

    insight = generate_ai_caption("ga4_metrics", df)
    st.success(f"💡 GA Insight: {insight}"

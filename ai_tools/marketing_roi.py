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

  # ---------------- Check usage ----------------
    from streamlit_app import check_usage
    if not check_usage("Marketing ROI"):
        st.stop()  # Stop the tool if free limit reached

    # ---------------- Tool logic ----------------
    uploaded_file = st.file_uploader("Upload Customer Data", type=['csv'])
    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        st.success("Data loaded successfully!")
        # Your Marketing ROI logic here...

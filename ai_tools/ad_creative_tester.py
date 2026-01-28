import streamlit as st
import pandas as pd
from services.ads_api import get_ad_performance  # Your real ads API service
from streamlit_app import save_to_dashboard, visualize_data, generate_ai_caption
from utils.dashboard import save_to_dashboard
from utils.visualization import visualize_data
from services.openai_api import generate_ai_caption
from utils.usage_limiter import can_use_tool, increment_usage, usage_banner
def run():
    st.subheader("🧪 Ad Creative Tester")
    usage_banner()

    if not can_use_tool():
        st.warning("🔒 Upgrade to unlock unlimited access.")
        st.stop()

    if st.button("Run A/B Analysis"):
        increment_usage()
        # 👉 real API + analytics logic here
        st.success("Analysis complete!")

    if st.button("Fetch Live Ad Data"):
        df_ads = get_ad_performance()

        st.dataframe(df_ads)

        save_to_dashboard("ad_performance", df_ads)
        visualize_data("ad_performance", df_ads)

        insight = generate_ai_caption("ad_performance", df_ads)
        st.success(f"💡 AI Insight: {insight}")
    # ------------------- Input -------------------
    campaign_id = st.text_input("Enter Campaign ID or Name")
    limit = st.number_input("Number of recent ads to analyze", min_value=1, max_value=100, value=10)

    if campaign_id:
        with st.spinner("Fetching ad performance data..."):
            try:
                # Fetch real ad data from your ads API
                df_ads = get_ad_performance(campaign_id=campaign_id, limit=limit)

                if df_ads.empty:
                    st.warning("No ad data found for this campaign.")
                    return

                st.success("✅ Data fetched successfully!")
                st.dataframe(df_ads)


                # ------------------- AI Caption -------------------
                caption = generate_ai_caption("ab_test", df_ads)
                st.success(f"💡 AI Insight: {caption}")

                # ------------------- Export Option -------------------
                csv = df_ads.to_csv(index=False).encode("utf-8")
                st.download_button(
                    label="📥 Download Report as CSV",
                    data=csv,
                    file_name=f"{campaign_id}_ab_test.csv",
                    mime="text/csv"
                )

            except Exception as e:
                st.error(f"Failed to fetch ad data: {e}")
  s

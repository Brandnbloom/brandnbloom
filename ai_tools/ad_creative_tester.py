import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

def run_ad_creative_tester():
    st.subheader("🧪 Ad Creative A/B Testing Simulator")

    st.markdown("Upload your campaign data (ad versions, impressions, clicks).")

    uploaded_file = st.file_uploader("Upload CSV", type=['csv'])
    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        st.write("Data Preview", df.head())

        if st.button("Run A/B Test Simulation"):
            # Simple CTR comparison
            df['ctr'] = df['clicks'] / df['impressions']
            summary = df.groupby('ad_version')['ctr'].mean().reset_index()
            st.write(summary)

            fig = px.bar(summary, x='ad_version', y='ctr', color='ad_version', title="A/B Test CTR Comparison")
            st.plotly_chart(fig)

            st.download_button(
                "📥 Download Summary CSV",
                data=summary.to_csv(index=False),
                file_name="ab_test_results.csv",
                mime="text/csv"
            )
    else:
        # Sample data download
        sample = pd.DataFrame({
            "ad_version": ["A", "B", "C"],
            "impressions": [1000, 1200, 1100],
            "clicks": [100, 130, 90]
        })
        st.download_button(
            "📥 Download Sample Data",
            data=sample.to_csv(index=False),
            file_name="sample_ab_test.csv",
            mime="text/csv"
        )
save_to_dashboard("ab_test", summary)

st.subheader("Ad Creative Tester")
campaign_id = st.text_input("Enter Campaign ID")
if campaign_id:
    # Pull real ad metrics
    df_ads = get_ad_performance(campaign_id)  # implement in your services
    st.dataframe(df_ads)
    
    # Save + visualize
    save_to_dashboard("ab_test", df_ads)
    visualize_data("ab_test", df_ads)
    
    # AI suggestions
    caption = generate_ai_caption("ab_test", df_ads)
    st.success(f"💡 AI Insight: {caption}")


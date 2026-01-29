import streamlit as st
import pandas as pd
from services.google_analytics_api import get_ga_data
from services.meta_pixel_api import get_meta_pixel_data
from utils.dashboard import save_to_dashboard
from utils.visualization import visualize_data
from services.openai_api import generate_ai_caption
import plotly.express as px
from services.ads_api import get_ads_data  # Meta Ads API
import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_ai_caption(tool_name, df):
    try:
        prompt = f"Suggest improvements and insights from {tool_name} dataset: {df.head(10).to_dict()}"
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=150
        )
        return response.choices[0].message.content
    except:
        return "AI Insight not available"

def run():
    st.header("🧪 Ad Creative Tester (A/B Testing)")

    if st.button("Fetch & Analyze Ads"):
        df = get_ads_data()  # Meta Ads API
        if df.empty:
            st.warning("No ad data available.")
            return
        st.success("✅ Ad data loaded")
        st.dataframe(df.head(10))

        # Example: CTR Comparison
        if "clicks" in df.columns and "impressions" in df.columns:
            df["CTR"] = df["clicks"] / df["impressions"] * 100
            fig = px.bar(df, x="ad_name", y="CTR", title="CTR % Comparison")
            st.plotly_chart(fig)

        # AI Caption / Suggestion
        caption = generate_ai_caption("Ad Creative Tester", df)
        st.success(f"💡 AI Suggestion: {caption}")

        # Save to dashboard
        df["AI_Insight"] = caption
        if "dashboard_data" not in st.session_state:
            st.session_state["dashboard_data"] = {}
        st.session_state["dashboard_data"]["ad_creatives"] = df

def run_roi_tracker(user_id):
    st.title("📊 Marketing ROI Tracker")

    # 1️⃣ Fetch GA + Meta
    ga_df = get_ga_data(property_id=os.getenv("GA4_PROPERTY_ID"))
    meta_df = get_meta_pixel_data()

    # 2️⃣ Merge on campaign
    df = pd.merge(ga_df, meta_df, left_on="campaign", right_on="campaign", how="outer").fillna(0)

    # 3️⃣ Calculate ROI
    df["ROI"] = df["revenue"] / df["spend"].replace(0, 1)

    # 4️⃣ Visualize
    st.dataframe(df)
    visualize_data("roi_tracker", df)

    # 5️⃣ Save + AI Caption
    save_to_dashboard("ROI Tracker", df)
    caption = generate_ai_caption("roi_tracker", df)
    st.success(f"💡 AI Insight: {caption}")



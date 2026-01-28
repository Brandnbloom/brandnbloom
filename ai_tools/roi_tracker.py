import streamlit as st
import pandas as pd
from services.google_analytics_api import get_ga_data
from services.meta_pixel_api import get_meta_pixel_data
from utils.dashboard import save_to_dashboard
from utils.visualization import visualize_data
from services.openai_api import generate_ai_caption

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



import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from services.ads_api import get_ad_performance
from utils.dashboard import save_to_dashboard
from utils.visualization import visualize_data
from services.openai_api import generate_ai_caption

def run():
    st.subheader("Ad Creative Tester")
    campaign_id = st.text_input("Enter Campaign ID")

    if campaign_id:
        df_ads = get_ad_performance(campaign_id)
        st.dataframe(df_ads)

        save_to_dashboard("ab_test", df_ads)
        visualize_data("ab_test", df_ads)

        caption = generate_ai_caption("ab_test", df_ads)
        st.success(f"💡 AI Insight: {caption}")


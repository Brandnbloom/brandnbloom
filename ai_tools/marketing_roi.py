import streamlit as st
from services.market_api import get_market_trends, get_marketing_roi
from utils.dashboard import save_to_dashboard
from services.openai_api import generate_ai_caption

def run():
    market_df = get_market_trends()
    roi_df = get_marketing_roi()

    save_to_dashboard("market_trends", market_df)
    save_to_dashboard("roi", roi_df)

    st.success(generate_ai_caption("market_trends", market_df))
    st.success(generate_ai_caption("roi", roi_df))


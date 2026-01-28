import streamlit as st
import pandas as pd

from services.google_analytics_api import get_ga_user_data
from services.stripe_api import get_stripe_customers
from services.meta_pixel_api import get_meta_pixel_data

from utils.dashboard import save_to_dashboard
from utils.visualization import visualize_data
from services.openai_api import generate_ai_caption

def run():
    st.subheader("👤 Customer 360 View")

    df_ga = get_ga_user_data()
    df_stripe = get_stripe_customers()
    df_meta = get_meta_pixel_data()

    df = df_ga.merge(df_stripe, on="email", how="left")
    df = df.merge(df_meta, on="email", how="left")

    st.dataframe(df)

    save_to_dashboard("customer_360", df)
    visualize_data("customer_360", df)

    insight = generate_ai_caption("customer_360", df)
    st.success(f"💡 Customer Insight: {insight}")


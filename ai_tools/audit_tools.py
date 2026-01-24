import streamlit as st
from services.insights_store import save_insight
from services.caption_engine import generate_caption
from services.instagram_api import get_profile, get_posts
from utils.dashboard import save_to_dashboard
from utils.visualization import visualize_data
from services.openai_api import generate_ai_caption

import pandas as pd

sample_data = pd.DataFrame({
    "customer_id": [1,2,3],
    "recency": [10, 20, 5],
    "frequency": [3, 1, 5],
    "monetary": [200, 150, 500],
    "churn": [0, 1, 0]
})

st.download_button(
    "📥 Download Sample Data",
    data=sample_data.to_csv(index=False),
    file_name="sample_data.csv",
    mime="text/csv"
)

def run():
    st.subheader("Instagram Data Analysis")
    username = st.text_input("Enter Instagram Username")

    if username:
        posts_df = get_posts(username, limit=50)
        st.dataframe(posts_df)

        save_to_dashboard("social_posts", posts_df)
        visualize_data("social_posts", posts_df)

        caption = generate_ai_caption("social_posts", posts_df)
        st.success(f"💡 AI Insight: {caption}")

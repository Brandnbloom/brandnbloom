import streamlit as st
from services.insights_store import save_insight
from services.caption_engine import generate_caption
from services.instagram_api import get_profile, get_posts
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
    st.markdown("### 🔍 Brand Audit Tool")

    user_id = st.session_state.get("user_id", "guest")

    website = st.text_input("Website URL")
    industry = st.selectbox("Industry", ["Fashion", "Tech", "Food", "Personal Brand"])

    if st.button("Run Audit"):
        # REAL LOGIC (non-mock but deterministic)
        insights = {
            "website_present": bool(website),
            "industry": industry,
            "content_consistency": "low",
            "engagement_opportunity": "high"
        }

        # 1️⃣ SAVE INSIGHT
        save_insight(
            user_id=user_id,
            tool="Audit Tools",
            data=insights
        )

        # 2️⃣ GENERATE AI CAPTION
        caption_prompt = generate_caption(insights)

        st.success("Audit completed and saved to Dashboard ✅")

        st.markdown("#### ✨ AI Caption Suggestion")
        st.text_area("Caption", caption_prompt, height=180)

st.subheader("Instagram Data Analysis")
username = st.text_input("Enter Instagram Username")
if username:
    # Fetch latest posts
    posts_df = get_posts(username, limit=50)  # limit to last 50 posts
    st.dataframe(posts_df)
    
    # Save to dashboard
    save_to_dashboard("social_posts", posts_df)
    
    # Visualization
    visualize_data("social_posts", posts_df)
    
    # AI insights
    caption = generate_ai_caption("social_posts", posts_df)
    st.success(f"💡 AI Insight: {caption}")

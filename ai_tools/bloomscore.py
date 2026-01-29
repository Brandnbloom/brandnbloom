import streamlit as st
from ai_tools.profile_fetcher import InstagramProfileFetcher
import pandas as pd
from services.instagram_api import get_profile, get_posts

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

def compute_bloomscore(profile):
    score = min(
        round(
            profile["engagement_rate"] * 40 +
            profile["posting_consistency"] * 30 +
            min(profile["followers"] / 100, 30)
        ),
        100
    )

    bucket = (
        "Excellent" if score >= 80 else
        "Good" if score >= 60 else
        "Average" if score >= 40 else
        "Needs Improvement"
    )

    return score, bucket

def run():
    st.markdown("## 🌸 BloomScore")

    username = st.text_input("Instagram Handle", "brandnbloom")

    if st.button("Analyze"):
        fetcher = InstagramProfileFetcher()
        profile = fetcher.fetch(username)

        score, bucket = compute_bloomscore(profile)

        st.metric("BloomScore", score)
        st.write("Category:", bucket)

  # ---------------- Check usage ----------------
    from streamlit_app import check_usage
    if not check_usage("Bloom Score"):
        st.stop()  # Stop the tool if free limit reached

    # ---------------- Tool logic ----------------
    uploaded_file = st.file_uploader("Upload Customer Data", type=['csv'])
    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        st.success("Data loaded successfully!")
        # Your bloom score logic here...


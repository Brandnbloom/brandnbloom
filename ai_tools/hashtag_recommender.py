import streamlit as st
from ai_tools.profile_fetcher import InstagramProfileFetcher

def run():
    st.markdown("## 🔖 Hashtag Recommender")

    username = st.text_input("Instagram Handle", "brandnbloom")

    if st.button("Recommend"):
        fetcher = InstagramProfileFetcher()
        profile = fetcher.fetch(username)

        hashtags = profile.get("recent_hashtags", [])
        st.code(" ".join(hashtags))


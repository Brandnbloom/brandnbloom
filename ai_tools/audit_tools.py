import streamlit as st
from ai_tools.profile_fetcher import InstagramProfileFetcher

def run():
    st.markdown("## 🔍 Audit Tools")

    username = st.text_input("Instagram Handle", "brandnbloom")

    if st.button("Run Audit"):
        fetcher = InstagramProfileFetcher()
        profile = fetcher.fetch(username)

        st.write("Followers:", profile["followers"])
        st.write("Engagement Rate:", profile["engagement_rate"])
        st.write("Bio Present:", profile["bio_present"])
        st.write("Profile Picture:", profile["profile_pic_present"])

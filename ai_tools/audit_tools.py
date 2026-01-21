import streamlit as st
from services.instagram_api import get_profile, get_posts

def run():
    st.subheader("Instagram Audit Tool (Live)")

    username = st.text_input("Instagram Username")

    if st.button("Run Audit"):
        if not username:
            st.warning("Enter a username")
            return

        try:
            profile = get_profile(username)
            posts = get_posts(username)

            st.success("Live data fetched")

            st.metric("Followers", profile["followers"])
            st.metric("Following", profile["following"])
            st.metric("Posts", profile["posts"])

            likes = [p["like_count"] for p in posts["data"] if "like_count" in p]
            comments = [p["comment_count"] for p in posts["data"] if "comment_count" in p]

            if likes:
                engagement = (sum(likes) + sum(comments)) / len(likes)
                st.metric("Avg Engagement", round(engagement, 2))

            st.markdown("### Recent Posts")
            for p in posts["data"][:6]:
                st.image(p["thumbnail_url"], width=150)

        except Exception as e:
            st.error(f"Audit failed: {e}")

# ai_tools/bloomscore.py

import streamlit as st


def calculate_engagement(likes: int, comments: int, followers: int) -> float:
    if followers <= 0:
        return 0.0
    return ((likes + comments) / followers) * 100


def run():
    st.markdown("## 🌸 BloomScore")
    st.markdown("Measure your brand’s social media health.")

    col1, col2 = st.columns(2)

    with col1:
        username = st.text_input("Instagram Username", placeholder="brandnbloom")
        followers = st.number_input("Followers", min_value=0, step=100)
        posts_per_week = st.slider("Posts per week", 0, 7, 3)

    with col2:
        avg_likes = st.number_input("Average Likes per Post", min_value=0, step=10)
        avg_comments = st.number_input("Average Comments per Post", min_value=0, step=5)

    if st.button("Calculate BloomScore"):
        if not username or followers == 0:
            st.error("Please enter valid profile details.")
            return

        engagement_rate = calculate_engagement(avg_likes, avg_comments, followers)

        # -------------------------
        # Scoring Logic (v1)
        # -------------------------
        engagement_score = min(engagement_rate * 10, 40)   # max 40
        consistency_score = min(posts_per_week * 5, 20)    # max 20

        reach_score = 0
        if followers >= 10000:
            reach_score = 25
        elif followers >= 3000:
            reach_score = 18
        elif followers >= 1000:
            reach_score = 12
        else:
            reach_score = 8

        bloomscore = int(engagement_score + consistency_score + reach_score)
        bloomscore = min(bloomscore, 100)

        if bloomscore >= 80:
            category = "🌟 Excellent"
        elif bloomscore >= 60:
            category = "✅ Good"
        elif bloomscore >= 40:
            category = "⚠️ Average"
        else:
            category = "❌ Needs Improvement"

        # -------------------------
        # Output
        # -------------------------
        st.success(f"BloomScore for @{username}: **{bloomscore}/100**")
        st.write("### Category:", category)

        st.markdown("### 📊 Breakdown")
        st.write(f"Engagement Rate: **{engagement_rate:.2f}%**")
        st.write(f"Posting Consistency Score: **{consistency_score}/20**")
        st.write(f"Reach Score: **{reach_score}/25**")

        st.markdown("### 💡 Recommendations")
        if engagement_rate < 2:
            st.write("• Improve content quality and hooks")
        if posts_per_week < 3:
            st.write("• Post at least 3–4 times per week")
        if followers < 3000:
            st.write("• Focus on collaborations and reels")

# ai_tools/business_compare.py

import streamlit as st


def engagement_rate(likes: int, comments: int, followers: int) -> float:
    if followers <= 0:
        return 0.0
    return ((likes + comments) / followers) * 100


def run():
    st.markdown("## 📈 Business Compare")
    st.markdown("Compare your brand with a competitor and see who’s winning.")

    st.markdown("### 🔹 Your Brand")
    c1, c2, c3 = st.columns(3)
    with c1:
        your_followers = st.number_input("Your Followers", min_value=0, step=100)
    with c2:
        your_likes = st.number_input("Your Avg Likes", min_value=0, step=10)
    with c3:
        your_comments = st.number_input("Your Avg Comments", min_value=0, step=5)

    your_posts = st.slider("Your Posts per Week", 0, 7, 3)

    st.divider()

    st.markdown("### 🔸 Competitor")
    c4, c5, c6 = st.columns(3)
    with c4:
        comp_followers = st.number_input("Competitor Followers", min_value=0, step=100)
    with c5:
        comp_likes = st.number_input("Competitor Avg Likes", min_value=0, step=10)
    with c6:
        comp_comments = st.number_input("Competitor Avg Comments", min_value=0, step=5)

    comp_posts = st.slider("Competitor Posts per Week", 0, 7, 3)

    if st.button("Compare Brands"):
        if your_followers == 0 or comp_followers == 0:
            st.error("Please enter valid follower counts.")
            return

        your_er = engagement_rate(your_likes, your_comments, your_followers)
        comp_er = engagement_rate(comp_likes, comp_comments, comp_followers)

        st.markdown("## 📊 Comparison Results")

        col1, col2 = st.columns(2)

        with col1:
            st.metric("Your Engagement Rate", f"{your_er:.2f}%")
            st.metric("Your Posting Frequency", f"{your_posts}/week")
            st.metric("Your Followers", your_followers)

        with col2:
            st.metric("Competitor Engagement Rate", f"{comp_er:.2f}%")
            st.metric("Competitor Posting Frequency", f"{comp_posts}/week")
            st.metric("Competitor Followers", comp_followers)

        st.markdown("### 🏆 Insights")

        if your_er > comp_er:
            st.write("✅ Your engagement is stronger than your competitor.")
        else:
            st.write("⚠️ Competitor has higher engagement — improve content quality.")

        if your_posts > comp_posts:
            st.write("✅ You post more consistently.")
        else:
            st.write("⚠️ Competitor posts more often — consistency matters.")

        if your_followers > comp_followers:
            st.write("✅ You have a larger audience.")
        else:
            st.write("⚠️ Competitor has a larger audience — focus on reach & growth.")

        st.markdown("### 💡 Action Plan")
        st.write("• Improve hooks & CTAs if engagement is low")
        st.write("• Match or exceed competitor posting frequency")
        st.write("• Use collaborations and reels for reach")

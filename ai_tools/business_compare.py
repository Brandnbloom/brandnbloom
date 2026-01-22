import streamlit as st

def engagement_rate(likes, comments, followers):
    if followers == 0:
        return 0
    return round(((likes + comments) / followers) * 100, 2)

def run():
    st.subheader("📊 Business Compare")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### Brand A")
        a_name = st.text_input("Brand A Name")
        a_followers = st.number_input("Followers", min_value=0)
        a_likes = st.number_input("Avg Likes", min_value=0)
        a_comments = st.number_input("Avg Comments", min_value=0)

    with col2:
        st.markdown("### Brand B")
        b_name = st.text_input("Brand B Name")
        b_followers = st.number_input("Followers ", min_value=0)
        b_likes = st.number_input("Avg Likes ", min_value=0)
        b_comments = st.number_input("Avg Comments ", min_value=0)

    if st.button("Compare Brands"):
        a_eng = engagement_rate(a_likes, a_comments, a_followers)
        b_eng = engagement_rate(b_likes, b_comments, b_followers)

        st.markdown("### 📈 Comparison Results")

        st.metric(f"{a_name} Engagement Rate", f"{a_eng}%")
        st.metric(f"{b_name} Engagement Rate", f"{b_eng}%")

        if a_eng > b_eng:
            st.success(f"🏆 {a_name} has stronger engagement")
        elif b_eng > a_eng:
            st.success(f"🏆 {b_name} has stronger engagement")
        else:
            st.info("Both brands have equal engagement")

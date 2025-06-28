import streamlit as st
from utils import send_email_with_pdf, can_use_tool, increment_usage

st.title("📈 BloomInsight – Performance Dashboard")

if can_use_tool("BloomInsight"):
    instagram_followers = st.number_input("📷 Instagram Followers", min_value=0)
    instagram_engagement = st.number_input("❤️ Instagram Engagement Rate (%)", min_value=0.0)

    gmb_views = st.number_input("📍 Google My Business Monthly Views", min_value=0)
    gmb_rating = st.slider("⭐ GMB Rating", min_value=1.0, max_value=5.0, value=4.0)

    website_visits = st.number_input("🌐 Website Visits (monthly)", min_value=0)
    bounce_rate = st.slider("↩️ Bounce Rate (%)", min_value=0, max_value=100, value=50)

    if st.button("🔍 Analyze & Email Report"):
        summary = f"""
        🌸 BloomInsight Report 🌸

        Instagram:
        - Followers: {instagram_followers}
        - Engagement Rate: {instagram_engagement}%

        Google My Business:
        - Monthly Views: {gmb_views}
        - Rating: {gmb_rating}/5

        Website:
        - Monthly Visits: {website_visits}
        - Bounce Rate: {bounce_rate}%
        """

        email = st.text_input("Enter your email to receive the report:")
        if email:
            send_email_with_pdf("Your BloomInsight Report", email, summary)
            increment_usage("BloomInsight")
else:
    st.warning("🛑 Free usage limit reached. Please upgrade to continue.")
    st.page_link("https://brand-n-bloom.com/upgrade", label="Upgrade Plan", icon="💳")

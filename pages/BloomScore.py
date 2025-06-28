import streamlit as st
from utils import can_use_tool, increment_usage, send_email_with_pdf
# show_stripe_buttons removed temporarily
st.title("📊 BloomScore – Social & Website Audit")

if can_use_tool("BloomScore"):
    with st.form("bloomscore_form"):
        instagram = st.text_input("Instagram URL")
        website = st.text_input("Website URL")
        email = st.text_input("Your Email")

        submitted = st.form_submit_button("Analyze")

        if submitted:
            increment_usage("BloomScore")

            # Mock Output
            result = f'''
            🔍 Instagram: {instagram}
            - Follower Quality: Good
            - Hashtags: #foodie #localdelight
            - Content Type: Mixed Reels & Posts
            - Frequency: 4x/week

            🌐 Website: {website}
            - SEO Score: 74/100
            - Mobile Friendly: Yes
            - Page Speed: Moderate
            '''

            st.code(result)
            send_email_with_pdf("Your BloomScore Report", email, result)

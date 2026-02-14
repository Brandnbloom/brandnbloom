import streamlit as st
from utils import can_use_tool, increment_usage, send_email_with_pdf
import plotly.express as px
import pandas as pd
import requests

username = st.text_input("Enter Instagram Username")
if st.button("Scrape Data"):
    response = requests.get(f"https://YOUR_RENDER_URL/scrape?username={username}")
    st.json(response.json())

st.set_page_config(page_title="BloomInsight", layout="wide")
st.title("📈 BloomInsight – Instagram Engagement Analyzer")

# Ask for user's email before starting (so we can track per-user usage)
email = st.text_input("📧 Enter your email to continue")

if email and can_use_tool(email, "BloomInsight"):
    st.write("Answer these quick questions about your Instagram account:")

    # Questionnaire inputs
    avg_likes = st.number_input("1️⃣ Average likes per post", min_value=0)
    avg_comments = st.number_input("2️⃣ Average comments per post", min_value=0)
    posts_per_month = st.number_input("3️⃣ Number of posts per month", min_value=0)
    followers = st.number_input("4️⃣ Current number of followers", min_value=0)
    goal_followers = st.number_input("5️⃣ Follower goal for next 3 months", min_value=0)
    content_type = st.selectbox("6️⃣ Main content type", ["Photos", "Reels", "Carousels", "Mixed"])
    hashtags_use = st.radio("7️⃣ Do you use hashtags?", ["Yes", "No"])
    collabs_use = st.radio("8️⃣ Do you collaborate with other creators?", ["Yes", "No"])

    if st.button("🔍 Analyze My Engagement"):
        st.subheader("Monthly Engagement Overview")

        # Fake monthly data simulation based on questionnaire
        months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun"]
        likes_data = [avg_likes + (i * 5) for i in range(len(months))]  # Just for demo
        df = pd.DataFrame({"Month": months, "Likes": likes_data})

        fig = px.bar(
            df,
            x="Month",
            y="Likes",
            title="📊 Estimated Average Likes per Month",
            color="Likes",
            color_continuous_scale="sunset"
        )
        st.plotly_chart(fig, use_container_width=True)

        # Insights based on answers
        st.subheader("📌 Top Recommendations")
        if avg_likes < 50:
            st.write("🚀 Increase engagement by posting **Reels** and trending content.")
        if posts_per_month < 8:
            st.write("📅 Increase posting frequency to at least **2 posts per week**.")
        if hashtags_use == "No":
            st.write("🏷️ Use relevant hashtags to reach a wider audience.")
        if collabs_use == "No":
            st.write("🤝 Collaborate with creators in your niche for growth.")

        # Email PDF option
        if st.checkbox("📤 Email me this report"):
            if st.button("Send Report"):
                report_text = (
                    f"Instagram Performance Summary\n\n"
                    f"Average Likes: {avg_likes}\n"
                    f"Average Comments: {avg_comments}\n"
                    f"Posts per Month: {posts_per_month}\n"
                    f"Followers: {followers}\n"
                    f"Goal Followers: {goal_followers}\n"
                    f"Content Type: {content_type}\n"
                    f"Hashtags Used: {hashtags_use}\n"
                    f"Collaborations: {collabs_use}"
                )
                send_email_with_pdf("BloomInsight Report", email, report_text)

        increment_usage(email, "BloomInsight")

elif email:
    st.error("⚠️ You've reached the usage limit for BloomInsight.")

st.info("""
🧠 *Note:* The insights provided by this tool are generated using AI and public data. 
While helpful, they may not reflect 100% accuracy or real-time changes. 
Always consult professionals before making critical decisions.
""")

import streamlit as st
from utils import can_use_tool, increment_usage, send_email_with_pdf
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="BloomInsight", layout="wide")
st.title("📈 BloomInsight – Instagram Engagement Analyzer")

if can_use_tool("BloomInsight"):
    uploaded_file = st.file_uploader("Upload your Instagram data CSV", type=["csv"])

    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)

        if 'Post Date' in df.columns and 'Likes' in df.columns:
            df['Post Date'] = pd.to_datetime(df['Post Date'])
            df['Month'] = df['Post Date'].dt.to_period("M").astype(str)

            st.subheader("Monthly Engagement Overview")
            monthly = df.groupby("Month")[["Likes"]].mean().reset_index()
            fig = px.bar(monthly, x="Month", y="Likes", title="📊 Average Likes per Month", color="Likes", color_continuous_scale="sunset")
            st.plotly_chart(fig, use_container_width=True)

            st.subheader("📌 Top Performing Posts")
            top_posts = df.sort_values("Likes", ascending=False).head(5)
            st.write(top_posts[["Post Date", "Caption", "Likes"]])

            # Email PDF option
            if st.checkbox("📤 Email me this report"):
                email = st.text_input("Enter your email")
                if st.button("Send Report"):
                    report_text = f"Instagram Performance Summary\n\nTop Posts:\n{top_posts.to_string(index=False)}"
                    send_email_with_pdf("BloomInsight Report", email, report_text)

            increment_usage("BloomInsight")
        else:
            st.warning("❗ Ensure your CSV has 'Post Date', 'Caption', and 'Likes' columns.")
else:
    st.error("⚠️ You've reached the usage limit for BloomInsight.")

st.info("""
🧠 *Note:* The insights provided by this tool are generated using AI and public data. While helpful, they may not reflect 100% accuracy or real-time changes. Always consult professionals before making critical decisions.
""")

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

        # Check for required columns
        if 'Post Date' in df.columns and 'Likes' in df.columns:
            if df.empty:
                st.warning("❗ Your CSV file is empty. Please upload a file with data.")
            else:
                df['Post Date'] = pd.to_datetime(df['Post Date'], errors='coerce')
                df = df.dropna(subset=['Post Date'])  # Remove rows where Post Date couldn't be parsed
                df['Month'] = df['Post Date'].dt.to_period("M").astype(str)

                # Double-check after cleaning that there's still data
                if df.empty:
                    st.warning("❗ No valid data found after processing dates. Please check your file.")
                else:
                    st.subheader("Monthly Engagement Overview")
                    monthly = df.groupby("Month")[["Likes"]].mean().reset_index()

                    if monthly.empty:
                        st.warning("❗ No monthly engagement data available to plot.")
                    else:
                        fig = px.bar(
                            monthly,
                            x="Month",
                            y="Likes",
                            title="📊 Average Likes per Month",
                            color="Likes",
                            color_continuous_scale="sunset"
                        )
                        st.plotly_chart(fig, use_container_width=True)

                    st.subheader("📌 Top Performing Posts")
                    top_posts = df.sort_values("Likes", ascending=False).head(5)
                    if top_posts.empty:
                        st.warning("❗ No top posts to display.")
                    else:
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

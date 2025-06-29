import streamlit as st
from utils import can_use_tool, increment_usage, send_email_with_pdf
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="DinePsych", layout="wide")
st.title("🧠 DinePsych – Customer Behavior Decoder")

if can_use_tool("DinePsych"):
    uploaded_file = st.file_uploader("Upload customer behavior CSV", type=["csv"])

    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.success("✅ File Uploaded Successfully")

        if 'Visit Time' in df.columns and 'Amount Spent' in df.columns:
            df['Visit Time'] = pd.to_datetime(df['Visit Time'])

            st.subheader("🕓 Visit Time Distribution")
            df['Hour'] = df['Visit Time'].dt.hour
            fig, ax = plt.subplots()
            sns.histplot(df['Hour'], bins=24, kde=True, ax=ax, color="#fbb8ac")
            st.pyplot(fig)

            st.subheader("💰 Spending Patterns")
            fig2, ax2 = plt.subplots()
            sns.boxplot(x=df['Amount Spent'], ax=ax2, color="#fac8b4")
            st.pyplot(fig2)

            # Email PDF option
            if st.checkbox("📤 Email me this report"):
                email = st.text_input("Enter your email")
                if st.button("Send Report"):
                    summary = df.describe().to_string()
                    send_email_with_pdf("DinePsych Report", email, f"Customer Behavior Analysis\n\n{summary}")

            increment_usage("DinePsych")
        else:
            st.warning("❗ Required columns: 'Visit Time' and 'Amount Spent'")
else:
    st.error("⚠️ You've reached the usage limit for DinePsych.")

st.info("""
🧠 *Note:* The insights provided by this tool are generated using AI and public data. While helpful, they may not reflect 100% accuracy or real-time changes. Always consult professionals before making critical decisions.
""")

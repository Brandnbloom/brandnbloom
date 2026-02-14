import streamlit as st
from utils import can_use_tool, increment_usage, send_email_with_pdf
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="DinePsych", layout="wide")
st.title("🧠 DinePsych – Customer Behavior Decoder")

if can_use_tool("DinePsych"):
    st.subheader("📋 Customer Behavior Questionnaire")

    with st.form("dinepsych_form"):
        visits_per_day = st.slider("Average number of customer visits per day", 10, 300, 50)
        peak_hour = st.selectbox("Busiest time of day", ["Morning", "Afternoon", "Evening", "Night"])
        avg_spend = st.number_input("Average spend per customer ($)", min_value=1, max_value=500, value=25)
        weekend_boost = st.slider("Weekend traffic increase (%)", 0, 200, 50)
        loyalty_rate = st.slider("Percentage of repeat customers", 0, 100, 40)
        
        submitted = st.form_submit_button("Generate Insights")

    if submitted:
        # Create fake dataset based on answers
        hours_map = {"Morning": 9, "Afternoon": 14, "Evening": 19, "Night": 22}
        df = pd.DataFrame({
            "Hour": [hours_map[peak_hour]] * visits_per_day,
            "Amount Spent": [avg_spend] * visits_per_day
        })

        # Visit Time Distribution
        st.subheader("🕓 Visit Time Distribution")
        fig, ax = plt.subplots()
        sns.histplot(df['Hour'], bins=24, kde=True, ax=ax, color="#fbb8ac")
        st.pyplot(fig)

        # Spending Patterns
        st.subheader("💰 Spending Patterns")
        fig2, ax2 = plt.subplots()
        sns.boxplot(x=df['Amount Spent'], ax=ax2, color="#fac8b4")
        st.pyplot(fig2)

        # Insights
        st.markdown(f"""
        **📊 Insights:**
        - Your busiest time is around **{peak_hour}**.
        - Average spend per customer is **${avg_spend}**.
        - Weekend traffic boosts your sales by **{weekend_boost}%**.
        - **{loyalty_rate}%** of your customers are repeat visitors.
        """)

        # Email PDF
        if st.checkbox("📤 Email me this report"):
            email = st.text_input("Enter your email")
            if st.button("Send Report"):
                report_text = f"""
                Customer Behavior Analysis:
                - Busiest Time: {peak_hour}
                - Average Spend: ${avg_spend}
                - Weekend Boost: {weekend_boost}%
                - Loyalty Rate: {loyalty_rate}%
                """
                send_email_with_pdf("DinePsych Report", email, report_text)

        increment_usage("DinePsych")
else:
    st.error("⚠️ You've reached the usage limit for DinePsych.")

st.info("""
🧠 *Note:* These insights are based on the questionnaire responses you provided and may not reflect actual customer data.
""")

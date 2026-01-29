import streamlit as st
import pandas as pd
from services.customer_api import get_customer_data
import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

def save_to_dashboard(tool_name, df):
    if "dashboard_data" not in st.session_state:
        st.session_state["dashboard_data"] = {}
    st.session_state["dashboard_data"][tool_name] = df

def visualize_data(tool_name, df):
    st.subheader("📊 Visualizations")
    st.line_chart(df[["CustomerID", "CLV"]].set_index("CustomerID"))

def generate_ai_caption(tool_name, df):
    try:
        prompt = f"Provide insights from {tool_name} dataset: {df.head(10).to_dict()}"
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=150
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"AI caption failed: {e}"

def run():
    st.header("💰 Customer Lifetime Value (CLV) Calculator")

    if st.button("Fetch & Calculate CLV"):
        with st.spinner("Fetching real customer data..."):
            df = get_customer_data()

        if df.empty:
            st.warning("No customer data available.")
            return

        st.success("✅ Customer data loaded!")
        st.dataframe(df.head(10))

          # ---------------- Check usage ----------------
    from streamlit_app import check_usage
    if not check_usage("CLV Calculator"):
        st.stop()  # Stop the tool if free limit reached

    # ---------------- Tool logic ----------------
    uploaded_file = st.file_uploader("Upload Customer Data", type=['csv'])
    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        st.success("Data loaded successfully!")
        # Your clv calculator logic here...

        # ---------------- CLV Calculation ----------------
        # Simple CLV = Average purchase value * Purchase frequency * 12 months (simplified)
        df["AveragePurchaseValue"] = df.get("TotalSpent", 0) / df.get("NumberOfPurchases", 1)
        df["CLV"] = df["AveragePurchaseValue"] * df.get("NumberOfPurchases", 0)

        save_to_dashboard("clv", df)
        visualize_data("clv", df)

        # AI Insight
        df["AI_Insight"] = generate_ai_caption("CLV", df)
        save_to_dashboard("clv", df)

        # Export CSV
        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="📥 Download CLV CSV",
            data=csv,
            file_name="clv.csv",
            mime="text/csv"
        )

import streamlit as st
from services.customer_api import get_customer_data
from utils.dashboard import save_to_dashboard
from utils.visualization import visualize_data
from services.openai_api import generate_ai_caption

def run():
    st.subheader("Customer Churn & CLV")

    df = get_customer_data()
    st.dataframe(df)

    churn_df = df.assign(churn_risk=df["last_purchase_days"] > 90)
    clv_df = df.assign(CLV=df["revenue"] * 2.5)

    save_to_dashboard("churn", churn_df)
    save_to_dashboard("clv", clv_df)

    visualize_data("churn", churn_df)
    visualize_data("clv", clv_df)

    st.success(generate_ai_caption("churn", churn_df))
    st.success(generate_ai_caption("clv", clv_df))


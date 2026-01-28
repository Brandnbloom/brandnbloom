import pandas as pd
import streamlit as st
from datetime import datetime

from utils.session import get_user_id
from utils.usage_limiter import can_use_tool, increment_usage, show_limit_message

def load_ga4_data():
    return pd.DataFrame([
        {"email": "a@test.com", "last_active": "2026-01-10", "sessions": 5},
        {"email": "b@test.com", "last_active": "2026-01-05", "sessions": 2},
    ])


def load_stripe_data():
    return pd.DataFrame([
        {"email": "a@test.com", "total_spent": 12000, "purchases": 3},
        {"email": "b@test.com", "total_spent": 3000, "purchases": 1},
    ])
def build_customer_360():
    df_ga = load_ga4_data()
    df_stripe = load_stripe_data()

    df = df_ga.merge(df_stripe, on="email", how="left")
    df["total_spent"] = df["total_spent"].fillna(0)
    df["purchases"] = df["purchases"].fillna(0)

    return df

def calculate_rfm(df):
    today = datetime.today()

    df["last_active"] = pd.to_datetime(df["last_active"])
    df["recency"] = (today - df["last_active"]).dt.days
    df["frequency"] = df["purchases"]
    df["monetary"] = df["total_spent"]

    # Simple scoring (1–5)
    df["R"] = pd.qcut(df["recency"], 5, labels=[5,4,3,2,1])
    df["F"] = pd.qcut(df["frequency"].rank(method="first"), 5, labels=[1,2,3,4,5])
    df["M"] = pd.qcut(df["monetary"], 5, labels=[1,2,3,4,5])

    df["RFM_SCORE"] = df["R"].astype(str) + df["F"].astype(str) + df["M"].astype(str)

    return df
def run_customer_360_tool():
    user_id = get_user_id()

    if not can_use_tool():
        show_limit_message()

    df = build_customer_360()
    df = calculate_rfm(df)

    increment_usage()

    st.success("✅ Customer 360 + RFM Generated")
    st.dataframe(df)

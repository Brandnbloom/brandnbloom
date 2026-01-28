import pandas as pd
import streamlit as st
from datetime import datetime

from sklearn.preprocessing import MinMaxScaler
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

# Internal
from utils.usage_limiter import check_usage
from utils.dashboard import save_to_dashboard


# -------------------------------------------------
# Merge GA + Stripe + Meta
# -------------------------------------------------

def build_customer_360(df_ga, df_razorpay, df_meta):

    df = df_ga.merge(df_razorpay, on="email", how="left")
    df = df.merge(df_meta, on="email", how="left")

    df.fillna(0, inplace=True)
    return df


# -------------------------------------------------
# RFM
# -------------------------------------------------

def calculate_rfm(df):

    df["last_purchase"] = pd.to_datetime(df["last_purchase"])

    df["Recency"] = (pd.Timestamp.today() - df["last_purchase"]).dt.days
    df["Frequency"] = df["num_purchases"]
    df["Monetary"] = df["total_spent"]

    scaler = MinMaxScaler()
    df[["R", "F", "M"]] = scaler.fit_transform(df[["Recency", "Frequency", "Monetary"]])

    df["RFM_Score"] = df["R"] + df["F"] + df["M"]

    return df


# -------------------------------------------------
# CLV
# -------------------------------------------------

def calculate_clv(df):

    avg_order = df["total_spent"] / df["num_purchases"].replace(0, 1)
    lifespan = 12  # months assumption

    df["CLV"] = avg_order * df["num_purchases"] * lifespan

    return df


# -------------------------------------------------
# Churn Label
# -------------------------------------------------

def label_churn(df, days=90):

    df["Churn"] = df["Recency"].apply(lambda x: 1 if x > days else 0)
    return df


# -------------------------------------------------
# Train churn ML
# -------------------------------------------------

def train_churn_model(df):

    X = df[["Recency", "Frequency", "Monetary"]]
    y = df["Churn"]

    model = LogisticRegression()
    model.fit(X, y)

    df["Churn_Probability"] = model.predict_proba(X)[:, 1]

    return df


# -------------------------------------------------
# MAIN TOOL
# -------------------------------------------------

def run_customer_360_rfm_tool(df_ga, df_razorpay, df_meta):

    st.title("🧠 Customer 360 + RFM + CLV + Churn")

    if not check_usage("customer_360"):
        st.warning("Free limit reached. Please upgrade.")
        return

    df = build_customer_360(df_ga, df_stripe, df_meta)
    df = calculate_rfm(df)
    df = calculate_clv(df)
    df = label_churn(df)
    df = train_churn_model(df)

    st.dataframe(df)

    save_to_dashboard(
        tool_name="Customer 360 + RFM + CLV + Churn",
        dataframe=df
    )

    st.success("✅ Customer intelligence generated!")

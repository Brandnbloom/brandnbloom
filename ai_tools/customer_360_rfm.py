import pandas as pd
import streamlit as st
from datetime import datetime
import numpy as np

# ML
from sklearn.preprocessing import MinMaxScaler
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

# Internal
from utils.usage_limiter import check_usage, can_use_tool, increment_usage, show_limit_message
from utils.dashboard import save_to_dashboard

from utils.session import get_user_id

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
def build_customer_360(df_ga, df_stripe, df_meta):
    """
    Merge GA + Stripe + Meta data
    """
    df = df_ga.merge(df_stripe, on="email", how="left")
    df = df.merge(df_meta, on="email", how="left")

    df.fillna(0, inplace=True)
    return df


    return df

def calculate_rfm(df):
    df["Recency"] = (pd.Timestamp.today() - pd.to_datetime(df["last_purchase"])).dt.days
    df["Frequency"] = df["num_purchases"]
    df["Monetary"] = df["total_spent"]

    scaler = MinMaxScaler()
    df[["R", "F", "M"]] = scaler.fit_transform(df[["Recency", "Frequency", "Monetary"]])

    df["RFM_Score"] = df["R"] + df["F"] + df["M"]
    return df

def calculate_clv(df):
    """
    Simple CLV formula
    """
    avg_order_value = df["total_spent"] / df["num_purchases"].replace(0, 1)
    purchase_frequency = df["num_purchases"]
    customer_lifespan = 12  # months (assumption)

    df["CLV"] = avg_order_value * purchase_frequency * customer_lifespan
    return df

def label_churn(df, churn_days=90):
    """
    If no purchase in last 90 days → churn = 1
    """
    df["Churn"] = df["Recency"].apply(lambda x: 1 if x > churn_days else 0)
    return df

def train_churn_model(df):
    features = df[["Recency", "Frequency", "Monetary"]]
    target = df["Churn"]

    X_train, X_test, y_train, y_test = train_test_split(
        features, target, test_size=0.2, random_state=42
    )

    model = LogisticRegression()
    model.fit(X_train, y_train)

    df["Churn_Probability"] = model.predict_proba(features)[:, 1]
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

def run_customer_360_rfm_tool(df_ga, df_stripe, df_meta):
    st.title("Customer 360 + RFM + CLV + Churn")

    # 🔒 Usage check
    if not check_usage("customer_360"):
        st.warning("Free limit reached. Please upgrade.")
        return

    # 🧠 Pipeline
    df = build_customer_360(df_ga, df_stripe, df_meta)
    df = calculate_rfm(df)
    df = calculate_clv(df)
    df = label_churn(df)
    df = train_churn_model(df)

    # 📊 Display
    st.dataframe(df)

    # 💾 Save to dashboard
    save_to_dashboard(
        tool_name="Customer 360 + RFM + CLV + Churn",
        dataframe=df
    )

    st.success("Customer intelligence generated successfully!")


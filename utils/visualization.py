import streamlit as st
import plotly.express as px
import pandas as pd


# ---------------- KPI CARDS ----------------

def show_kpis(df):

    col1, col2, col3, col4 = st.columns(4)

    total_customers = len(df)
    avg_clv = round(df["CLV"].mean(),2) if "CLV" in df else 0
    churn = round(df["Churn_Probability"].mean()*100,2) if "Churn_Probability" in df else 0
    revenue = round(df["total_spent"].sum(),2) if "total_spent" in df else 0

    col1.metric("Customers", total_customers)
    col2.metric("Avg CLV", avg_clv)
    col3.metric("Churn %", churn)
    col4.metric("Revenue", revenue)


# ---------------- GENERIC BAR ----------------

def show_numeric_bar_chart(df, title):

    numeric = df.select_dtypes(include="number")

    if numeric.empty:
        return

    fig = px.bar(numeric, title=title)
    st.plotly_chart(fig, use_container_width=True)


# ---------------- CLV ----------------

def show_clv_chart(df):

    if "CLV" not in df.columns:
        return

    fig = px.line(df, y="CLV", title="Customer Lifetime Value")
    st.plotly_chart(fig, use_container_width=True)


# ---------------- CHURN ----------------

def show_churn_chart(df):

    if "Churn_Probability" not in df.columns:
        return

    fig = px.histogram(df, x="Churn_Probability", title="Churn Probability")
    st.plotly_chart(fig, use_container_width=True)


# ---------------- FUNNEL ----------------

def show_funnel(df):

    if not all(col in df.columns for col in ["sessions","num_purchases"]):
        return

    funnel = pd.DataFrame({
        "Stage":["Visitors","Buyers"],
        "Count":[df["sessions"].sum(),df["num_purchases"].sum()]
    })

    fig = px.funnel(funnel, x="Count", y="Stage", title="Conversion Funnel")
    st.plotly_chart(fig, use_container_width=True)


# ---------------- COHORT ----------------

def show_cohort(df):

    if "last_purchase" not in df.columns:
        return

    df["month"] = pd.to_datetime(df["last_purchase"]).dt.to_period("M")

    cohort = df.groupby("month")["email"].count().reset_index()

    fig = px.bar(cohort, x="month", y="email", title="Customer Cohort Growth")
    st.plotly_chart(fig, use_container_width=True)

import streamlit as st
import plotly.express as px


def show_numeric_bar_chart(df, title="Metrics"):

    numeric = df.select_dtypes(include="number")

    if numeric.empty:
        st.info("No numeric data available")
        return

    fig = px.bar(numeric, title=title)
    st.plotly_chart(fig, use_container_width=True)


def show_clv_chart(df):

    if "CLV" not in df.columns:
        return

    fig = px.line(df, y="CLV", title="Customer Lifetime Value")
    st.plotly_chart(fig, use_container_width=True)


def show_churn_chart(df):

    if "Churn_Probability" not in df.columns:
        return

    fig = px.histogram(df, x="Churn_Probability", title="Churn Probability Distribution")
    st.plotly_chart(fig, use_container_width=True)

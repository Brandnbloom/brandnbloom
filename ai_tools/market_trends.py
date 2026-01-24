import streamlit as st
import pandas as pd
import plotly.express as px

def run_market_trends():
    st.subheader("🌊 Market Trend Analyzer")

    uploaded_file = st.file_uploader("Upload Sales/Market Data (CSV)", type=['csv'])
    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        st.write("Data Preview", df.head())

        if st.button("Analyze Trends"):
            fig = px.line(df, x='date', y='value', color='category', title="Market Trends")
            st.plotly_chart(fig)

            st.download_button(
                "📥 Download Trends CSV",
                data=df.to_csv(index=False),
                file_name="market_trends.csv",
                mime="text/csv"
            )
    else:
        # Sample
        sample = pd.DataFrame({
            "date": pd.date_range(start="2026-01-01", periods=5),
            "category": ["A","B","A","B","A"],
            "value": [100, 120, 110, 130, 125]
        })
        st.download_button(
            "📥 Download Sample Data",
            data=sample.to_csv(index=False),
            file_name="sample_market_trends.csv",
            mime="text/csv"
        )


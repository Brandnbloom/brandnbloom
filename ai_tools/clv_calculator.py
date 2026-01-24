import streamlit as st
import pandas as pd
import numpy as np

def run_clv_calculator():
    st.subheader("💰 Customer Lifetime Value Calculator")

    uploaded_file = st.file_uploader("Upload transaction data (CSV)", type=['csv'])
    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        st.write("Data Preview", df.head())

        if st.button("Calculate CLV"):
            df['clv'] = df['monetary'] * df['frequency'] / df['recency']
            st.write("CLV Results", df[['customer_id', 'clv']])

            st.download_button(
                "📥 Download CLV CSV",
                data=df.to_csv(index=False),
                file_name="clv_results.csv",
                mime="text/csv"
            )
    else:
        # Sample
        sample = pd.DataFrame({
            "customer_id": [1, 2, 3],
            "recency": [10, 20, 5],
            "frequency": [3, 1, 5],
            "monetary": [200, 150, 500]
        })
        st.download_button(
            "📥 Download Sample Data",
            data=sample.to_csv(index=False),
            file_name="sample_clv.csv",
            mime="text/csv"
        )
save_to_dashboard("clv", df)



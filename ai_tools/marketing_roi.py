import streamlit as st
import pandas as pd
import plotly.express as px

def run_marketing_roi():
    st.subheader("📊 Marketing ROI Tracker")

    uploaded_file = st.file_uploader("Upload Campaign Data (CSV)", type=['csv'])
    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        st.write("Data Preview", df.head())

        if st.button("Calculate ROI"):
            # Simple ROI: revenue / cost
            df['roi'] = df['revenue'] / df['cost']
            st.write(df[['campaign', 'roi']])

            fig = px.bar(df, x='campaign', y='roi', color='campaign', title="Campaign ROI")
            st.plotly_chart(fig)

            st.download_button(
                "📥 Download ROI CSV",
                data=df.to_csv(index=False),
                file_name="roi_results.csv",
                mime="text/csv"
            )
    else:
        # Sample
        sample = pd.DataFrame({
            "campaign": ["C1","C2","C3"],
            "revenue": [1000, 1500, 1200],
            "cost": [500, 700, 600]
        })
        st.download_button(
            "📥 Download Sample Data",
            data=sample.to_csv(index=False),
            file_name="sample_roi.csv",
            mime="text/csv"
        )
save_to_dashboard("roi", df)

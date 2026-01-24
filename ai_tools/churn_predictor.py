import streamlit as st
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

def run_churn_predictor():
    st.subheader("📉 Churn Predictor (Machine Learning)")

    uploaded_file = st.file_uploader("Upload Customer Data (CSV)", type=['csv'])
    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        st.write("Data Preview", df.head())

        if st.button("Predict Churn"):
            X = df.drop('churn', axis=1)
            y = df['churn']

            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
            model = RandomForestClassifier()
            model.fit(X_train, y_train)
            score = model.score(X_test, y_test)

            st.success(f"Accuracy: {score*100:.2f}%")
    else:
        # Sample
        sample = pd.DataFrame({
            "recency": [10, 5, 20],
            "frequency": [3, 6, 1],
            "monetary": [200, 500, 150],
            "churn": [0, 0, 1]
        })
        st.download_button(
            "📥 Download Sample Data",
            data=sample.to_csv(index=False),
            file_name="sample_churn.csv",
            mime="text/csv"
        )


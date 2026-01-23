import streamlit as st
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

sample_data = pd.DataFrame({
    "customer_id": [1,2,3],
    "recency": [10, 20, 5],
    "frequency": [3, 1, 5],
    "monetary": [200, 150, 500],
    "churn": [0, 1, 0]
})

st.download_button(
    "📥 Download Sample Data",
    data=sample_data.to_csv(index=False),
    file_name="sample_data.csv",
    mime="text/csv"
)

def run_churn_predictor():
    st.subheader("📉 Churn Prediction Model")

    uploaded_file = st.file_uploader("Upload Customer Data (CSV)", type=["csv"])
    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        st.write("Data Loaded Successfully!", df.head())

        if st.button("Run Prediction"):
            X = df.drop("churn", axis=1)
            y = df["churn"]

            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
            model = RandomForestClassifier()
            model.fit(X_train, y_train)
            score = model.score(X_test, y_test)

            st.success(f"Model Accuracy: {score*100:.2f}%")


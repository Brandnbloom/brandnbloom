import streamlit as st
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from services.customer_api import get_customer_data
from streamlit_app import save_to_dashboard, visualize_data, generate_ai_caption

def run():
    st.header("📉 Churn Predictor - Real Customer Data")

    limit = st.number_input("Number of customers to fetch", min_value=100, max_value=10000, value=500)
    if st.button("Fetch & Predict Churn"):
        with st.spinner("Fetching customer data..."):
            df = get_customer_data(limit=limit)
        
        if df.empty:
            st.warning("No customer data available.")
            return

        st.success("✅ Customer data loaded!")
        st.dataframe(df.head(10))

        # ------------------- Feature Engineering -------------------
        df["Recency"] = (pd.Timestamp.now() - pd.to_datetime(df["LastPurchaseDate"])).dt.days
        df["Frequency"] = df["NumberOfPurchases"]
        df["Monetary"] = df["TotalSpent"]

        features = ["Recency", "Frequency", "Monetary"]
        X = df[features]

        # If ChurnFlag exists, we can do supervised learning
        if "ChurnFlag" in df.columns:
            y = df["ChurnFlag"]
        else:
            st.info("ChurnFlag not found, creating pseudo churn (top 20% least active).")
            threshold = X["Recency"].quantile(0.8)
            y = (X["Recency"] > threshold).astype(int)

        # ------------------- Train/Test Split -------------------
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        model = RandomForestClassifier(n_estimators=100, random_state=42)
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        acc = accuracy_score(y_test, y_pred)

        st.metric("Prediction Accuracy", f"{acc*100:.2f}%")

        # ------------------- Prediction on All Customers -------------------
        df["ChurnPrediction"] = model.predict(X)
        save_to_dashboard("churn", df)
        visualize_data("churn", df)

        # ------------------- AI Caption -------------------
        caption = generate_ai_caption("churn", df)
        st.success(f"💡 AI Insight: {caption}")

        # ------------------- Export -------------------
        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="📥 Download Churn Predictions CSV",
            data=csv,
            file_name="churn_predictions.csv",
            mime="text/csv"
        )

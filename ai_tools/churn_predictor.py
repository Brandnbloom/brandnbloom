import streamlit as st
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from services.customer_api import get_customer_data
import openai
import os

# Load OpenAI API Key
openai.api_key = os.getenv("OPENAI_API_KEY")

# ------------------ Helper Functions ------------------

def save_to_dashboard(tool_name, df):
    if "dashboard_data" not in st.session_state:
        st.session_state["dashboard_data"] = {}
    st.session_state["dashboard_data"][tool_name] = df

def visualize_data(tool_name, df):
    st.subheader("📊 Visualizations")
    st.bar_chart(df[["Recency", "Frequency", "Monetary"]].fillna(0))

def generate_ai_caption(tool_name, df):
    """
    Generate AI caption/insight using GPT API
    """
    try:
        prompt = f"Summarize insights from {tool_name} dataset: {df.head(10).to_dict()}"
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=150
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"AI caption failed: {e}"

# ------------------ Main Function ------------------

def run():
    st.header("📉 Churn Predictor - Real Customer Data")

    if st.button("Fetch & Predict Churn"):
        with st.spinner("Fetching real customer data..."):
            df = get_customer_data()

        if df.empty:
            st.warning("No customer data available.")
            return

        st.success("✅ Customer data loaded!")
        st.dataframe(df.head(10))

        # ---------------- Feature Engineering ----------------
        df["Recency"] = (pd.Timestamp.now() - pd.to_datetime(df.get("LastPurchaseDate", pd.Timestamp.now()))).dt.days
        df["Frequency"] = df.get("NumberOfPurchases", 0)
        df["Monetary"] = df.get("TotalSpent", 0)

        features = ["Recency", "Frequency", "Monetary"]
        X = df[features]

        # Create pseudo churn if not present
        if "ChurnFlag" in df.columns:
            y = df["ChurnFlag"]
        else:
            threshold = X["Recency"].quantile(0.8)
            y = (X["Recency"] > threshold).astype(int)

        # ---------------- Model ----------------
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        model = RandomForestClassifier(n_estimators=100, random_state=42)
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        acc = accuracy_score(y_test, y_pred)
        st.metric("Prediction Accuracy", f"{acc*100:.2f}%")

        # Predict for all
        df["ChurnPrediction"] = model.predict(X)
        save_to_dashboard("churn", df)
        visualize_data("churn", df)

        # AI Insight
        caption = generate_ai_caption("churn", df)
        st.success(f"💡 AI Insight: {caption}")

        # Export CSV
        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="📥 Download Churn Predictions CSV",
            data=csv,
            file_name="churn_predictions.csv",
            mime="text/csv"
        )


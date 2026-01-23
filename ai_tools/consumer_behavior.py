import streamlit as st
import pandas as pd
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer

# Download once (safe even if repeated)
nltk.download("vader_lexicon")

def analyze_sentiment(text):
    sia = SentimentIntensityAnalyzer()
    score = sia.polarity_scores(str(text))["compound"]

    if score >= 0.05:
        return "Positive"
    elif score <= -0.05:
        return "Negative"
    else:
        return "Neutral"

def run():
    st.markdown("## 🧠 Consumer Behavior & Sentiment Analysis")
    st.markdown("Analyze real customer feedback from Google Forms.")

    uploaded_file = st.file_uploader(
        "Upload Google Form responses (CSV)",
        type=["csv"]
    )

    st.session_state["consumer_insights"] = {
    "total_responses": len(df),
    "positive": int((df["Sentiment"] == "Positive").sum()),
    "neutral": int((df["Sentiment"] == "Neutral").sum()),
    "negative": int((df["Sentiment"] == "Negative").sum()),
}

# Optional: Save to file
df.to_csv("data/consumer_sentiment_latest.csv", index=False)

st.success("Insights saved for Dashboard & AI captions")

    if uploaded_file:
        df = pd.read_csv(uploaded_file)

        st.markdown("### 📋 Raw Responses")
        st.dataframe(df, use_container_width=True)

        # Select text column for sentiment
        text_columns = df.select_dtypes(include="object").columns.tolist()

        if not text_columns:
            st.warning("No text columns found for sentiment analysis.")
            return

        text_col = st.selectbox(
            "Select column to analyze sentiment",
            text_columns
        )

        if st.button("Analyze Sentiment"):
            df["Sentiment"] = df[text_col].apply(analyze_sentiment)

            st.markdown("### 📊 Sentiment Distribution")
            st.bar_chart(df["Sentiment"].value_counts())

            st.markdown("### 😊 Positive Feedback")
            st.write(df[df["Sentiment"] == "Positive"][text_col].head(5))

            st.markdown("### 😐 Neutral Feedback")
            st.write(df[df["Sentiment"] == "Neutral"][text_col].head(5))

            st.markdown("### 😞 Negative Feedback")
            st.write(df[df["Sentiment"] == "Negative"][text_col].head(5))

            st.success("✅ Sentiment analysis completed using real NLP.")

from services.storage import save_insights

insights = {
    "total": len(df),
    "positive": int((df["Sentiment"] == "Positive").sum()),
    "neutral": int((df["Sentiment"] == "Neutral").sum()),
    "negative": int((df["Sentiment"] == "Negative").sum()),
}

save_insights(insights)
st.session_state["consumer_insights"] = insights


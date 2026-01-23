import streamlit as st
import requests
from bs4 import BeautifulSoup
import re
from textblob import TextBlob
import pandas as pd

def run():
    st.markdown("## 🧠 Consumer Behavior Analysis")
    st.markdown("Upload real customer responses from Google Forms.")

    uploaded_file = st.file_uploader(
        "Upload Google Form responses (CSV)",
        type=["csv"]
    )

    if uploaded_file:
        df = pd.read_csv(uploaded_file)

        st.markdown("### 📋 Raw Responses")
        st.dataframe(df, use_container_width=True)

        st.markdown("### 🔍 Key Insights")

        # Example insights (REAL DATA driven)
        if "Would you recommend this brand?" in df.columns:
            rec_counts = df["Would you recommend this brand?"].value_counts()
            st.bar_chart(rec_counts)

        if "What frustrates you?" in df.columns:
            st.markdown("#### Common Frustrations")
            st.write(df["What frustrates you?"].dropna().head(10))

        if "What do you like most?" in df.columns:
            st.markdown("#### What Customers Love")
            st.write(df["What do you like most?"].dropna().head(10))

        st.success("✅ Live consumer behavior insights generated!")


# -------------------------------------------------
# TEXT CLEANING
# -------------------------------------------------
def clean_text(text):
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"[^a-zA-Z0-9 .,!?]", "", text)
    return text.strip()


# -------------------------------------------------
# BEHAVIOR ANALYSIS ENGINE
# -------------------------------------------------
def analyze_consumer_behavior(url, audience, product_type):
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")

        # Extract visible text
        texts = " ".join(
            [p.get_text() for p in soup.find_all(["p", "h1", "h2", "h3"])]
        )
        texts = clean_text(texts)

        blob = TextBlob(texts)
        sentiment = blob.sentiment.polarity

        # Sentiment mapping
        if sentiment > 0.25:
            emotion = "Positive & Trust-Building"
        elif sentiment < -0.1:
            emotion = "Confusing or Emotionally Weak"
        else:
            emotion = "Neutral / Informational"

        # CTA detection
        ctas = re.findall(
            r"(buy now|sign up|get started|contact us|book now|try free)",
            texts.lower()
        )

        # Awareness stage
        if "why" in texts.lower() or "problem" in texts.lower():
            stage = "Awareness (Problem-aware)"
        elif ctas:
            stage = "Decision-ready"
        else:
            stage = "Consideration"

        # Trust signals
        trust_keywords = [
            "testimonials", "reviews", "clients", "trusted",
            "years", "experience", "certified"
        ]
        trust_score = sum(
            1 for k in trust_keywords if k in texts.lower()
        )

        # Friction indicators
        friction = []
        if len(texts) < 400:
            friction.append("Low information depth")
        if not ctas:
            friction.append("No strong CTA")
        if trust_score < 2:
            friction.append("Weak trust signals")

        return {
            "emotion": emotion,
            "sentiment_score": round(sentiment, 2),
            "buyer_stage": stage,
            "cta_count": len(ctas),
            "trust_score": trust_score,
            "friction": friction,
            "summary": f"""
Audience: {audience}
Product Type: {product_type}

Visitors feel: {emotion}
They are in: {stage}

Main blockers:
{', '.join(friction) if friction else 'No major friction detected'}
"""
        }

    except Exception as e:
        return {"error": str(e)}


# -------------------------------------------------
# STREAMLIT UI
# -------------------------------------------------
def run():
    st.markdown("## 🧠 Consumer Behavior Analysis")
    st.markdown(
        "Understand **how your consumers think, feel, and decide** using real behavioral signals."
    )

    st.divider()

    url = st.text_input("Website URL", placeholder="https://yourwebsite.com")
    audience = st.selectbox("Target Audience", ["B2C", "B2B"])
    product_type = st.selectbox(
        "Offering Type", ["Product", "Service", "SaaS"]
    )

    if st.button("Analyze Consumer Behavior"):
        if not url:
            st.warning("Please enter a website URL.")
            return

        with st.spinner("Reading consumer signals..."):
            result = analyze_consumer_behavior(url, audience, product_type)

        if "error" in result:
            st.error(result["error"])
            return

        st.divider()
        st.subheader("🔍 Consumer Insights")

        st.metric("Emotional Tone", result["emotion"])
        st.metric("Buyer Stage", result["buyer_stage"])
        st.metric("CTA Strength", result["cta_count"])
        st.metric("Trust Signals", result["trust_score"])

        st.divider()
        st.markdown("### 🚧 Conversion Friction")
        if result["friction"]:
            for f in result["friction"]:
                st.write("•", f)
        else:
            st.success("No major friction detected")

        st.divider()
        st.markdown("### 🧠 Behavioral Summary")
        st.write(result["summary"])

        st.caption(
            "Insights generated using live content psychology & consumer behavior models."
        )

import streamlit as st
import requests
from bs4 import BeautifulSoup
import re
from textblob import TextBlob
from textstat import flesch_reading_ease


# -------------------------------------------------
# UTILITIES
# -------------------------------------------------
def extract_text(url):
    response = requests.get(url, timeout=10)
    soup = BeautifulSoup(response.text, "html.parser")
    text = " ".join(
        [t.get_text() for t in soup.find_all(["p", "h1", "h2", "h3", "li"])]
    )
    return re.sub(r"\s+", " ", text).strip()


# -------------------------------------------------
# BLOOMSCORE ENGINE
# -------------------------------------------------
def calculate_bloomscore(url):
    text = extract_text(url)
    text_lower = text.lower()

    # 1️⃣ Clarity
    clarity_keywords = ["we help", "our mission", "we provide", "solution", "problem"]
    clarity_score = sum(1 for k in clarity_keywords if k in text_lower) * 10
    clarity_score = min(clarity_score, 100)

    # 2️⃣ Trust
    trust_keywords = [
        "trusted", "clients", "testimonials", "reviews",
        "years of experience", "certified", "award"
    ]
    trust_score = sum(1 for k in trust_keywords if k in text_lower) * 12
    trust_score = min(trust_score, 100)

    # 3️⃣ CTA Strength
    ctas = re.findall(
        r"(get started|sign up|book now|contact us|try free|buy now)",
        text_lower
    )
    cta_score = min(len(ctas) * 20, 100)

    # 4️⃣ Consistency
    headings = re.findall(r"(h1|h2|h3)", text_lower)
    consistency_score = 80 if len(headings) >= 5 else 50

    # 5️⃣ Emotional Tone
    sentiment = TextBlob(text).sentiment.polarity
    emotional_score = int((sentiment + 1) * 50)

    # 6️⃣ Readability
    readability = flesch_reading_ease(text)
    if readability > 60:
        ux_score = 90
    elif readability > 40:
        ux_score = 70
    else:
        ux_score = 40

    # Final BloomScore
    bloomscore = int(
        (clarity_score + trust_score + cta_score +
         consistency_score + emotional_score + ux_score) / 6
    )

    return {
        "BloomScore": bloomscore,
        "Clarity": clarity_score,
        "Trust": trust_score,
        "CTA": cta_score,
        "Consistency": consistency_score,
        "Emotion": emotional_score,
        "UX Readability": ux_score,
        "Sentiment": round(sentiment, 2)
    }


# -------------------------------------------------
# STREAMLIT UI
# -------------------------------------------------
def run():
    st.markdown("## 🌸 BloomScore")
    st.markdown(
        "Your **live brand health score** based on consumer psychology & content clarity."
    )

    st.divider()

    url = st.text_input("Website URL", placeholder="https://yourbrand.com")

    if st.button("Generate BloomScore"):
        if not url:
            st.warning("Please enter a website URL.")
            return

        with st.spinner("Calculating brand health..."):
            try:
                result = calculate_bloomscore(url)
            except Exception as e:
                st.error(f"Analysis failed: {e}")
                return

        st.divider()

        st.metric("🌸 BloomScore", f"{result['BloomScore']} / 100")

        col1, col2, col3 = st.columns(3)
        col1.metric("Clarity", result["Clarity"])
        col1.metric("Trust", result["Trust"])

        col2.metric("CTA Strength", result["CTA"])
        col2.metric("Consistency", result["Consistency"])

        col3.metric("Emotion", result["Emotion"])
        col3.metric("UX Readability", result["UX Readability"])

        st.divider()
        st.caption(
            "BloomScore uses live website content, behavioral psychology & NLP analysis."
        )

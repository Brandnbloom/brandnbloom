# ai_tools/ocr_sentiment.py

from textblob import TextBlob
from typing import Dict

def analyze_text_sentiment(text: str) -> Dict[str, str]:
    """
    Analyzes sentiment of the given text.
    Returns polarity (positive, neutral, negative) and score (-1 to 1)
    """
    blob = TextBlob(text)
    score = blob.sentiment.polarity

    if score > 0.1:
        sentiment = "Positive"
    elif score < -0.1:
        sentiment = "Negative"
    else:
        sentiment = "Neutral"

    return {
        "sentiment": sentiment,
        "score": round(score, 2)
    }

# brandnbloom/ai_tools/ocr_sentiment.py

from typing import Dict
from io import BytesIO
from PIL import Image
import pytesseract

# Optional: simple sentiment via TextBlob (install textblob)
try:
    from textblob import TextBlob
except Exception:
    TextBlob = None


def extract_text_from_image(img_bytes: bytes) -> str:
    """
    Extract text from an uploaded image using Tesseract OCR.

    Parameters:
        img_bytes (bytes): Raw image bytes

    Returns:
        str: Extracted text
    """
    image = Image.open(BytesIO(img_bytes)).convert("RGB")
    return pytesseract.image_to_string(image)


def sentiment_of_text(text: str) -> Dict:
    """
    Returns a sentiment analysis dictionary.

    If TextBlob is available:
        - polarity: -1 to 1
        - subjectivity: 0 to 1

    If TextBlob is NOT available:
        - Uses a basic word-list heuristic.

    Parameters:
        text (str): text to analyze

    Returns:
        dict: sentiment metrics
    """
    if not text:
        return {
            "polarity": 0.0,
            "subjectivity": 0.0,
            "summary": "No text found"
        }

    # If TextBlob is NOT installed → fallback to heuristic
    if TextBlob is None:
        positives = ["good", "great", "love", "amazing", "beautiful", "nice"]
        negatives = ["bad", "angry", "hate", "terrible", "ugly"]

        t = text.lower()
        score = sum(t.count(w) for w in positives) - sum(t.count(w) for w in negatives)
        polarity = max(-1.0, min(1.0, score / 5.0))

        return {
            "polarity": polarity,
            "subjectivity": 0.5,
            "summary": "Heuristic sentiment"
        }

    # Full TextBlob sentiment
    tb = TextBlob(text)
    return {
        "polarity": tb.sentiment.polarity,
        "subjectivity": tb.sentiment.subjectivity,
        "summary": "TextBlob result"
    }

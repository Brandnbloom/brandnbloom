# brandnbloom/ai_tools/ocr_sentiment.py
from typing import Dict
from io import BytesIO
from PIL import Image
import pytesseract

# Optional: simple sentiment via TextBlob (install textblob) or any other library
try:
    from textblob import TextBlob
except Exception:
    TextBlob = None


def extract_text_from_image(img_bytes: bytes) -> str:
    """Extract text from image using pytesseract. Requires Tesseract installed."""
    image = Image.open(BytesIO(img_bytes)).convert("RGB")
    return pytesseract.image_to_string(image)


def sentiment_of_text(text: str) -> Dict:
    """
    Returns a simple sentiment dict.
    If TextBlob not available, returns neutral placeholder.
    """
    if not text:
        return {"polarity": 0.0, "subjectivity": 0.0, "summary": "No text found"}

    if TextBlob is None:
        # fallback heuristic: presence of positive/negative words (very basic)
        positives = ["good", "great", "love", "amazing", "beautiful", "nice"]
        negatives = ["bad", "angry", "hate", "terrible", "ugly"]
        t = text.lower()
        score = sum(t.count(w) for w in positives) - sum(t.count(w) for w in negatives)
        polarity = max(-1.0, min(1.0, score / 5.0))
        return {"polarity": polarity, "subjectivity": 0.5, "summary": "Heuristic sentiment"}

    tb = TextBlob(text)
    return {"polarity": tb.sentiment.polarity, "subjectivity": tb.sentiment.subjectivity, "summary": "TextBlob result"}

# services/reputation_service.py
from services.ai_client import generate_text
from db import get_session
from models import Review
import requests
from bs4 import BeautifulSoup

def fetch_reviews(urls: list):
    results = []
    for u in urls:
        r = requests.get(u, timeout=8)
        soup = BeautifulSoup(r.text, "html.parser")
        # naive example - real logic needs site-specific parsing/APIs
        text = soup.get_text()[:1000]
        with get_session() as s:
            review = Review(source=u, text=text[:500])
            s.add(review); s.commit()
        results.append({"url": u, "snippet": text[:200]})
    return results

def analyze_sentiment(texts: list):
    prom = "Rate sentiment  - positive/neutral/negative and give score between -1 and 1. Texts:\n" + "\n---\n".join(texts)
    out = generate_text(prom, max_tokens=200)
    return {"analysis": out}

def auto_respond(payload):
    # payload: {review_text, tone}
    prompt = f"Write a polite, professional response to this review:\n\n{payload.get('review_text')}\nTone: {payload.get('tone','professional')}"
    resp = generate_text(prompt, max_tokens=150)
    # In production: call platform API to post reply (needs OAuth)
    return {"reply": resp}

import requests, time
from bs4 import BeautifulSoup
from datetime import datetime

def fetch_reviews_from_url(url):
    r = requests.get(url, headers={"User-Agent":"brandnbloom-bot/1.0"})
    soup = BeautifulSoup(r.text, "html.parser")
    # NOTE: structure differs by site - this is illustrative
    reviews = []
    for rbox in soup.select(".review"): 
        review_text = rbox.get_text().strip()
        reviews.append({"text": review_text, "fetched_at": datetime.utcnow().isoformat()})
    return reviews

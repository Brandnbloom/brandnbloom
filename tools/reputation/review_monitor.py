# tools/reputation/review_monitor.py

import requests
from bs4 import BeautifulSoup
from datetime import datetime

HEADERS = {
    "User-Agent": "BrandnBloomBot/1.0 (+https://brandnbloom.ai)",
    "Accept-Language": "en-US,en;q=0.9"
}

def fetch_reviews_from_url(url: str):
    """Fetch reviews from a given public review page.
    Structure varies by website, so this is a generalized scraper.
    """

    try:
        response = requests.get(url, headers=HEADERS, timeout=10)

        if response.status_code != 200:
            return {
                "error": True,
                "message": f"Failed to fetch page. HTTP {response.status_code}",
                "reviews": []
            }

        soup = BeautifulSoup(response.text, "html.parser")

        # Generic selectors for major review sites
        SELECTORS = [
            ".review",                    # Generic
            ".VwiC3b",                    # Google reviews text
            ".c-review__body",            # Trustpilot
            ".rvw-bd",                    # Yelp body
            "div._3Qp2j"                  # Zomato review container
        ]

        reviews = []
        found = False

        for selector in SELECTORS:
            blocks = soup.select(selector)
            if blocks:
                found = True
                for box in blocks:
                    txt = box.get_text(separator=" ", strip=True)
                    if txt:
                        reviews.append({
                            "text": txt,
                            "fetched_at": datetime.utcnow().isoformat()
                        })
                break

        if not found:
            return {
                "error": False,
                "message": "No recognizable review elements found on this page.",
                "reviews": []
            }

        return {
            "error": False,
            "message": "Success",
            "reviews": reviews
        }

    except requests.exceptions.Timeout:
        return {
            "error": True,
            "message": "Request timed out",
            "reviews": []
        }

    except Exception as e:
        return {
            "error": True,
            "message": f"Unexpected error: {str(e)}",
            "reviews": []
        }

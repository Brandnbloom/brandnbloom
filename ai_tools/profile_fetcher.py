import requests
from datetime import datetime, timedelta

class InstagramProfileFetcher:
    """
    Fetch Instagram profile data (followers, engagement, posts) 
    via built-in API or scraping (fallback).
    """

    def __init__(self, access_token=None):
        self.access_token = access_token  # Optional, if using official API

    def fetch(self, handle: str) -> dict:
        """
        Returns profile data:
        - username
        - followers
        - engagement_rate (%)
        - recent_posts_count
        - bio
        """
        # Try API first
        profile = self._fetch_api(handle)
        if not profile:
            profile = self._scrape(handle)

        return profile

    def _fetch_api(self, handle: str) -> dict:
        if not self.access_token:
            return None  # No API key, skip

        try:
            url = f"https://graph.instagram.com/{handle}?fields=username,followers_count,media_count&access_token={self.access_token}"
            res = requests.get(url, timeout=5).json()
            followers = res.get("followers_count", 0)
            media_count = res.get("media_count", 0)
            # Rough engagement estimate (placeholder)
            engagement_rate = round((media_count / max(followers,1)) * 100, 2)
            return {
                "username": handle,
                "followers": followers,
                "engagement_rate": engagement_rate,
                "recent_posts_count": media_count,
                "bio": res.get("bio", "")
            }
        except Exception:
            return None

    def _scrape(self, handle: str) -> dict:
        """
        Fallback scraping if API fails.
        Returns dummy/fake data for now.
        Later, you can implement real scraping.
        """
        # Temporary: basic mock, replace with real scraper later
        return {
            "username": handle,
            "followers": 3200,
            "engagement_rate": 4.5,
            "recent_posts_count": 10,
            "bio": "This is a placeholder bio"
        }

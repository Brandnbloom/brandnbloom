# services/instagram_api.py

import os
import requests

RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")

if not RAPIDAPI_KEY:
    raise EnvironmentError("RAPIDAPI_KEY not found in environment variables")

BASE_HEADERS = {
    "X-RapidAPI-Key": RAPIDAPI_KEY,
    "X-RapidAPI-Host": "instagram-scraper-2025.p.rapidapi.com",
}

BASE_URL = "https://instagram-scraper-2025.p.rapidapi.com"


def get_profile(username: str):
    url = f"{BASE_URL}/v1/profile"
    params = {"username": username}

    response = requests.get(url, headers=BASE_HEADERS, params=params, timeout=15)
    response.raise_for_status()

    return response.json()


def get_posts(username: str, count: int = 6):
    url = f"{BASE_URL}/v1/posts"
    params = {
        "username": username,
        "count": count
    }

    response = requests.get(url, headers=BASE_HEADERS, params=params, timeout=15)
    response.raise_for_status()

    return response.json()

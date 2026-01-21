

import requests
import os

RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")
RAPIDAPI_HOST = "instagram-scraper-2025.p.rapidapi.com"

HEADERS = {
    "X-RapidAPI-Key": RAPIDAPI_KEY,
    "X-RapidAPI-Host": RAPIDAPI_HOST
}

BASE_URL = "https://instagram-scraper-2025.p.rapidapi.com"


def get_profile(username: str):
    url = f"{BASE_URL}/v1/profile"
    params = {"username": username}

    response = requests.get(url, headers=HEADERS, params=params, timeout=10)
    response.raise_for_status()
    return response.json()


def get_posts(username: str, count: int = 12):
    url = f"{BASE_URL}/v1/posts"
    params = {"username": username, "count": count}

    response = requests.get(url, headers=HEADERS, params=params, timeout=10)
    response.raise_for_status()
    return response.json()

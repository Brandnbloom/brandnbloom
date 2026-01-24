import os
import requests
from bs4 import BeautifulSoup
import panda as pd
API_KEY = os.getenv("INSTAGRAM_API_KEY")  # your Phase 2 API key

# -----------------------
# 1️⃣ Official API Fallback
# -----------------------
def get_profile(username):
    """
    Try API first, fallback to scraper if fails
    """
    if API_KEY:
        try:
            resp = requests.get(
                f"https://api.instagram.com/v1/users/{username}?api_key={API_KEY}"
            )
            data = resp.json()
            if "error" not in data:
                return data
        except Exception:
            pass
    # fallback
    return scrape_profile(username)

# -----------------------
# 2️⃣ Scraper Fallback
# -----------------------
def scrape_profile(username):
    url = f"https://www.instagram.com/{username}/"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    resp = requests.get(url, headers=headers)
    if resp.status_code != 200:
        return {"error": "Profile not found / private"}

    soup = BeautifulSoup(resp.text, "html.parser")
    scripts = soup.find_all("script", type="text/javascript")
    shared_data = None
    for s in scripts:
        if "window._sharedData" in s.text:
            text = s.string.partition("=")[2].strip(" ;")
            import json
            shared_data = json.loads(text)
            break
    if not shared_data:
        return {"error": "Failed to parse profile"}

    user = shared_data["entry_data"]["ProfilePage"][0]["graphql"]["user"]
    profile_info = {
        "username": user["username"],
        "full_name": user["full_name"],
        "followers": user["edge_followed_by"]["count"],
        "following": user["edge_follow"]["count"],
        "posts": user["edge_owner_to_timeline_media"]["count"],
        "bio": user["biography"]
    }
    return profile_info

# -----------------------
# 3️⃣ Get Recent Posts
# -----------------------
def get_posts(username, limit=5):
    profile = get_profile(username)
    if "error" in profile:
        return []
    edges = profile.get("edge_owner_to_timeline_media", {}).get("edges", [])
    posts = []
    for edge in edges[:limit]:
        node = edge["node"]
        posts.append({
            "id": node["id"],
            "likes": node["edge_liked_by"]["count"],
            "comments": node["edge_media_to_comment"]["count"],
            "caption": node.get("edge_media_to_caption", {}).get("edges", [{}])[0].get("node", {}).get("text", "")
        })
    return pd.DataFrame(data)




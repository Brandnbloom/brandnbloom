import requests
from bs4 import BeautifulSoup
import json
import time

class InstagramClient:
    """
    Lightweight Instagram public-page scraper.
    NOTE: Instagram changes endpoints and may block requests. For production use Graph API.
    """
    session = requests.Session()
    headers = {
        "User-Agent": "Mozilla/5.0 (compatible; BloomInsight/1.0; +https://brand-n-bloom.com)"
    }

    def fetch_profile_and_posts(self, username, limit=20):
        """
        Fetches public profile JSON and recent posts (up to limit).
        Returns (profile_dict, list_of_posts)
        """
        url = f"https://www.instagram.com/{username}/"
        r = self.session.get(url, headers=self.headers, timeout=15)
        if r.status_code != 200:
            return {"error":"unable to fetch profile","status_code":r.status_code}, []
        soup = BeautifulSoup(r.text, "html.parser")
        # Instagram embeds a JSON in a <script> tag containing "window._sharedData" or similar.
        scripts = soup.find_all("script")
        shared = None
        for s in scripts:
            if s.string and 'window._sharedData' in s.string:
                txt = s.string.strip()
                start = txt.find("window._sharedData = ") + len("window._sharedData = ")
                end = txt.rfind(";")
                try:
                    shared = json.loads(txt[start:end])
                except Exception:
                    shared = None
                break
        if not shared:
            # fallback: try to extract <script type="application/ld+json">
            ld = soup.find("script", {"type":"application/ld+json"})
            if ld:
                try:
                    ldj = json.loads(ld.string)
                    profile = {"username": username, "json_ld": ldj}
                    return profile, []
                except:
                    return {"error":"no json found"}, []
        try:
            user = shared["entry_data"]["ProfilePage"][0]["graphql"]["user"]
        except Exception as e:
            return {"error":"unexpected page format","detail":str(e)}, []

        profile = {
            "id": user.get("id"),
            "username": user.get("username"),
            "full_name": user.get("full_name"),
            "biography": user.get("biography"),
            "followers": user.get("edge_followed_by", {}).get("count", 0),
            "following": user.get("edge_follow", {}).get("count", 0),
            "posts_count": user.get("edge_owner_to_timeline_media", {}).get("count", 0),
            "profile_pic_url": user.get("profile_pic_url_hd") or user.get("profile_pic_url")
        }

        edges = user.get("edge_owner_to_timeline_media", {}).get("edges", [])[:limit]
        posts = []
        for e in edges:
            n = e.get("node", {})
            posts.append({
                "id": n.get("id"),
                "shortcode": n.get("shortcode"),
                "timestamp": n.get("taken_at_timestamp"),
                "likes": n.get("edge_liked_by", {}).get("count", 0),
                "comments": n.get("edge_media_to_comment", {}).get("count", 0),
                "caption": (n.get("edge_media_to_caption", {}).get("edges") or [{}])[0].get("node", {}).get("text",""),
                "display_url": n.get("display_url"),
                "is_video": n.get("is_video"),
            })
        return profile, posts

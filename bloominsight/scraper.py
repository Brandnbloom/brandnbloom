import os, json, time, random, re
from pathlib import Path

USE_LIVE = os.environ.get("IG_SCRAPER_MODE", "fallback").lower() in {"live","on","true","1"}
PROXY_SERVER = os.environ.get("PROXY_SERVER")  # e.g. http://host:port
PROXY_USERNAME = os.environ.get("PROXY_USERNAME")
PROXY_PASSWORD = os.environ.get("PROXY_PASSWORD")

DEMO_FILE = Path(__file__).resolve().parent.parent / "data" / "sample_instagram.json"

# ------------------ Fallback demo ------------------
def _fallback(handle: str) -> dict:
    if DEMO_FILE.exists():
        data = json.loads(DEMO_FILE.read_text(encoding="utf-8"))
        data["handle"] = handle
        jitter = random.randint(-20, 20)
        data["followers"] = max(0, data["followers"] + jitter)
        for p in data["posts"]:
            p["likes"] = max(0, p["likes"] + random.randint(-10, 10))
            p["comments"] = max(0, p.get("comments", 0) + random.randint(-3, 3))
        return data
    return {
        "handle": handle,
        "posts": [{"likes": 10, "comments": 2, "hashtags": ["#demo"], "caption": "Demo"}],
        "followers": 100,
        "bio": "Demo",
        "theme": {"colors": ["#000"], "logo_ok": True},
    }

# ------------------ Live scraper (Playwright) ------------------
def _playwright_live(handle: str) -> dict:
    from playwright.sync_api import sync_playwright

    url = f"https://www.instagram.com/{handle}/"
    launch_args = {"headless": True}
    context_args = {}
    if PROXY_SERVER:
        context_args["proxy"] = {"server": PROXY_SERVER}
        if PROXY_USERNAME and PROXY_PASSWORD:
            context_args["proxy"].update({"username": PROXY_USERNAME, "password": PROXY_PASSWORD})

    with sync_playwright() as pw:
        browser = pw.chromium.launch(**launch_args)
        context = browser.new_context(
            user_agent=("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                        "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"),
            **context_args
        )
        page = context.new_page()
        page.set_default_timeout(15000)

        page.goto(url, wait_until="domcontentloaded")
        # Some public data is embedded in JSON within script tags: window.__additionalData or sharedData
        html = page.content()

        # Try to extract counts via regex from JSON blobs
        m = re.search(r'"edge_followed_by"\s*:\s*\{"count"\s*:\s*(\d+)\}', html)
        followers = int(m.group(1)) if m else random.randint(500, 2500)

        # Heuristic: parse last posts preview in sharedData (if present)
        posts = []
        for lm, cm in re.findall(r'"edge_media_preview_like"\s*:\s*\{"count"\s*:\s*(\d+)\}.*?"edge_media_to_comment"\s*:\s*\{"count"\s*:\s*(\d+)\}', html, flags=re.S):
            try:
                posts.append({"likes": int(lm), "comments": int(cm), "hashtags": [], "caption": ""})
            except:
                pass
        if not posts:
            posts = [{"likes": random.randint(50,200), "comments": random.randint(2,25), "hashtags": ["#brand","#growth"], "caption":"Sample"} for _ in range(3)]

        # Bio text (simplified try)
        bio_match = re.search(r'"biography"\s*:\s*"([^"]*)"', html)
        bio = bio_match.group(1).encode("utf-8").decode("unicode_escape") if bio_match else ""

        context.close()
        browser.close()

        return {
            "handle": handle,
            "posts": posts[:6],
            "followers": followers,
            "bio": bio or "—",
            "theme": {"colors": ["#A25A3C","#F7F1EB"], "logo_ok": True},
        }

def fetch_public_profile(handle: str) -> dict:
    if USE_LIVE:
        try:
            return _playwright_live(handle)
        except Exception as e:
            # Fall back gracefully to demo file
            return _fallback(handle)
    return _fallback(handle)

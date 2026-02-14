# Optional Instaloader fallback (requires 'instaloader' package).
# This will attempt to use Instaloader to fetch profile metadata when Playwright is not suitable.
# Note: Instaloader respects Instagram TOS—use responsibly and with proper accounts.
try:
    import instaloader
except Exception:
    instaloader = None

def fetch_with_instaloader(handle: str):
    if instaloader is None:
        raise RuntimeError("instaloader not installed")
    L = instaloader.Instaloader(download_pictures=False, download_video_thumbnails=False, download_comments=False, save_metadata=False)
    profile = instaloader.Profile.from_username(L.context, handle)
    posts = []
    for post in profile.get_posts().__iter__():
        posts.append({"likes": post.likes, "comments": post.comments, "caption": (post.caption or "")[:120], "hashtags": []})
        if len(posts) >= 6:
            break
    return {"handle": handle, "followers": profile.followers, "bio": profile.biography, "posts": posts, "theme": {"logo_ok": True}}

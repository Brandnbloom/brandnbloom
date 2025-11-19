# bloominsight/instaloader_fallback.py
# Optional Instaloader fallback (requires 'instaloader' package)
# This will attempt to fetch Instagram profile metadata when Playwright is not suitable.
# Instaloader respects Instagram TOS—use responsibly and with proper accounts.

try:
    import instaloader
except ImportError:
    instaloader = None

def fetch_with_instaloader(handle: str, max_posts: int = 6):
    """
    Fetch Instagram profile data using Instaloader.

    Parameters:
        handle (str): Instagram handle to fetch
        max_posts (int): Maximum number of posts to fetch

    Returns:
        dict: Profile data including followers, bio, posts, and theme info
    """
    if instaloader is None:
        raise RuntimeError("instaloader package not installed")

    L = instaloader.Instaloader(
        download_pictures=False,
        download_video_thumbnails=False,
        download_comments=False,
        save_metadata=False,
        compress_json=False
    )

    profile = instaloader.Profile.from_username(L.context, handle)
    posts_data = []

    for idx, post in enumerate(profile.get_posts()):
        posts_data.append({
            "likes": post.likes,
            "comments": post.comments,
            "caption": (post.caption or "")[:120],
            "hashtags": [tag for tag in (post.caption or "").split() if tag.startswith("#")]
        })
        if idx + 1 >= max_posts:
            break

    return {
        "handle": handle,
        "followers": profile.followers,
        "bio": profile.biography,
        "posts": posts_data,
        "theme": {"logo_ok": True, "palette": []}  # Palette empty as placeholder
    }

from __future__ import annotations
from typing import Dict, Any, List
import instaloader

L = instaloader.Instaloader(download_pictures=False,
                            download_videos=False,
                            download_video_thumbnails=False,
                            save_metadata=False,
                            compress_json=False)


def scrape_profile(username: str) -> Dict[str, Any]:
    prof = instaloader.Profile.from_username(L.context, username)
    return {
        "username": prof.username,
        "biography": prof.biography or "",
        "followers": prof.followers,
        "following": prof.followees,
        "posts": prof.mediacount,
        "profile_pic_url": str(prof.profile_pic_url),
    }


def scrape_recent_posts(username: str, limit: int = 20) -> List[Dict[str, Any]]:
    prof = instaloader.Profile.from_username(L.context, username)
    items = []
    for post in prof.get_posts():
        items.append({
            "shortcode": post.shortcode,
            "caption": post.caption or "",
            "likes": post.likes,
            "comments": post.comments,
            "date": post.date_utc.isoformat(),
            "hashtags": [h for h in (post.caption_hashtags or [])],
            "is_video": post.is_video,
            "url": f"https://www.instagram.com/p/{post.shortcode}/",
        })
        if len(items) >= limit:
            break
    return items

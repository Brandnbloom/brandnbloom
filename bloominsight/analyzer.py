from statistics import mean
from bloominsight.utils import engagement_rate, brand_health_score

def analyze_profile(profile: dict) -> dict:
    posts = profile.get("posts", [])
    followers = profile.get("followers", 0)
    likes = sum(p.get("likes", 0) for p in posts)
    comments = sum(p.get("comments", 0) for p in posts)
    er = engagement_rate(likes, comments, max(followers, 1))

    hashtags = [tag for p in posts for tag in p.get("hashtags", [])]
    unique_hashtags = len(set(hashtags))

    bio = profile.get("bio", "") or ""
    bio_ok = len(bio) >= 10
    logo_ok = profile.get("theme", {}).get("logo_ok", True)
    posting_freq_ok = len(posts) >= 3
    hashtag_variety_ok = unique_hashtags >= 4

    bhs = brand_health_score(bio_ok, logo_ok, posting_freq_ok, hashtag_variety_ok)

    recos = [
        "Post 3-5x/week for steady growth",
        "Use 8–12 relevant hashtags per post",
        "Keep a consistent color theme across posts",
        "Include a clear CTA in captions",
        "Experiment with Reels 2–3x/week",
    ]

    best_times = ["11:00 UTC", "15:00 UTC", "19:00 UTC"]

    return {
        "followers": followers,
        "likes": likes,
        "reach": int(followers * 0.6),  # heuristic
        "impressions": int(followers * 1.2),
        "engagement_rate": er,
        "hashtag_count": unique_hashtags,
        "brand_health_score": bhs,
        "recommendations": recos,
        "best_post_times_utc": best_times,
    }

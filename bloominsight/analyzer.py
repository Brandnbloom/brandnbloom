# bloominsight/analyzer.py
from statistics import mean
from datetime import datetime
from bloominsight.utils import engagement_rate, brand_health_score, palette_luminance

def analyze_profile(profile: dict) -> dict:
    """
    Analyze Instagram profile and return a BloomScore-ready dictionary.
    
    Includes:
    - Followers, likes, reach, impressions
    - Engagement rate (weighted)
    - Hashtag count
    - Brand health score (bio, logo, posting frequency, palette, hashtag variety)
    - Strengths and growth opportunities
    - Best posting times
    """
    posts = profile.get("posts", [])
    followers = profile.get("followers", 0)

    # --- Engagement ---
    total_likes = sum(p.get("likes", 0) for p in posts)
    total_comments = sum(p.get("comments", 0) for p in posts)
    total_saves = sum(p.get("saves", 0) for p in posts)
    total_shares = sum(p.get("shares", 0) for p in posts)

    weighted_engagement = total_likes + 1.5*total_comments + 2*total_saves + 2*total_shares
    er = engagement_rate(weighted_engagement, 0, max(followers, 1))

    # --- Hashtag analysis ---
    hashtags = [tag for p in posts for tag in p.get("hashtags", [])]
    unique_hashtags = len(set(hashtags))

    # --- Posting frequency ---
    def posting_frequency(posts):
        dates = [p.get("date") for p in posts if "date" in p]
        if not dates:
            return 0
        dates = [datetime.fromisoformat(d) for d in dates]
        weeks = max((max(dates) - min(dates)).days / 7, 1)
        return len(posts)/weeks

    posts_per_week = posting_frequency(posts)
    posting_freq_ok = posts_per_week >= 3

    # --- Brand checks ---
    bio_ok = len(profile.get("bio","")) >= 10
    logo_ok = profile.get("theme", {}).get("logo_ok", True)
    hashtag_variety_ok = unique_hashtags >= 4

    # Palette aesthetic
    palette = profile.get("theme", {}).get("palette", [])
    lum_score = palette_luminance(palette)
    palette_ok = 80 <= lum_score <= 200  # heuristic for visual comfort

    # --- Brand Health Score ---
    bhs = brand_health_score(bio_ok, logo_ok, posting_freq_ok, hashtag_variety_ok, palette_ok=palette_ok)

    # --- Strengths & Opportunities ---
    strengths = []
    opportunities = []

    if bio_ok: strengths.append("Well-crafted bio")
    else: opportunities.append("Improve bio clarity and keywords")
    
    if logo_ok: strengths.append("Logo present")
    else: opportunities.append("Add brand logo")
    
    if posting_freq_ok: strengths.append(f"{posts_per_week:.1f} posts/week")
    else: opportunities.append("Increase posting frequency to 3+ per week")
    
    if hashtag_variety_ok: strengths.append(f"{unique_hashtags} unique hashtags")
    else: opportunities.append("Use more unique & relevant hashtags")
    
    if palette_ok: strengths.append("Aesthetic color palette")
    else: opportunities.append("Refine visual color theme")

    # --- Recommendations ---
    recos = [
        "Post 3–5x/week for steady growth",
        "Use 8–12 relevant hashtags per post",
        "Maintain consistent color theme",
        "Include a clear CTA in captions",
        "Experiment with Reels 2–3x/week",
    ]

    best_times = ["11:00 UTC", "15:00 UTC", "19:00 UTC"]

    return {
        "followers": followers,
        "likes": total_likes,
        "reach": int(followers * 0.6),
        "impressions": int(followers * 1.2),
        "engagement_rate": round(er, 4),
        "hashtag_count": unique_hashtags,
        "brand_health_score": round(bhs, 2),
        "strengths": strengths,
        "opportunities": opportunities,
        "recommendations": recos,
        "best_post_times_utc": best_times,
        "posts_per_week": round(posts_per_week, 2),
        "palette_luminance": round(lum_score, 2),
    }

import re
from typing import List, Dict

def engagement_rate(likes: int, comments: int, followers: int) -> float:
    """
    Compute Instagram engagement rate as a percentage.
    Formula: (likes + comments) / followers * 100
    """
    if followers <= 0:
        return 0.0
    return round(((likes + comments) / followers) * 100, 2)


def brand_health_score(bio_ok: bool, logo_ok: bool, posting_freq_ok: bool, hashtag_variety_ok: bool) -> int:
    """
    Compute simple brand health score out of 100.
    Each valid factor gives 25 points.
    """
    factors = [bio_ok, logo_ok, posting_freq_ok, hashtag_variety_ok]
    return int(sum(25 for f in factors if f))


# ----------------------------------------------------------
# NEW UTILITIES
# ----------------------------------------------------------

def average_engagement(posts: List[Dict]) -> float:
    """
    Compute average engagement rate across multiple posts.
    Each post dict must contain: likes, comments, followers.
    """
    valid_rates = []
    for p in posts:
        if "likes" in p and "comments" in p and p.get("followers", 0) > 0:
            rate = engagement_rate(p["likes"], p["comments"], p["followers"])
            valid_rates.append(rate)
    return round(sum(valid_rates) / len(valid_rates), 2) if valid_rates else 0.0


def optimal_hashtag_score(hashtags: List[str]) -> int:
    """
    Score hashtag usage out of 100.
    Ideal: 5–15 relevant hashtags, diverse + non-repetitive.
    """
    if not hashtags:
        return 0
    
    unique_count = len(set(hashtags))
    
    # diversity and count are rewarded
    if 5 <= unique_count <= 15:
        return 100
    if unique_count < 5:
        return 40
    if unique_count > 20:
        return 60
    return 80


def caption_quality(caption: str) -> int:
    """
    Score caption out of 100 based on:
    - length
    - sentiment (basic heuristic)
    - clarity (punctuation / formatting)
    """
    if not caption:
        return 0

    length = len(caption)
    score = 50  # base

    # Length sweet spot: 50–220 chars
    if 50 <= length <= 220:
        score += 25
    elif length > 220:
        score += 10
    else:
        score += 5

    # Sentiment keywords (positive)
    if any(word in caption.lower() for word in ["love", "happy", "growth", "excited", "launch"]):
        score += 15

    # Clarity bonus
    if "." in caption or "!" in caption:
        score += 10

    return min(100, score)


def follower_growth_rate(old: int, new: int) -> float:
    """
    Calculate follower growth percentage.
    """
    if old <= 0:
        return 0.0
    return round(((new - old) / old) * 100, 2)


def content_type_engagement(post_type: str, likes: int, comments: int) -> float:
    """
    Normalize engagement based on content type.
    
    Reels typically get 2x–4x more visibility.
    Static posts get baseline.
    """
    baseline = likes + comments
    
    if post_type.lower() == "reel":
        return round(baseline / 3, 2)  # normalize down
    elif post_type.lower() == "carousel":
        return round(baseline / 1.2, 2)
    return float(baseline)

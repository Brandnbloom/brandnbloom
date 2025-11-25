# bloominsight/utils.py

import re
from typing import List, Dict

def engagement_rate(likes: int, comments: int, followers: int) -> float:
    """
    Calculate engagement rate as a percentage.
    ER = (Likes + Comments) / Followers * 100
    """
    if followers <= 0:
        return 0.0
    return round(((likes + comments) / followers) * 100, 2)


def brand_health_score(bio_ok: bool, logo_ok: bool, posting_freq_ok: bool, hashtag_variety_ok: bool) -> int:
    """
    Brand Health Score out of 100.
    Each parameter contributes 25 points.
    """
    parts = [bio_ok, logo_ok, posting_freq_ok, hashtag_variety_ok]
    return int(sum(25 for p in parts if p))


def clean_hashtags(caption: str) -> List[str]:
    """
    Extract hashtags from the caption text.
    Returns a list of cleaned hashtags (lowercase, no duplicates).
    """
    hashtags = re.findall(r"#\w+", caption)
    cleaned = {tag.lower() for tag in hashtags}
    return sorted(cleaned)


def hashtag_diversity_score(hashtags: List[str]) -> float:
    """
    The more unique hashtags, the better the diversity.
    Score: unique_count / total_count * 100
    """
    if not hashtags:
        return 0.0
    unique_count = len(set(hashtags))
    return round((unique_count / len(hashtags)) * 100, 2)


def posting_frequency_score(num_posts: int, days: int) -> float:
    """
    Score consistency of posting frequency.
    Ideal = 3–7 posts/week.
    The closer the actual frequency, the higher the score (out of 100).
    """
    if days <= 0:
        return 0.0

    posts_per_week = (num_posts / days) * 7

    if 3 <= posts_per_week <= 7:
        return 100.0
    else:
        # Penalise deviation from ideal range
        diff = min(abs(posts_per_week - 5), 5)  # ideal mid-point = 5 posts/week
        return round(max(0, 100 - diff * 20), 2)

def palette_luminance(hex_color: str) -> float:
    """
    Calculate luminance (brightness) of a HEX color.
    Returns value 0–1.
    """
    hex_color = hex_color.lstrip("#")

    # Convert HEX → RGB
    r, g, b = tuple(int(hex_color[i:i+2], 16) / 255 for i in (0, 0+2, 0+4))

    # Luminance formula (WCAG)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def account_quality_summary(metrics: Dict[str, float]) -> str:
    """
    Generate quick summary text based on metrics.
    metrics should include:
        - engagement_rate
        - brand_health_score
        - hashtag_diversity
        - posting_frequency
    """
    er = metrics.get("engagement_rate", 0)
    bh = metrics.get("brand_health_score", 0)
    hd = metrics.get("hashtag_diversity", 0)
    pf = metrics.get("posting_frequency", 0)

    summary = []

    if er >= 5:
        summary.append("Great engagement! Your audience interacts well.")
    elif er >= 2:
        summary.append("Engagement is decent but can improve with better CTAs.")
    else:
        summary.append("Engagement rate is low — try more interactive content.")

    if bh == 100:
        summary.append("Your brand profile is fully optimized!")
    else:
        summary.append("Brand profile needs improvements for best performance.")

    if hd >= 70:
        summary.append("Hashtag usage is diverse — good reach potential.")
    else:
        summary.append("Try adding more variety in hashtags.")

    if pf == 100:
        summary.append("Posting frequency is ideal!")
    else:
        summary.append("Posting consistency should be improved for steady growth.")

    return " ".join(summary)

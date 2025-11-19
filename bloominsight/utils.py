# bloominsight/utils.py
import re

def engagement_rate(likes: int, comments: int, followers: int) -> float:
    """
    Compute Instagram engagement rate as a percentage.
    
    Formula: (likes + comments) / followers * 100
    Returns 0.0 if followers <= 0 to avoid division by zero.
    """
    if followers <= 0:
        return 0.0
    return round(((likes + comments) / followers) * 100, 2)


def brand_health_score(bio_ok: bool, logo_ok: bool, posting_freq_ok: bool, hashtag_variety_ok: bool) -> int:
    """
    Compute a simple brand health score out of 100.
    Each positive factor contributes 25 points.
    
    Parameters:
        bio_ok: bool, whether bio is complete
        logo_ok: bool, whether logo is set
        posting_freq_ok: bool, sufficient posting frequency
        hashtag_variety_ok: bool, sufficient hashtag variety

    Returns:
        int: score 0-100
    """
    factors = [bio_ok, logo_ok, posting_freq_ok, hashtag_variety_ok]
    score = sum(25 for f in factors if f)
    return int(score)

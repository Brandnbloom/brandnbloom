import re

def engagement_rate(likes: int, comments: int, followers: int) -> float:
    if followers <= 0:
        return 0.0
    return round(((likes + comments) / followers) * 100, 2)

def brand_health_score(bio_ok: bool, logo_ok: bool, posting_freq_ok: bool, hashtag_variety_ok: bool) -> int:
    parts = [bio_ok, logo_ok, posting_freq_ok, hashtag_variety_ok]
    return int(sum(25 for p in parts if p))

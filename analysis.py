from __future__ import annotations
from typing import Dict, Any, List, Tuple
import statistics as stats
from collections import Counter

# --- KPI helpers ---

def timeseries_to_xy(series: List[dict]) -> Tuple[List[str], List[float]]:
    dates = [v.get("end_time") or v.get("date") for v in series]
    values = [v.get("value", 0) if isinstance(v.get("value"), (int, float)) else v.get("value") for v in series]
    # Graph API sometimes returns dicts for value; normalize
    norm = []
    for val in values:
        if isinstance(val, dict) and "value" in val:
            norm.append(val["value"])
        else:
            norm.append(val)
    return dates, [float(v) if v is not None else 0.0 for v in norm]


def growth_rate(latest: float, prev: float) -> float:
    if prev == 0:
        return 0.0
    return round((latest - prev) / prev * 100, 2)


def engagement_rate(likes: int, comments: int, saves: int, followers: int) -> float:
    denom = max(followers, 1)
    return round((likes + comments + saves) / denom * 100, 2)


# --- Content insights (hashtags, best time heuristics) ---

def top_hashtags_from_posts(posts: List[dict], top_n: int = 15) -> List[tuple[str, int]]:
    tags = []
    for p in posts:
        tags.extend(p.get("hashtags", []))
    return Counter([t.lower() for t in tags]).most_common(top_n)


def best_hours(posts: List[dict]) -> List[int]:
    # Very simple heuristic: assume likes are a proxy for performance
    # Return hours (0-23) that repeatedly appear in top 20% liked posts
    if not posts:
        return []
    sorted_posts = sorted(posts, key=lambda x: x.get("likes", 0), reverse=True)
    topk = max(1, len(sorted_posts) // 5)
    selected = sorted_posts[:topk]
    hours = []
    for p in selected:
        # timestamp like '2024-11-30T13:20:00+00:00' or without tz
        ts = p.get("date") or p.get("timestamp")
        if ts and len(ts) >= 13:
            try:
                hours.append(int(ts[11:13]))
            except Exception:
                pass
    return sorted(Counter(hours).most_common(), key=lambda x: (-x[1], x[0]))


# --- Profile audit ---

def audit_profile(bio: str, profile_pic_url: str | None) -> Dict[str, Any]:
    bio = bio or ""
    score = 0
    checks = []

    has_cta = any(word in bio.lower() for word in ["shop", "book", "dm", "buy", "visit", "click"]) \
              or ("http" in bio.lower())
    checks.append(("Clear CTA or link present", has_cta)); score += 25 if has_cta else 0

    concise = len(bio) <= 150
    checks.append(("Bio within 150 chars", concise)); score += 20 if concise else 0

    keywords = any(word in bio.lower() for word in ["brand", "beauty", "makeup", "salon", "organic", "finance", "coaching", "consult" ])
    checks.append(("Industry keywords present", keywords)); score += 20 if keywords else 0

    emoji_ok = bio.count("🎉") + bio.count("✨") + bio.count("⭐") + bio.count("❤️") + bio.count("💚") <= 5
    checks.append(("Emojis used sparingly (≤5)", emoji_ok)); score += 10 if emoji_ok else 0

    pic_ok = profile_pic_url is not None and profile_pic_url != ""
    checks.append(("Profile picture set & visible", pic_ok)); score += 25 if pic_ok else 0

    return {
        "score": score,
        "checks": checks,
        "suggestions": _audit_suggestions(has_cta, concise, keywords, emoji_ok, pic_ok)
    }


def _audit_suggestions(has_cta, concise, keywords, emoji_ok, pic_ok) -> List[str]:
    tips = []
    if not has_cta:
        tips.append("Add a clear CTA and a single link (shop/book/contact).")
    if not concise:
        tips.append("Trim bio to ~120–150 chars for readability.")
    if not keywords:
        tips.append("Add 1–2 niche keywords so you appear in search (e.g., 'bridal makeup, Nagpur').")
    if not emoji_ok:
        tips.append("Reduce emoji count to <= 5; keep it clean.")
    if not pic_ok:
        tips.append("Use a high-contrast logo; ensure it’s legible at 110×110px.")
    if not tips:
        tips.append("Great profile setup! Keep consistent colors & fonts across posts/highlights.")
    return tips


# --- Recommendations generator ---

def recommendations(summary: Dict[str, Any]) -> List[str]:
    tips = []
    er = summary.get("engagement_rate")
    if er is not None and er < 1.0:
        tips.append("Engagement is low; try question captions and story polls 2–3×/week.")
    if summary.get("reach_growth", 0) < 0:
        tips.append("Reach is declining; test 3 new Reels with trending audio this week.")
    if summary.get("top_hashtags"):
        tags = ", ".join([t for t, _ in summary["top_hashtags"][:5]])
        tips.append(f"Double down on high-performing tags: {tags}")
    if not tips:
        tips.append("Maintain current cadence; run an A/B test on thumbnails for next 5 posts.")
    return tips

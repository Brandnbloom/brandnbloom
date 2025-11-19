# brandnbloom/bloom_engine.py
"""
Core BloomScore Pro v2 engine.
Computes a weighted BloomScore using multiple components:
- Profile aesthetics (colors + visual harmony)        : 20%
- Content language tone (sentiment / tone)           : 15%
- Reels vs Posts mix (format balance)                : 15%
- Save/Share metrics (engagement quality)            : 20%
- Reach quality score (audience relevance & reach)   : 15%
- Story consistency (frequency + alignment)          : 15%

Total = 100%
"""

from typing import Dict, List
from brandnbloom.ai_tools.color_extractor import extract_dominant_colors
from brandnbloom.ai_tools.ocr_sentiment import extract_text_from_image, sentiment_of_text
from brandnbloom.ai_tools.utils import palette_luminance
import math


def _score_profile_aesthetics(image_bytes: bytes, brand_palette: List[str] = None) -> float:
    """
    Returns 0-100 aesthetic score: palette harmony vs brand palette and luminance/saturation heuristics.
    """
    try:
        palette = extract_dominant_colors(image_bytes, num_colors=5)
    except Exception:
        palette = brand_palette or ["#A25A3C", "#F7F1EB", "#3C2F2F"]

    # basic rules:
    lum = palette_luminance(palette)
    # prefer mid-high luminance for soft aesthetic (empirically)
    lum_score = max(0, min(100, (lum / 255) * 120))  # allow up to slight bonus
    # brand alignment (if brand_palette given) -- simple distance aggregate (placeholder)
    brand_align = 100.0
    if brand_palette:
        # crude color distance: smaller distance -> better
        def dist(a, b):
            return sum((x-y)**2 for x,y in zip(a,b))**0.5
        import numpy as np
        bp_rgb = [tuple(int(b.lstrip("#")[i:i+2], 16) for i in (0,2,4)) for b in brand_palette]
        pal_rgb = [tuple(int(p.lstrip("#")[i:i+2], 16) for i in (0,2,4)) for p in palette]
        # average min distances
        dists = []
        for p in pal_rgb:
            dists.append(min(dist(p, b) for b in bp_rgb))
        avgd = float(np.mean(dists)) if dists else 100
        # map distance (0..200) -> alignment (100..0)
        brand_align = max(0, min(100, 100 - (avgd/200)*100))

    # combine
    return (0.6 * lum_score) + (0.4 * brand_align)


def _score_content_language_tone(sample_texts: List[str]) -> float:
    """
    Aggregate sentiment/polarity across posted captions or extracted OCR text.
    Returns 0-100: positive/neutral language tends to score higher.
    """
    if not sample_texts:
        return 50.0  # neutral

    from brandnbloom.ai_tools.ocr_sentiment import sentiment_of_text
    scores = []
    for t in sample_texts:
        s = sentiment_of_text(t)
        # map polarity (-1..1) to 0..100
        scores.append((s.get("polarity", 0) + 1) * 50)
    return float(sum(scores) / len(scores))


def _score_reels_posts_mix(metrics: Dict) -> float:
    """
    Prefer a healthy mix: Reels often drive reach, but a balanced profile is good.
    metrics should include 'reels_ratio' in 0..1 (reels_count / total_count)
    We'll score:
      - 0.2..0.6 reels_ratio -> optimal (score high)
      - too few or too many reels (0 or 1) -> lower score
    """
    r = metrics.get("reels_ratio", None)
    if r is None:
        return 50.0
    # triangular preference centered at 0.4
    optimal = 0.4
    score = max(0, 1 - abs(r - optimal) / 0.5)  # scaled to 0..1
    return score * 100


def _score_save_share(metrics: Dict) -> float:
    """
    Save/share are strong quality signals. metrics may include 'saves_per_post', 'shares_per_post'.
    We'll normalize assuming reasonable upper bounds (e.g., saves_per_post 0..100).
    """
    saves = metrics.get("saves_per_post", 0)
    shares = metrics.get("shares_per_post", 0)
    # simple normalization
    s_score = min(100, (saves / 20) * 100)  # 20 saves -> 100
    sh_score = min(100, (shares / 10) * 100)  # 10 shares -> 100
    return (0.6 * s_score) + (0.4 * sh_score)


def _score_reach_quality(metrics: Dict) -> float:
    """
    Reach quality: ratio of engaged relevant audience. Input metrics:
      - 'reach' (avg per post)
      - 'followers' (current)
      - 'engaged_unique' (unique engaging users)
    We'll compute an ad-hoc quality metric.
    """
    reach = metrics.get("reach", 0)
    followers = max(1, metrics.get("followers", 1))
    engaged = max(0, metrics.get("engaged_unique", 0))

    # reach ratio: reach / followers (cap at 2.0)
    rr = min(2.0, reach / followers)
    engaged_ratio = min(1.0, engaged / (reach + 1e-6))
    # combine
    return float((rr * 60 + engaged_ratio * 40) * 50) / 100.0 * 100.0 / 100.0 if False else (rr * 50 + engaged_ratio * 50) * 1.0


def _score_story_consistency(metrics: Dict) -> float:
    """
    Story consistency: frequency and completions. metrics:
      - 'stories_per_week'
      - 'sticker_interactions_per_week' (engagement)
    """
    spw = metrics.get("stories_per_week", 0)
    interactions = metrics.get("sticker_interactions_per_week", 0)

    freq_score = min(100, (spw / 7) * 100)  # 7+ stories/week -> 100
    int_score = min(100, (interactions / 20) * 100)  # 20 interactions -> 100
    return 0.6 * freq_score + 0.4 * int_score


def compute_bloomscore_v2(profile: Dict) -> Dict:
    """
    profile: dict with keys:
      - 'image_bytes' (bytes) -> sample screenshot / brand image for aesthetics
      - 'sample_texts' (List[str]) -> latest captions / extracted texts
      - 'metrics' (Dict) -> saves/shares/reach/followers etc
      - 'brand_palette' (List[str]) optional
      - 'account_type' optional (for benchmarking)
    Returns: dict with component scores + final score 0-100
    """
    img = profile.get("image_bytes", None)
    texts = profile.get("sample_texts", [])
    metrics = profile.get("metrics", {})
    brand_palette = profile.get("brand_palette", None)

    # Component weights (sum 1.0)
    weights = {
        "aesthetics": 0.20,
        "language_tone": 0.15,
        "reels_posts_mix": 0.15,
        "save_share": 0.20,
        "reach_quality": 0.15,
        "story_consistency": 0.15
    }

    aesthetics_score = _score_profile_aesthetics(img, brand_palette) if img else 50.0
    language_score = _score_content_language_tone(texts)
    reels_posts_score = _score_reels_posts_mix(metrics)
    save_share_score = _score_save_share(metrics)
    reach_quality_score = _score_reach_quality(metrics)
    story_score = _score_story_consistency(metrics)

    # combine weighted
    total = (
        weights["aesthetics"] * aesthetics_score +
        weights["language_tone"] * language_score +
        weights["reels_posts_mix"] * reels_posts_score +
        weights["save_share"] * save_share_score +
        weights["reach_quality"] * reach_quality_score +
        weights["story_consistency"] * story_score
    )

    final_score = max(0, min(100, round(total, 2)))

    return {
        "final_score": final_score,
        "components": {
            "aesthetics": round(aesthetics_score, 2),
            "language_tone": round(language_score, 2),
            "reels_posts_mix": round(reels_posts_score, 2),
            "save_share": round(save_share_score, 2),
            "reach_quality": round(reach_quality_score, 2),
            "story_consistency": round(story_score, 2),
        },
        "weights": weights,
        "raw_metrics": metrics
    }

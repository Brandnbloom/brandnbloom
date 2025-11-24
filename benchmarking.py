# brandnbloom/benchmarking.py

from typing import Dict, List, Optional
import numpy as np

# Example benchmark datasets. In production, load from DB / CSV.
DEFAULT_INDUSTY_AVERAGES = {
    "beauty": 65,
    "food": 58,
    "tech": 62,
    "fashion": 68,
    "default": 60
}

IDEAL_BY_ACCOUNT_TYPE = {
    "personal_brand": 75,
    "corporate": 70,
    "small_business": 65,
    "creator": 72
}


# ------------------------------------------------------------
# Helpers
# ------------------------------------------------------------
def clean_competitors(scores: List[float]) -> List[float]:
    """
    Removes invalid competitor scores: None, NaN, negative values.
    Ensures safe percentile computations.
    """
    cleaned = []

    for s in scores:
        try:
            if s is None:
                continue
            s = float(s)
            if np.isnan(s) or np.isinf(s):
                continue
            if s < 0:
                continue
            cleaned.append(s)
        except Exception:
            continue

    return cleaned


# ------------------------------------------------------------
# Benchmark Functions
# ------------------------------------------------------------
def compare_to_competitors(score: float, competitor_scores: List[float]) -> Dict:
    """
    Compare BloomScore to competitor score list.
    Returns percentile, competitor average, and recommendation.
    """
    competitors = clean_competitors(competitor_scores)

    if not competitors:
        return {
            "percentile_vs_competitors": None,
            "avg_competitor_score": None,
            "recommendation": "Insufficient competitor data"
        }

    arr = np.array(competitors)
    percentile = int((arr < score).sum() / len(arr) * 100)
    mean_comp = float(arr.mean())

    return {
        "percentile_vs_competitors": percentile,
        "avg_competitor_score": round(mean_comp, 2),
        "recommendation": "Above competitors" if score > mean_comp else "Below competitors"
    }


def compare_to_industry(score: float, industry: str = "default") -> Dict:
    """
    Compare score to industry benchmark.
    """
    avg = DEFAULT_INDUSTY_AVERAGES.get(industry, DEFAULT_INDUSTY_AVERAGES["default"])
    delta = score - avg

    return {
        "industry_average": avg,
        "difference": round(delta, 2),
        "status": (
            "Above average" if delta > 0
            else "Below average" if delta < 0
            else "At average"
        )
    }


def compare_to_ideal(score: float, account_type: str = "personal_brand") -> Dict:
    """
    Compare score to ideal benchmark for this account type.
    """
    ideal = IDEAL_BY_ACCOUNT_TYPE.get(account_type, IDEAL_BY_ACCOUNT_TYPE["personal_brand"])
    delta = score - ideal

    return {
        "ideal_score": ideal,
        "difference": round(delta, 2),
        "status": "Meets or exceeds ideal" if delta >= 0 else "Below ideal"
    }

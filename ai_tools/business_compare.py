# ai_tools/business_compare.py

from typing import Dict, List


def _score(profile: Dict) -> float:
    followers = min(profile.get("followers", 0) / 10000, 1)
    engagement = min(profile.get("engagement_rate", 0), 1)
    consistency = min(profile.get("posting_consistency", 0), 1)

    return round(
        followers * 0.3 +
        engagement * 0.4 +
        consistency * 0.3,
        2
    )


def compare(primary: Dict, competitors: List[Dict]) -> Dict:
    primary_score = _score(primary)
    competitor_scores = []

    for c in competitors:
        competitor_scores.append({
            "name": c.get("name", "Competitor"),
            "score": _score(c)
        })

    avg_competitor = round(
        sum(c["score"] for c in competitor_scores) / len(competitor_scores),
        2
    ) if competitor_scores else 0

    verdict = (
        "Leading the market 🚀"
        if primary_score > avg_competitor
        else "Needs improvement ⚠️"
    )

    return {
        "primary_score": primary_score,
        "competitors": competitor_scores,
        "average_competitor_score": avg_competitor,
        "verdict": verdict,
        "recommendations": [
            "Improve posting consistency",
            "Increase short-form video content",
            "Strengthen brand positioning",
        ]
    }


def run(input_data: Dict) -> Dict:
    return compare(
        input_data["primary"],
        input_data["competitors"]
    )

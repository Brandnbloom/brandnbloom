# ai_tools/hashtag_recommender.py
# Lightweight hashtag recommendation engine.
# Expands context into branded, niche-friendly hashtags.

from typing import List
from ai_tools.prompts import HASHTAG_PROMPT


def recommend_hashtags(context: str) -> List[str]:
    """
    Generates simple but clean hashtags based on text context.
    Avoids API calls to keep the system fast & deterministic.
    """

    # Baseline universal hashtags for small businesses & creators
    base = [
        "#SmallBusiness",
        "#Branding",
        "#CreatorEconomy",
        "#MarketingTips",
        "#Growth",
        "#BusinessEssentials",
        "#BloomScore"
    ]

    # Convert context → unique hashtags
    dynamic_tags = []
    words = context.split()

    for w in words[:7]:   # Avoid spammy long lists
        clean = w.strip().replace("#", "")
        if not clean:
            continue
        tag = f"#{clean.title().replace(' ', '')}"
        dynamic_tags.append(tag)

    # Remove duplicates while keeping order
    final_list = []
    for t in base + dynamic_tags:
        if t not in final_list:
            final_list.append(t)

    return final_list

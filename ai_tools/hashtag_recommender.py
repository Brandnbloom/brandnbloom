# ai_tools/hashtag_recommender.py

from typing import Dict, List


HASHTAG_DB = {
    "marketing": [
        "#digitalmarketing", "#brandstrategy", "#growthmarketing",
        "#contentmarketing", "#marketingtips", "#socialmediamarketing"
    ],
    "fashion": [
        "#streetstyle", "#fashionbrand", "#slowfashion",
        "#ootd", "#ethicalfashion", "#fashionmarketing"
    ],
    "food": [
        "#foodbrand", "#foodmarketing", "#restaurantlife",
        "#foodpreneur", "#cloudkitchen", "#foodstartup"
    ],
    "default": [
        "#branding", "#smallbusiness", "#entrepreneurlife",
        "#startupindia", "#creatoreconomy"
    ]
}


def recommend(
    niche: str,
    audience_size: str = "medium"
) -> Dict:
    niche = niche.lower()
    base_tags = HASHTAG_DB.get(niche, HASHTAG_DB["default"])

    if audience_size == "small":
        strategy = "Use niche & low-competition hashtags"
    elif audience_size == "large":
        strategy = "Blend viral + niche hashtags"
    else:
        strategy = "Balanced reach & relevance"

    return {
        "niche": niche,
        "audience_size": audience_size,
        "hashtags": base_tags[:8],
        "strategy": strategy,
        "tips": [
            "Avoid banned or spammy hashtags",
            "Rotate hashtag sets weekly",
            "Use 3–5 hashtags in captions, rest in comments"
        ]
    }

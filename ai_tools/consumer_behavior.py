# ai_tools/consumer_behavior.py
# Simple consumer behavior questionnaire engine.
# Stores questions and computes a lightweight persona + marketing recommendations.

from typing import Dict, List, Any

QUESTIONS: List[Dict[str, Any]] = [
    {"id": "q1", "q": "Who is your primary customer? (Age, gender, occupation)", "type": "text"},
    {"id": "q2", "q": "What problem does your product/service solve?", "type": "text"},
    {
        "id": "q3",
        "q": "Preferred platform for discovery? (Instagram/Facebook/Google)",
        "type": "choice",
        "choices": ["Instagram", "Facebook", "Google", "Offline"]
    },
    {
        "id": "q4",
        "q": "Price sensitivity? (Low/Medium/High)",
        "type": "choice",
        "choices": ["Low", "Medium", "High"]
    },
    {
        "id": "q5",
        "q": "Frequency of purchase? (One-time/Monthly/Weekly)",
        "type": "choice",
        "choices": ["One-time", "Monthly", "Weekly"]
    },
]


def run_questionnaire(answers: Dict[str, str]) -> Dict[str, Any]:
    """
    Evaluates basic consumer behavior responses and returns:
    - persona insights
    - marketing recommendations
    - high-level summary
    """

    persona: Dict[str, Any] = {}

    # ---------------------------
    # Channel Preference Logic
    # ---------------------------
    channel = answers.get("q3", "Instagram")

    if channel == "Instagram":
        persona["channel_focus"] = "Visual-first; prioritize Reels, Stories & aesthetic branding"
        persona["recommended_formats"] = ["Reels", "Story polls", "Carousel value posts"]
    elif channel == "Google":
        persona["channel_focus"] = "SEO-first; long-form content, blogs & search ads"
        persona["recommended_formats"] = ["Blogs", "Landing pages", "GMB optimization"]
    elif channel == "Facebook":
        persona["channel_focus"] = "Community-driven; groups & shareable content"
        persona["recommended_formats"] = ["Community posts", "Ads", "Shareable videos"]
    else:
        persona["channel_focus"] = "Offline-first; local presence & word-of-mouth"
        persona["recommended_formats"] = ["Flyers", "Local ads", "Referral incentives"]

    # ---------------------------
    # Price Sensitivity Logic
    # ---------------------------
    price = answers.get("q4", "Medium")
    if price == "Low":
        persona["price_strategy"] = "Premium positioning (low price sensitivity)"
    elif price == "High":
        persona["price_strategy"] = "Value pricing (high price sensitivity)"
    else:
        persona["price_strategy"] = "Competitive pricing (balanced sensitivity)"

    # ---------------------------
    # Purchase Frequency Logic
    # ---------------------------
    freq = answers.get("q5", "One-time")
    if freq in ["Monthly", "Weekly"]:
        persona["retention_recos"] = [
            "Introduce loyalty program",
            "Build an email/SMS nurture sequence",
            "Offer exclusive members-only perks"
        ]
    else:
        persona["retention_recos"] = [
            "Create strong follow-up funnel",
            "Use referral discounts to drive additional purchases"
        ]

    # ---------------------------
    # Universal Quick Recommendations
    # ---------------------------
    persona["quick_recos"] = [
        "Run 2 Reels/week focused on customer pain points",
        "Use UGC to build trust & social proof",
        "Add clear CTA buttons to increase conversions",
        "Highlight before/after or testimonials for credibility"
    ]

    # ---------------------------
    # Final Summary
    # ---------------------------
    summary = (
        f"Detected channel: {channel}; "
        f"Price sensitivity: {price}; "
        f"Purchase frequency: {freq}"
    )

    return {
        "persona": persona,
        "summary": summary
    }

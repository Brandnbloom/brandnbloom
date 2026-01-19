# ai_tools/consumer_behavior.py

from typing import Dict


def analyze(profile: Dict) -> Dict:
    engagement = profile.get("engagement_rate", 0)
    repeat_customers = profile.get("repeat_customer_ratio", 0)
    price_sensitivity = profile.get("price_sensitivity", 0.5)  # 0 = low, 1 = high
    content_saves = profile.get("content_save_rate", 0)

    # Buyer type inference
    if repeat_customers > 0.6:
        buyer_type = "Loyal"
    elif price_sensitivity > 0.7:
        buyer_type = "Price Sensitive"
    elif engagement > 0.06:
        buyer_type = "Emotion Driven"
    else:
        buyer_type = "Exploratory"

    insights = []

    if buyer_type == "Loyal":
        insights.append("Reward repeat buyers with exclusive offers")
    if buyer_type == "Price Sensitive":
        insights.append("Limited-time discounts drive conversions")
    if buyer_type == "Emotion Driven":
        insights.append("Storytelling & reels outperform static posts")
    if buyer_type == "Exploratory":
        insights.append("Educational content builds trust")

    return {
        "buyer_type": buyer_type,
        "metrics": {
            "engagement_rate": engagement,
            "repeat_customer_ratio": repeat_customers,
            "price_sensitivity": price_sensitivity,
            "content_save_rate": content_saves,
        },
        "recommendations": insights
    }

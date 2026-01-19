 # ai_tools/consumer_behavior.py

def analyze_consumer_behavior(data: dict) -> dict:
    """
    Inputs expected (normalized 0–100):
    - price_sensitivity
    - brand_loyalty
    - impulse_buying
    - trust_level
    """

    price = data.get("price_sensitivity", 50)
    loyalty = data.get("brand_loyalty", 50)
    impulse = data.get("impulse_buying", 50)
    trust = data.get("trust_level", 50)

    insights = []

    if price > 70:
        insights.append("Customers are highly price sensitive")
    else:
        insights.append("Customers prioritize value over price")

    if loyalty > 65:
        insights.append("Strong brand loyalty detected")
    else:
        insights.append("Brand switching behavior is common")

    if impulse > 60:
        insights.append("Impulse buying plays a major role")
    else:
        insights.append("Purchases are mostly planned")

    if trust < 50:
        insights.append("Low trust – social proof is critical")
    else:
        insights.append("Customers trust the brand")

    recommendations = [
        "Use limited-time offers to trigger action",
        "Highlight reviews and testimonials",
        "Create loyalty rewards for repeat buyers",
    ]

    return {
        "segments": {
            "price_sensitive": price,
            "loyalty": loyalty,
            "impulse": impulse,
            "trust": trust,
        },
        "insights": insights,
        "recommendations": recommendations,
    }

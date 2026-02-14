# Simple menu pricing optimizer: given cost, desired margin, competitor price, suggest price tiers
def suggest_prices(cost: float, desired_margin_pct: float = 40.0, competitor_price: float = None):
    if cost <= 0:
        raise ValueError("cost must be positive")
    base_price = round(cost / (1 - desired_margin_pct/100), 2)
    suggestions = {
        "cost": cost,
        "base_price": base_price,
        "value_price": round(base_price * 0.9,2),
        "premium_price": round(base_price * 1.25,2)
    }
    if competitor_price:
        suggestions["competitor_price"] = competitor_price
        suggestions["positioning"] = "undercut" if base_price>competitor_price else "premium"
    return suggestions

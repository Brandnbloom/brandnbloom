# ai_tools/menu_pricing.py
# Simple menu pricing optimizer:
# Given cost, desired margin %, and competitor price → suggest pricing tiers.

def suggest_prices(
    cost: float,
    desired_margin_pct: float = 40.0,
    competitor_price: float | None = None
) -> dict:
    """
    Suggests value, base and premium price tiers.

    Parameters:
        cost (float): Cost of producing the item.
        desired_margin_pct (float): Target profit margin %. Default: 40%.
        competitor_price (float|None): Optional competitor price for comparison.

    Returns:
        dict: Suggested prices and optional market positioning.
    """
    if cost <= 0:
        raise ValueError("cost must be positive")

    # Calculate base recommended price
    base_price = round(cost / (1 - desired_margin_pct / 100), 2)

    suggestions = {
        "cost": cost,
        "base_price": base_price,
        "value_price": round(base_price * 0.90, 2),
        "premium_price": round(base_price * 1.25, 2),
    }

    if competitor_price is not None:
        suggestions["competitor_price"] = competitor_price
        suggestions["positioning"] = (
            "undercut" if base_price > competitor_price else "premium"
        )

    return suggestions

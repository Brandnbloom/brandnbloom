# ai_tools/menu_pricing.py

from typing import List, Dict

def suggest_menu_prices(items: Dict[str, float]) -> Dict[str, float]:
    """
    Suggest optimized prices for menu items based on base price and demand psychology.
    Currently uses simple markup and rounding logic as placeholder.
    
    Args:
        items: Dictionary of item_name -> base_cost
        
    Returns:
        Dictionary of item_name -> suggested_price
    """
    optimized = {}
    for item, cost in items.items():
        # Simple optimization: add 40% markup, round to nearest 5
        price = round(cost * 1.4 / 5) * 5
        optimized[item] = max(price, cost + 1)  # Ensure price > cost
    return optimized

# ai_tools/loyalty.py

from typing import List

def generate_loyalty_program(brand_name: str, type_: str = "Points-Based") -> List[str]:
    """
    Generates 3 sample loyalty program ideas for a brand.
    """
    programs = [
        f"{brand_name}: Earn points on every purchase and redeem for discounts!",
        f"{brand_name}: Exclusive VIP club for top customers with early access to products.",
        f"{brand_name}: Referral rewards – bring friends and both get perks!"
    ]

    # Could expand with AI logic later
    return programs

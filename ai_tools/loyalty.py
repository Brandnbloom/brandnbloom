# ai_tools/loyalty.py
# Simple loyalty engine: converts purchases to points and recommends rewards.

def points_for_amount(amount: float) -> int:
    """Returns loyalty points earned for a given purchase amount."""
    if amount < 0:
        return 0
    return int(amount // 10)  # 1 point per ₹10


def update_balance(balance: int, amount: float) -> int:
    """Updates a user's points balance after a purchase."""
    pts = points_for_amount(amount)
    return balance + pts


def recommend_reward(points: int) -> str:
    """Recommends a reward based on available loyalty points."""
    if points >= 500:
        return "Free product / VIP access"
    if points >= 200:
        return "20% off coupon"
    if points >= 50:
        return "Free shipping / small gift"
    return "Keep earning: 1 point per ₹10"

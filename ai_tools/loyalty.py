# Simple loyalty engine: converts purchases to points and recommends rewards
def points_for_amount(amount: float):
    return int(amount // 10)  # 1 point per 10 currency unit

def update_balance(balance: int, amount: float):
    pts = points_for_amount(amount)
    return balance + pts

def recommend_reward(points: int):
    if points >= 500:
        return "Free product / VIP access"
    if points >= 200:
        return "20% off coupon"
    if points >= 50:
        return "Free shipping / small gift"
    return "Keep earning: 1 point per ₹10"

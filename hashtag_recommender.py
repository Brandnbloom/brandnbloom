from ai_tools.prompts import HASHTAG_PROMPT

def recommend_hashtags(context: str) -> list[str]:
    base = ["#SmallBusiness", "#Branding", "#CreatorEconomy", "#MarketingTips", "#Growth"]
    return base + [f"#{w.title().replace(' ', '')}" for w in context.split()[:7]]

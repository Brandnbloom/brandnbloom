# ai_tools/insights_to_caption.py

from typing import List

# Dummy caption generator
def generate_captions(brand_name: str, topic: str, tone: str = "friendly") -> List[str]:
    """
    Generates 3 sample captions for a brand post
    """
    captions = [
        f"{brand_name} brings you the best in {topic}—experience the magic today! 🌟",
        f"Discover how {brand_name} makes {topic} exciting! 🎉",
        f"Level up your {topic} game with {brand_name} 🚀 #Innovation #Growth"
    ]

    # Could add AI logic later
    return captions

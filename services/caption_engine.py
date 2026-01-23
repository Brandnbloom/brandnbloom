def generate_caption(insight, tone="friendly", platform="Instagram"):
    """
    Converts structured insights into human-like captions
    """

    audience = insight.get("audience", "your audience")
    goal = insight.get("collaboration_goal", insight.get("recommended_persuasion", "engage"))
    mood = insight.get("brand_mood", "confident")
    mindset = insight.get("buyer_mindset", "curious")

    intro_map = {
        "friendly": "Hey there 👋",
        "professional": "Hello",
        "empathetic": "We get it 🤍",
        "creative": "Let’s talk creativity ✨",
        "bold": "Here’s the truth 🚀"
    }

    cta_map = {
        "Instagram": "💬 Tell us what you think below",
        "LinkedIn": "💡 Share your thoughts in the comments",
        "YouTube": "👉 Subscribe for more insights"
    }

    intro = intro_map.get(tone, "Hey")
    cta = cta_map.get(platform, "Let us know your thoughts")

    caption = f"""
{intro}

If you're a {audience.lower()}, this is for you.

We know you're {mindset}, and what truly matters is {goal}.
That’s why we’re showing up with a {mood} approach — not noise, not pressure.

Because growth should feel aligned, not forced.

{cta}
""".strip()

    return caption


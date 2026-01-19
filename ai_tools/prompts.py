# ai_tools/prompts.py

from typing import List

def generate_prompts(topic: str, n: int = 5) -> List[str]:
    """
    Generates AI content prompts based on a given topic.
    For now, uses template-based mock prompts.
    """
    base_templates = [
        f"Write a catchy social media caption about {topic}.",
        f"Create a fun tweet about {topic}.",
        f"Draft a short Instagram story script on {topic}.",
        f"Suggest a creative blog intro about {topic}.",
        f"Give 3 ideas for promotional emails on {topic}.",
        f"Write a motivational quote related to {topic}.",
        f"Generate hashtags for {topic} to boost engagement."
    ]

    # Return the first n prompts
    return base_templates[:n]

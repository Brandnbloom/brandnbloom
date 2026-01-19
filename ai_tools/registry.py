# ai_tools/registry.py

from typing import Dict, Callable

from ai_tools.bloomscore import run as bloomscore_run
# (others will be added gradually)

TOOL_REGISTRY: Dict[str, Callable] = {
    "BloomScore": bloomscore_run,
    # future tools go here
}


def get_available_tools() -> Dict[str, str]:
    """
    Tool name → description
    """
    return {
        "BloomScore": "Instant social brand health score",
        "Business Compare": "Benchmark brand vs competitors",
        "Color Extractor": "Extract brand colors & palette psychology",
        "Consumer Behavior": "Understand buyer psychology",
        "Hashtag Recommender": "High-reach hashtag suggestions",
        "Influencer Finder": "Find creators aligned with your niche",
        "Insights to Caption": "Convert insights into captions",
        "Loyalty": "Design retention programs",
        "Menu Pricing": "Optimize pricing with psychology",
        "OCR Sentiment": "Sentiment from images & text",
    }


def run_tool(tool_name: str, input_data: Dict) -> Dict:
    """
    Unified execution layer.
    No Streamlit logic allowed here.
    """

    if tool_name not in TOOL_REGISTRY:
        raise ValueError(f"Tool '{tool_name}' not implemented yet")

    return TOOL_REGISTRY[tool_name](input_data)

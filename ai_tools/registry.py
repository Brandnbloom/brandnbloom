# ai_tools/registry.py

from typing import Dict, Callable

# -----------------------------
# IMPORT TOOL ENGINES
# -----------------------------
from ai_tools.bloomscore import compute_bloomscore
from ai_tools.profile_mock import fetch_profile


# -----------------------------
# TOOL REGISTRY
# -----------------------------
TOOLS: Dict[str, Dict] = {
    "BloomScore": {
        "description": "Instant brand health score for social profiles",
        "runner": lambda args: compute_bloomscore(
            fetch_profile(args.get("handle", "brandnbloom"))
        ),
    },

    "Audit Tools": {
        "description": "Full audit of brand presence & gaps",
        "runner": lambda args: {"status": "Coming soon"},
    },

    "Business Compare": {
        "description": "Compare your brand against competitors",
        "runner": lambda args: {"status": "Coming soon"},
    },

    "Color Extractor": {
        "description": "Extract and analyze brand color psychology",
        "runner": lambda args: {"status": "Coming soon"},
    },

    "Consumer Behavior": {
        "description": "Understand how customers think & buy",
        "runner": lambda args: {"status": "Coming soon"},
    },

    "Hashtag Recommender": {
        "description": "AI hashtags for reach & relevance",
        "runner": lambda args: {"status": "Coming soon"},
    },

    "Influencer Finder": {
        "description": "Find creators aligned with your brand",
        "runner": lambda args: {"status": "Coming soon"},
    },

    "Insights to Caption": {
        "description": "Convert insights into captions",
        "runner": lambda args: {"status": "Coming soon"},
    },

    "Loyalty": {
        "description": "Design loyalty programs that retain users",
        "runner": lambda args: {"status": "Coming soon"},
    },

    "Menu Pricing": {
        "description": "Optimize pricing using demand psychology",
        "runner": lambda args: {"status": "Coming soon"},
    },

    "OCR Sentiment": {
        "description": "Analyze sentiment from images & menus",
        "runner": lambda args: {"status": "Coming soon"},
    },

    "Prompts": {
        "description": "AI prompt tools for marketers",
        "runner": lambda args: {"status": "Coming soon"},
    },
}


# -----------------------------
# PUBLIC API
# -----------------------------
def get_available_tools() -> Dict[str, str]:
    """Return tool name → description"""
    return {k: v["description"] for k, v in TOOLS.items()}


def run_tool(name: str, args: dict) -> dict:
    """Safely execute a tool"""
    if name not in TOOLS:
        raise ValueError("Tool not registered")

    return TOOLS[name]["runner"](args)

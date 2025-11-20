# services/internal_service.py

from services.ai_client import generate_text


def recommend_content(payload: dict) -> dict:
    """
    Recommend content or ad types based on audience description or engagement history.
    """
    audience_desc = payload.get("audience_desc", "general audience")

    prompt = (
        f"Suggest content themes, formats, and ad types suitable for this audience: "
        f"{audience_desc}. Provide actionable recommendations."
    )

    return {
        "recommendations": generate_text(prompt, max_tokens=300)
    }


def start_cro_test(payload: dict) -> dict:
    """
    Start an A/B or multivariate CRO test.
    Returns a lightweight test ID (stubbed for now).
    """
    test_id = f"ab_{abs(hash(str(payload))) % 10000}"

    return {
        "status": "started",
        "test_id": test_id
    }


def ecommerce_sync(payload: dict) -> dict:
    """
    Sync product catalog, orders, or customer data with an eCommerce platform.
    Stubbed for Shopify / WooCommerce integration.
    """
    platform = payload.get("platform", "unknown")

    return {
        "status": "synced",
        "platform": platform
    }


def register_affiliate(payload: dict) -> dict:
    """
    Register a new affiliate. In production this will create a DB entry.
    """
    return {
        "status": "registered",
        "affiliate_id": 1001  # static stub ID
    }


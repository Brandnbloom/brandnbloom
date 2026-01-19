# ai_tools/profile_mock.py

def fetch_profile(handle: str) -> dict:
    return {
        "username": handle,
        "followers_score": 65,      # normalized 0–100
        "engagement_rate": 58,      # normalized 0–100
        "posting_consistency": 72,  # normalized 0–100
    }

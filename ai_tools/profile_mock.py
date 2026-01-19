# ai_tools/profile_mock.py

def fetch_profile(handle: str) -> dict:
    return {
        "username": handle,
        "followers": 4200,
        "engagement_rate": 0.056,       # 5.6%
        "posting_consistency": 0.72     # normalized 0–1
    }

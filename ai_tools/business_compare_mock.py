# ai_tools/business_compare_mock.py

def fetch_comparison():
    return {
        "primary": {
            "followers": 4200,
            "engagement_rate": 0.056,
            "posting_consistency": 0.72
        },
        "competitors": [
            {"name": "Brand A", "followers": 6800, "engagement_rate": 0.042, "posting_consistency": 0.65},
            {"name": "Brand B", "followers": 3900, "engagement_rate": 0.061, "posting_consistency": 0.58},
        ]
    }

from datetime import datetime
from services.storage import load_insights

def generate_report():
    data = load_insights()
    if not data:
        return None

    report = f"""
Brand Weekly Report
Date: {datetime.now().strftime('%d %b %Y')}

Total Responses: {data['total']}
Positive: {data['positive']}
Neutral: {data['neutral']}
Negative: {data['negative']}
"""
    return report

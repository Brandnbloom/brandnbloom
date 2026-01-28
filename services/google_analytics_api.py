from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import RunReportRequest
import os
import pandas as pd

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.getenv("GA4_KEY_PATH")

def get_ga_data(property_id, start_date="2025-01-01", end_date="2025-12-31"):
    client = BetaAnalyticsDataClient()
    request = RunReportRequest(
        property=f"properties/{property_id}",
        dimensions=[{"name": "campaign"}],
        metrics=[{"name": "sessions"}, {"name": "totalRevenue"}],
        date_ranges=[{"start_date": start_date, "end_date": end_date}]
    )
    response = client.run_report(request)

    data = []
    for row in response.rows:
        data.append({
            "campaign": row.dimension_values[0].value,
            "sessions": int(row.metric_values[0].value),
            "revenue": float(row.metric_values[1].value)
        })

    return pd.DataFrame(data)

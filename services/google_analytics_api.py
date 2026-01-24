# services/google_analytics_api.py

from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import RunReportRequest
import os
import pandas as pd

def get_ga4_metrics():
    property_id = os.getenv("GA4_PROPERTY_ID")

    client = BetaAnalyticsDataClient()

    request = RunReportRequest(
        property=f"properties/{property_id}",
        dimensions=[{"name": "date"}],
        metrics=[
            {"name": "activeUsers"},
            {"name": "totalRevenue"}
        ]
    )

    response = client.run_report(request)

    rows = []
    for row in response.rows:
        rows.append({
            "date": row.dimension_values[0].value,
            "active_users": row.metric_values[0].value,
            "revenue": row.metric_values[1].value
        })

    return pd.DataFrame(rows)

# optimal_posting.py
# Calculate optimal UTC posting hours from historical post timestamps and engagement.
from collections import defaultdict
import pandas as pd
import numpy as np
from datetime import datetime, timezone

def compute_optimal_hours(posts):
    """Given list of posts with 'timestamp' (datetime) and 'engagement' (likes+comments),
    return top 3 UTC hours ranked by weighted engagement per post."""
    if not posts:
        return []
    df = pd.DataFrame(posts)
    # ensure timestamp is datetime
    df['timestamp'] = pd.to_datetime(df['timestamp'], utc=True)
    df['hour_utc'] = df['timestamp'].dt.hour
    df['engagement'] = df.get('engagement', df.get('likes',0) + df.get('comments',0))
    agg = df.groupby('hour_utc')['engagement'].agg(['sum','count']).reset_index()
    agg['avg_engagement'] = agg['sum'] / agg['count']
    agg = agg.sort_values('avg_engagement', ascending=False)
    top_hours = agg.head(3)['hour_utc'].tolist()
    return top_hours

# Example usage:
# posts = [{'timestamp':'2025-08-01T10:00:00Z','likes':100,'comments':5}, ...]
# compute_optimal_hours(posts)

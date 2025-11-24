# tools/analytics/dashboard.py

import streamlit as st
import pandas as pd
import json
from .events_store import EventStore


def show_dashboard():
    st.title("Analytics Dashboard")

    try:
        events = EventStore.query_events(limit=200)
    except Exception as e:
        st.error(f"Error loading events: {e}")
        return

    rows = []
    for event in events:
        try:
            payload = json.loads(event.payload)
        except json.JSONDecodeError:
            payload = {"error": "Invalid JSON payload"}

        rows.append({
            **payload,
            "created_at": event.created_at,
            "event_type": getattr(event, "event_type", None),
            "user_id": getattr(event, "user_id", None),
        })

    if not rows:
        st.info("No events found yet.")
        return

    df = pd.DataFrame(rows)

    # 📌 Optional: Pretty time formatting
    if "created_at" in df.columns:
        df["created_at"] = pd.to_datetime(df["created_at"]).dt.strftime("%Y-%m-%d %H:%M:%S")

    st.subheader("📊 Recent Events")
    st.dataframe(df, use_container_width=True)

    # 📈 Optional: Quick metrics summary
    st.subheader("Metrics Summary")

    event_counts = df["event_type"].value_counts() if "event_type" in df else None

    if event_counts is not None:
        st.bar_chart(event_counts)
    else:
        st.write("No event types available for summary.")


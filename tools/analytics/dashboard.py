import streamlit as st
from .events_store import EventStore
import pandas as pd
import json

def show_dashboard():
    st.title("Analytics Dashboard")
    events = EventStore.query_events(200)
    rows = []
    for e in events:
        obj = json.loads(e.payload)
        rows.append({**obj, "created_at": e.created_at})
    if rows:
        df = pd.DataFrame(rows)
        st.dataframe(df)
    else:
        st.info("No events yet.")

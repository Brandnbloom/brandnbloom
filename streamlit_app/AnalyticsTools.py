import streamlit as st
import requests
from .config import BACKEND_URL

st.title("📊 Analytics & Reporting Tools")

# --- Authentication Check ---
if "token" not in st.session_state:
    st.warning("Please login first.")
    st.stop()

headers = {"Authorization": f"Bearer {st.session_state['token']}"}

# =============================================================================
# 1. LOG EVENT
# =============================================================================
st.subheader("📝 Log Event")

with st.form("log_event_form"):
    event_name = st.text_input("Event Name")
    value = st.number_input("Value", min_value=0.0, step=1.0)
    submit_log = st.form_submit_button("Log Event")

if submit_log:
    if not event_name.strip():
        st.error("Event name cannot be empty.")
    else:
        resp = requests.post(
            f"{BACKEND_URL}/api/analytics/log-event",
            params={"event_name": event_name, "value": value},
            headers=headers
        )
        if resp.status_code == 200:
            st.success("Event logged successfully!")
            st.json(resp.json())
        else:
            st.error(resp.text)


# =============================================================================
# 2. VIEW ANALYTICS
# =============================================================================
st.subheader("📈 View Analytics Summary")

if st.button("Load Analytics"):
    resp = requests.get(f"{BACKEND_URL}/api/analytics/analytics", headers=headers)

    if resp.status_code == 200:
        data = resp.json()

        if not data:
            st.info("No analytics data available yet.")
        else:
            st.json(data)

    else:
        st.error("Error fetching analytics.")


# =============================================================================
# 3. GENERATE REPORT
# =============================================================================
st.subheader("📄 Generate Detailed Report")

if st.button("Generate Report"):
    resp = requests.get(f"{BACKEND_URL}/api/analytics/report", headers=headers)

    if resp.status_code == 200:
        report = resp.json()
        st.success("Report generated successfully!")
        st.json(report)
    else:
        st.error("Error generating report.")

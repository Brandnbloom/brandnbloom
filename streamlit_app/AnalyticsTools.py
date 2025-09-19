import streamlit as st
import requests
from .config import BACKEND_URL

st.title("Analytics & Reporting Tools")

if "token" not in st.session_state:
    st.warning("Please login first.")
    st.stop()

headers = {"Authorization": f"Bearer {st.session_state['token']}"}

# ---------------- Log Event ----------------
st.subheader("Log Event")
event_name = st.text_input("Event Name")
value = st.number_input("Value", min_value=0.0, step=1.0)

if st.button("Log Event"):
    response = requests.post(f"{BACKEND_URL}/api/analytics/log-event",
                             params={"event_name": event_name, "value": value},
                             headers=headers)
    if response.status_code == 200:
        st.success("Event logged successfully!")
        st.json(response.json())
    else:
        st.error("Error logging event.")

# ---------------- View Analytics ----------------
st.subheader("View Analytics")
if st.button("Load Analytics"):
    response = requests.get(f"{BACKEND_URL}/api/analytics/analytics", headers=headers)
    if response.status_code == 200:
        data = response.json()
        st.json(data)
    else:
        st.error("Error fetching analytics.")

# ---------------- Generate Report ----------------
st.subheader("Generate Report")
if st.button("Generate Report"):
    response = requests.get(f"{BACKEND_URL}/api/analytics/report", headers=headers)
    if response.status_code == 200:
        report = response.json()
        st.json(report)
    else:
        st.error("Error generating report.")


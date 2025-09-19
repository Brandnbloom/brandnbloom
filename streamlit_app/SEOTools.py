import streamlit as st
import requests
from .config import BACKEND_URL

st.title("SEO Tools")

if "token" not in st.session_state:
    st.warning("Please login first to access SEO Tools.")
    st.stop()

# ---------------- SEO Audit ----------------
st.subheader("SEO Audit")
audit_url = st.text_input("Enter website URL to audit")

if st.button("Run SEO Audit"):
    headers = {"Authorization": f"Bearer {st.session_state['token']}"}
    response = requests.get(f"{BACKEND_URL}/tools/seo-audit", params={"url": audit_url}, headers=headers)
    if response.status_code == 200:
        data = response.json()
        st.json(data)
    else:
        st.error("Error running SEO audit.")

# ---------------- Keyword Tracker ----------------
st.subheader("Keyword Tracker")
kw_url = st.text_input("Website URL for keyword tracking")
keyword = st.text_input("Keyword to track")

if st.button("Add Keyword"):
    headers = {"Authorization": f"Bearer {st.session_state['token']}"}
    response = requests.post(f"{BACKEND_URL}/tools/keyword-track", params={"url": kw_url, "keyword": keyword}, headers=headers)
    if response.status_code == 200:
        st.success("Keyword added!")
        st.json(response.json())
    else:
        st.error("Error adding keyword.")

if st.button("View My Keywords"):
    headers = {"Authorization": f"Bearer {st.session_state['token']}"}
    response = requests.get(f"{BACKEND_URL}/tools/keyword-track", headers=headers)
    if response.status_code == 200:
        st.json(response.json())
    else:
        st.error("Error fetching keywords.")

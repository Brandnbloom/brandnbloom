import streamlit as st
import requests
from .config import BACKEND_URL

st.title("SEO Tools")

# ---------------- Check Login ----------------
if "token" not in st.session_state:
    st.warning("Please login first to access SEO Tools.")
    st.stop()

headers = {"Authorization": f"Bearer {st.session_state['token']}"}

# ---------------- SEO Audit ----------------
st.subheader("SEO Audit")
audit_url = st.text_input("Enter website URL to audit")

if st.button("Run SEO Audit"):
    try:
        response = requests.get(
            f"{BACKEND_URL}/api/seo/audit",
            params={"url": audit_url},
            headers=headers,
            timeout=15
        )
        if response.status_code == 200:
            st.json(response.json())
        else:
            st.error(response.json().get("detail", "Error running SEO audit."))
    except Exception as e:
        st.error(f"Connection error: {e}")

# ---------------- Keyword Tracker ----------------
st.subheader("Keyword Tracker")
kw_url = st.text_input("Website URL for keyword tracking")
keyword = st.text_input("Keyword to track")

if st.button("Add Keyword"):
    try:
        response = requests.post(
            f"{BACKEND_URL}/api/keywords/add",
            params={"url": kw_url, "keyword": keyword},
            headers=headers,
            timeout=15
        )
        if response.status_code == 200:
            st.success("Keyword added successfully!")
            st.json(response.json())
        else:
            st.error(response.json().get("detail", "Error adding keyword."))
    except Exception as e:
        st.error(f"Connection error: {e}")

if st.button("View My Keywords"):
    try:
        response = requests.get(
            f"{BACKEND_URL}/api/keywords/list",
            headers=headers,
            timeout=15
        )
        if response.status_code == 200:
            st.json(response.json())
        else:
            st.error("Error fetching keywords.")
    except Exception as e:
        st.error(f"Connection error: {e}")

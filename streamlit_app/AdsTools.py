import streamlit as st
import requests
from .config import BACKEND_URL

st.title("Ads & Marketing Tools")

if "token" not in st.session_state:
    st.warning("Please login first.")
    st.stop()

# ---------------- Create Ad ----------------
st.subheader("Create Ad Campaign")
campaign_name = st.text_input("Campaign Name")
platform = st.selectbox("Platform", ["Google", "Facebook", "LinkedIn"])
budget = st.number_input("Budget ($)", min_value=1.0, step=1.0)
content = st.text_area("Ad Content")

if st.button("Create Ad"):
    headers = {"Authorization": f"Bearer {st.session_state['token']}"}
    response = requests.post(f"{BACKEND_URL}/tools/create-ad",
                             params={"campaign_name": campaign_name, "platform": platform, "budget": budget, "content": content},
                             headers=headers)
    if response.status_code == 200:
        st.success("Ad created successfully!")
        st.json(response.json())
    else:
        st.error("Error creating ad.")

if st.button("View My Ads"):
    headers = {"Authorization": f"Bearer {st.session_state['token']}"}
    response = requests.get(f"{BACKEND_URL}/tools/my-ads", headers=headers)
    if response.status_code == 200:
        st.json(response.json())
    else:
        st.error("Error fetching ads.")

# ---------------- Creative Generator ----------------
st.subheader("AI Creative Generator")
ad_type = st.selectbox("Ad Type", ["Text Copy", "Image"])
prompt = st.text_input("Creative Prompt")

if st.button("Generate Creative"):
    headers = {"Authorization": f"Bearer {st.session_state['token']}"}
    response = requests.post(f"{BACKEND_URL}/tools/generate-creative",
                             params={"ad_type": ad_type, "prompt": prompt},
                             headers=headers)
    if response.status_code == 200:
        st.json(response.json())
    else:
        st.error("Error generating creative.")

# ---------------- Budget Optimizer ----------------
st.subheader("Optimize Budget")
ad_id = st.number_input("Ad ID", min_value=0, step=1)

if st.button("Optimize Budget"):
    headers = {"Authorization": f"Bearer {st.session_state['token']}"}
    response = requests.post(f"{BACKEND_URL}/tools/optimize-budget", params={"ad_id": ad_id}, headers=headers)
    if response.status_code == 200:
        st.json(response.json())
    else:
        st.error("Error optimizing budget.")

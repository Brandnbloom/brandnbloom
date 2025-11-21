import streamlit as st
import requests
from .config import BACKEND_URL

st.title("📢 Ads & Marketing Tools")

if "token" not in st.session_state:
    st.warning("Please login first.")
    st.stop()

auth_header = {"Authorization": f"Bearer {st.session_state['token']}"}

# ---------------------------------------------------------
# CREATE AD CAMPAIGN
# ---------------------------------------------------------
st.subheader("📝 Create Ad Campaign")

with st.form("create_ad_form"):
    campaign_name = st.text_input("Campaign Name")
    platform = st.selectbox("Platform", ["Google", "Facebook", "LinkedIn"])
    budget = st.number_input("Budget ($)", min_value=1.0, step=1.0)
    content = st.text_area("Ad Content")

    create_ad_btn = st.form_submit_button("Create Ad")

if create_ad_btn:
    if not campaign_name or not content:
        st.error("Campaign name and content are required.")
    else:
        resp = requests.post(
            f"{BACKEND_URL}/tools/create-ad",
            params={
                "campaign_name": campaign_name,
                "platform": platform,
                "budget": budget,
                "content": content,
            },
            headers=auth_header
        )
        if resp.status_code == 200:
            st.success("Ad created successfully!")
            st.json(resp.json())
        else:
            st.error(resp.text)


# ---------------------------------------------------------
# VIEW ALL ADS
# ---------------------------------------------------------
st.subheader("📄 My Ads")

if st.button("View My Ads"):
    resp = requests.get(f"{BACKEND_URL}/tools/my-ads", headers=auth_header)
    if resp.status_code == 200:
        ads = resp.json()
        if not ads:
            st.info("No ads found.")
        else:
            st.json(ads)
    else:
        st.error("Error fetching ads.")


# ---------------------------------------------------------
# CREATIVE GENERATOR (AI)
# ---------------------------------------------------------
st.subheader("🎨 AI Creative Generator")

with st.form("creative_form"):
    ad_type = st.selectbox("Ad Type", ["Text Copy", "Image"])
    prompt = st.text_input("Creative Prompt")
    creative_btn = st.form_submit_button("Generate Creative")

if creative_btn:
    if not prompt:
        st.error("Prompt cannot be empty.")
    else:
        resp = requests.post(
            f"{BACKEND_URL}/tools/generate-creative",
            params={"ad_type": ad_type, "prompt": prompt},
            headers=auth_header
        )
        if resp.status_code == 200:
            output = resp.json()
            st.success("Creative generated!")

            if ad_type == "Text Copy":
                st.write(output.get("creative_text", ""))
            else:
                # Backend returns image URL or base64
                if "image_url" in output:
                    st.image(output["image_url"])
                elif "image_base64" in output:
                    st.image(output["image_base64"])
                else:
                    st.json(output)
        else:
            st.error("Error generating creative.")


# ---------------------------------------------------------
# BUDGET OPTIMIZER
# ---------------------------------------------------------
st.subheader("💰 Budget Optimizer")

with st.form("optimize_form"):
    ad_id = st.number_input("Ad ID", min_value=1, step=1)
    optimize_btn = st.form_submit_button("Optimize Budget")

if optimize_btn:
    resp = requests.post(
        f"{BACKEND_URL}/tools/optimize-budget",
        params={"ad_id": ad_id},
        headers=auth_header
    )
    if resp.status_code == 200:
        st.success("Budget optimized!")
        st.json(resp.json())
    else:
        st.error("Error optimizing budget.")

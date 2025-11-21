import streamlit as st
import requests
from .config import BACKEND_URL

st.title("👥 CRM & Lead Generation Tools")

# ---------------- AUTH CHECK ----------------
if "token" not in st.session_state:
    st.warning("Please login first.")
    st.stop()

headers = {"Authorization": f"Bearer {st.session_state['token']}"}


# =============================================================================
# 1. CREATE NEW LEAD
# =============================================================================
st.subheader("➕ Add New Lead")

with st.form("create_lead_form"):
    name = st.text_input("Name")
    email = st.text_input("Email")
    phone = st.text_input("Phone")
    source = st.text_input("Source (e.g., Instagram, Website, Referral)")
    submit_lead = st.form_submit_button("Create Lead")

if submit_lead:
    if not name.strip():
        st.error("Name cannot be empty.")
    elif not email.strip():
        st.error("Email cannot be empty.")
    else:
        resp = requests.post(
            f"{BACKEND_URL}/api/crm/create-lead",
            params={"name": name, "email": email, "phone": phone, "source": source},
            headers=headers
        )
        if resp.status_code == 200:
            st.success("Lead created successfully!")
            st.json(resp.json())
        else:
            st.error("Error creating lead.")


# =============================================================================
# 2. VIEW LEADS
# =============================================================================
st.subheader("📋 My Leads")

if st.button("Load Leads"):
    resp = requests.get(f"{BACKEND_URL}/api/crm/leads", headers=headers)

    if resp.status_code == 200:
        leads = resp.json()

        if not leads:
            st.info("No leads found.")
        else:
            for idx, lead in enumerate(leads):
                st.markdown(
                    f"""
                    **ID:** {idx}  
                    **Name:** {lead['name']}  
                    **Email:** {lead['email']}  
                    **Phone:** {lead.get('phone', '-')}  
                    **Source:** {lead.get('source', '-')}  
                    **Status:** {lead['status']}  
                    ---
                    """
                )
    else:
        st.error("Error loading leads.")


# =============================================================================
# 3. UPDATE LEAD STATUS
# =============================================================================
st.subheader("🛠 Update Lead Status")

with st.form("update_status_form"):
    lead_index = st.number_input("Lead ID", min_value=0, step=1)
    new_status = st.text_input("New Status (e.g., New, Contacted, Qualified, Won, Lost)")
    update_btn = st.form_submit_button("Update Status")

if update_btn:
    if not new_status.strip():
        st.error("Status cannot be empty.")
    else:
        resp = requests.put(
            f"{BACKEND_URL}/api/crm/update-status",
            params={"lead_index": lead_index, "status": new_status},
            headers=headers
        )
        if resp.status_code == 200:
            st.success("Lead updated successfully!")
            st.json(resp.json())
        else:
            st.error("Error updating lead.")

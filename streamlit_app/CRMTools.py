import streamlit as st
import requests
from .config import BACKEND_URL

st.title("CRM & Lead Generation Tools")

if "token" not in st.session_state:
    st.warning("Please login first.")
    st.stop()

headers = {"Authorization": f"Bearer {st.session_state['token']}"}

# ---------------- Create Lead ----------------
st.subheader("Add New Lead")
name = st.text_input("Name")
email = st.text_input("Email")
phone = st.text_input("Phone")
source = st.text_input("Source")

if st.button("Create Lead"):
    response = requests.post(f"{BACKEND_URL}/api/crm/create-lead",
                             params={"name": name, "email": email, "phone": phone, "source": source},
                             headers=headers)
    if response.status_code == 200:
        st.success("Lead created successfully!")
        st.json(response.json())
    else:
        st.error("Error creating lead.")

# ---------------- View Leads ----------------
st.subheader("My Leads")
if st.button("Load Leads"):
    response = requests.get(f"{BACKEND_URL}/api/crm/leads", headers=headers)
    if response.status_code == 200:
        leads = response.json()
        for idx, lead in enumerate(leads):
            st.write(f"{idx}: {lead['name']} - {lead['email']} - Status: {lead['status']}")
    else:
        st.error("Error loading leads.")

# ---------------- Update Lead Status ----------------
st.subheader("Update Lead Status")
lead_index = st.number_input("Lead ID", min_value=0, step=1)
new_status = st.text_input("New Status")

if st.button("Update Status"):
    response = requests.put(f"{BACKEND_URL}/api/crm/update-status",
                            params={"lead_index": lead_index, "status": new_status},
                            headers=headers)
    if response.status_code == 200:
        st.success("Lead updated successfully!")
        st.json(response.json())
    else:
        st.error("Error updating lead.")

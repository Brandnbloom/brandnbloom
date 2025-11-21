import streamlit as st
import requests
from .config import BACKEND_URL

st.title("🌸 Brand n Bloom — Dashboard")

# ---------------- AUTH CHECK ----------------
if "token" not in st.session_state:
    st.warning("Please login first.")
    st.stop()

headers = {"Authorization": f"Bearer {st.session_state['token']}"}

# ---------------- USER PROFILE ----------------
st.subheader("👤 Your Profile")

user_resp = requests.get(f"{BACKEND_URL}/auth/me", headers=headers)

if user_resp.status_code == 200:
    user = user_resp.json()
    st.success("Profile loaded!")

    st.markdown(
        f"""
        **Name:** {user.get('name', 'User')}  
        **Email:** {user.get('email', '-')}  
        **Plan:** {user.get('plan', 'Free')}  
        **Member Since:** {user.get('created_at', '-')}  
        """
    )
else:
    st.error("Could not load your profile.")


# ---------------- USAGE STATS (UI Placeholder) ----------------
st.subheader("📊 Usage Summary")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Articles Generated", "–")
with col2:
    st.metric("Brand Kits Created", "–")
with col3:
    st.metric("Leads Added", "–")

st.caption("Usage stats will update automatically as your backend grows.")


# ---------------- PLAN & BILLING ----------------
st.subheader("💳 Upgrade / Manage Subscription")

st.write("Unlock unlimited SEO tools, branding tools, analytics & CRM automation.")

if st.button("Upgrade Plan"):
    response = requests.post(
        f"{BACKEND_URL}/billing/create-checkout-session",
        headers=headers
    )
    if response.status_code == 200:
        checkout_url = response.json().get("checkout_url")
        st.success("Checkout session created!")
        st.markdown(f"👉 **[Click here to upgrade]({checkout_url})**")
    else:
        st.error("Error creating checkout session.")


# ---------------- QUICK LINKS ----------------
st.subheader("🚀 Quick Access")

colA, colB = st.columns(2)

with colA:
    st.markdown("🔧 **[Branding Tools](./BrandingTools)**")
    st.markdown("🖋 **[Writer Tools](./WriterTools)**")
    st.markdown("📢 **[Ads Tools](./AdsTools)**")

with colB:
    st.markdown("📊 **[Analytics](./AnalyticsTools)**")
    st.markdown("👥 **[CRM Tools](./CRMTools)**")
    st.markdown("🏷 **[Brand Kit Generator](./BrandKitTools)**")


# ---------------- LOGOUT ----------------
st.subheader("🔒 Logout")

if st.button("Logout"):
    st.session_state.clear()
    st.success("Logged out! Please refresh the page.")

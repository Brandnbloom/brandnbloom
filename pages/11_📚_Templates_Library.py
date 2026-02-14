import streamlit as st
from utils.ui import inject_css, dark_mode_toggle

inject_css(); st.title("📚 Templates Library"); dark_mode_toggle()

tabs = st.tabs(["Captions", "Hashtags", "Emails", "Proposals", "Calendars"])
with tabs[0]:
    st.write("Swipeable caption starters:")
    st.code("Hook + Value + CTA\nExample: Ready to 5x your reach? Here's the playbook... ➜ Save this!")
with tabs[1]:
    st.write("Mix of large/mid/long-tail tags. Edit per niche.")
with tabs[2]:
    st.write("Welcome email, nurture sequence, promo blast — ready-to-edit.")
with tabs[3]:
    st.write("Client proposal one-pagers with outcomes & timelines.")
with tabs[4]:
    st.write("30-day content calendar skeleton with theme pillars.")

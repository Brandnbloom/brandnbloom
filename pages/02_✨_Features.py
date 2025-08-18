import streamlit as st
from utils.ui import inject_css, dark_mode_toggle
inject_css()
st.title("✨ Features")
dark_mode_toggle()
st.markdown("""
**Analytics**
- BloomInsight (IG analytics, KPIs, brand health, recos, best times)
- Competitor analysis, historical tracking

**AI Tools**
- Bloomscore, Caption & Hashtag generator, Visual Audit
- Influencer Finder, Email Automations, Scheduler
- Templates Library, Reel Script Generator, Local SEO Audit

**Operations**
- Client Onboarding Assistant, Proposal Generator, Auto Content Calendar
- Recurring Report Generator, Bloom CRM, Ads Helper, API Prompt Packs
""")

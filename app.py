import streamlit as st

# Set the page configuration
st.set_page_config(page_title="Brand n Bloom", layout="wide")

# Title and intro
st.title("🌸 Brand n Bloom")
st.markdown("""
Welcome to **Brand n Bloom** — where brands blossom beyond borders.

We’re a boutique, AI-powered marketing agency helping global restaurants and hospitality businesses scale with intelligent SEO, performance-driven digital strategies, and creative storytelling.
""")

# Tools section
st.header("✨ Try Our AI Tools")

# Add page links to tools in the pages/ folder
st.page_link("pages/review_reply_assistant.py", label="📝 Review Reply Assistant")
st.page_link("pages/visual_brand_audit.py", label="🎨 Visual Brand Audit")

# Future tools (coming soon)
st.markdown("""
---

🛠 **Coming Soon:**
- 🌟 BloomScore (AI-powered brand score)
- 📷 AI Competitor Snapshot
- 🧾 Digital Menu Designer
- 📊 Multi-Channel Dashboard

""")

# Contact footer
st.markdown("---")
st.markdown("""
📞 **Contact Us**  
📱 WhatsApp: [+91 9619617877](https://wa.me/919619617877)  
📧 Email: agency@brandnbloom.com  
📍 Location: India-based, globally driven 🌍  
🔗 Instagram: [@brand_n_bloom](https://instagram.com/brand_n_bloom)
""")# Main homepage

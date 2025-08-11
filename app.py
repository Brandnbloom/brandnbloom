import streamlit as st
import streamlit.components.v1 as components

# Page settings
st.set_page_config(page_title="Brand n Bloom", layout="wide")

# --- PWA + Meta tags ---
st.markdown("""
<link rel="manifest" href="static/manifest.json" />
<meta name="theme-color" content="#FF2898" />
<link rel="apple-touch-icon" href="static/icon-192.png">
<link rel="icon" href="static/favicon.ico" type="image/x-icon">
<meta name="google-site-verification" content="YE75SNSAONjr9Y4IYqOZiA1dkG5OYRIstxk-SdSJEZY" />
""", unsafe_allow_html=True)

# --- Service Worker Registration ---
components.html("""
<script>
if ("serviceWorker" in navigator) {
  window.addEventListener("load", () => {
    navigator.serviceWorker
      .register("static/service-worker.js")
      .then((reg) => console.log("✅ SW registered", reg))
      .catch((err) => console.error("❌ SW registration failed", err));
  });
}
</script>
""", height=0)

# Banner
st.image("assets/banner.png", use_container_width=True)

# Welcome text
st.markdown("""
<style>
    .main-title {
        font-size: 32px;
        font-weight: 600;
        color: #3c3c3c;
    }
    .subtext {
        font-size: 18px;
        color: #666;
    }
</style>

<div class="main-title">Welcome to Brand n Bloom 🌸</div>
<div class="subtext">
    Unleash the power of branding with AI. Our tools empower restaurants and brands to analyze, grow, and bloom creatively.
</div>
""", unsafe_allow_html=True)

# --- Collapsible Menu ---
with st.expander("📂 Click here to explore all tools and info sections"):
    col1, col2, col3 = st.columns(3)

    with col1:
        st.page_link("pages/BloomScore.py", label="📊 BloomScore")
        st.page_link("pages/Consumer_Behavior.py", label="🧠 DinePsych")
        st.page_link("pages/Visual_Audit.py", label="🎨 Visual Audit")
        st.page_link("pages/Review_Reply.py", label="💬 Review Assistant")

    with col2:
        st.page_link("pages/Digital_Menu.py", label="📄 Digital Menu")
        st.page_link("pages/BloomInsight.py", label="📈 BloomInsight")
        st.page_link("pages/blogs.py", label="📝 Blogs")
        st.page_link("pages/contact_us.py", label="📬 Contact")

    with col3:
        st.page_link("pages/about_us.py", label="👥 About Us")
        st.page_link("pages/about_ceo.py", label="👩‍💼 About CEO")
        st.page_link("pages/our_services.py", label="🛠️ Our Services")
        st.page_link("pages/manifesto.py", label="📜 Manifesto")
        st.page_link("pages/legal.py", label="⚖️ Terms & Privacy")
        st.page_link("pages/disclaimer.py", label="🛑 Disclaimer")

# --- Google Translate ---
components.html("""
<div id="google_translate_element"></div>
<script type="text/javascript">
function googleTranslateElementInit() {
  new google.translate.TranslateElement({pageLanguage: 'en'}, 'google_translate_element');
}
</script>
<script src="//translate.google.com/translate_a/element.js?cb=googleTranslateElementInit"></script>
""", height=60)

# --- Tawk.to Live Chat ---
components.html("""
<script type="text/javascript">
var Tawk_API=Tawk_API||{}, Tawk_LoadStart=new Date();
(function(){
var s1=document.createElement("script"),s0=document.getElementsByTagName("script")[0];
s1.async=true;
s1.src='https://embed.tawk.to/6860e99d73af5e1912a4fcb7/1iut914c9';
s1.charset='UTF-8';
s1.setAttribute('crossorigin','*');
s0.parentNode.insertBefore(s1,s0);
})();
</script>
""", height=0)

# --- Cookie Consent ---
def cookie_consent():
    if "accepted_cookies" not in st.session_state:
        st.session_state.accepted_cookies = False

    if not st.session_state.accepted_cookies:
        with st.expander("🍪 We use cookies! Click to accept."):
            if st.button("Accept Cookies"):
                st.session_state.accepted_cookies = True
                st.success("Thank you for accepting cookies!")

cookie_consent()

# --- Google Analytics ---
components.html("""
<script async src="https://www.googletagmanager.com/gtag/js?id=G-0GBTQZDD53"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-0GBTQZDD53');
</script>
""", height=0)

# --- Responsive Cards CSS ---
from utils import responsive_cards_css
responsive_cards_css()

# --- Tool Cards ---
tools = [
    {"name": "BloomScore", "desc": "Audit your social & web presence.", "url": "/BloomScore"},
    {"name": "DinePsych", "desc": "Analyze customer behavior in restaurants.", "url": "/Consumer-Behavior"},
    {"name": "Visual Audit", "desc": "Screenshot-based brand tone check.", "url": "/Visual-Audit"},
    {"name": "Review Assistant", "desc": "Reply to reviews with emotion-based tone.", "url": "/Review-Reply"},
    {"name": "Digital Menu Creator", "desc": "Generate restaurant menus with Canva-ready design.", "url": "/Digital-Menu"},
    {"name": "BloomInsight", "desc": "Track SEO, traffic, and GMB in one dashboard.", "url": "/BloomInsight"}
]

st.markdown("<div class='tool-card-container'>", unsafe_allow_html=True)
for tool in tools:
    st.markdown(f"""
    <div class='tool-card'>
        <h4>{tool["name"]}</h4>
        <p>{tool["desc"]}</p>
        <a href="{tool['url']}">🚀 Try Now</a>
    </div>
    """, unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

# --- Usage Check ---
from utils import check_usage_and_alert
check_usage_and_alert()

# Footer
st.markdown("""
<hr>
<p style='text-align: center; font-size: 0.9em;'>© 2025 Brand n Bloom. All rights reserved.</p>
""", unsafe_allow_html=True)

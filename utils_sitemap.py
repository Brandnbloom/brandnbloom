import os
import requests
from datetime import datetime

# ================= CONFIG =================
DOMAIN = "https://your-domain.onrender.com"  # Change this to your deployed domain
STATIC_DIR = "static"
SITEMAP_FILE = os.path.join(STATIC_DIR, "sitemap.xml")
# ===========================================

# Pages you want in your sitemap
PAGES = [
    "/",  # Homepage
    "/BloomScore",
    "/Consumer-Behavior",
    "/Visual-Audit",
    "/Review-Reply",
    "/Digital-Menu",
    "/BloomInsight",
    "/blogs",
    "/contact_us",
    "/about_us",
    "/about_ceo",
    "/our_services",
    "/manifesto",
    "/legal",
    "/disclaimer"
]

def generate_sitemap():
    """Generate sitemap.xml file."""
    if not os.path.exists(STATIC_DIR):
        os.makedirs(STATIC_DIR)

    urlset_open = '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
    urlset_close = '</urlset>'
    urls = []

    for page in PAGES:
        loc = f"{DOMAIN}{page}"
        lastmod = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
        urls.append(f"""
        <url>
            <loc>{loc}</loc>
            <lastmod>{lastmod}</lastmod>
            <changefreq>weekly</changefreq>
            <priority>0.8</priority>
        </url>
        """)

    sitemap_content = f"{urlset_open}{''.join(urls)}{urlset_close}"

    with open(SITEMAP_FILE, "w", encoding="utf-8") as f:
        f.write(sitemap_content.strip())

    print(f"✅ Sitemap generated at {SITEMAP_FILE}")


def ping_search_engines():
    """Ping Google and Bing to notify about updated sitemap."""
    sitemap_url = f"{DOMAIN}/static/sitemap.xml"
    engines = {
        "Google": f"https://www.google.com/ping?sitemap={sitemap_url}",
        "Bing": f"https://www.bing.com/ping?sitemap={sitemap_url}"
    }

    for name, url in engines.items():
        try:
            resp = requests.get(url, timeout=10)
            if resp.status_code == 200:
                print(f"✅ {name} ping successful")
            else:
                print(f"⚠️ {name} ping returned {resp.status_code}")
        except Exception as e:
            print(f"❌ {name} ping failed: {e}")


def update_sitemap_and_ping():
    """Full process: generate sitemap then ping search engines."""
    try:
        generate_sitemap()
        ping_search_engines()
    except Exception as e:
        print(f"❌ Failed to update sitemap: {e}")

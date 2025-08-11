import os
import requests
from datetime import datetime

# ===== CONFIG =====
DOMAIN = "https://www.brand-and-bloom.com"
STATIC_ROUTES = [
    "",  # Home
    "pages/about_us",
    "pages/about_ceo",
    "pages/our_services",
    "pages/contact_us",
    "pages/legal",
    "pages/disclaimer",
    "pages/manifesto",
    "pages/blogs",
]
CHANGEFREQ = "weekly"
PRIORITY = "0.7"
SITEMAP_FILENAME = "static/sitemap.xml"
SITEMAP_URL = f"{DOMAIN}/static/sitemap.xml"  # Must match hosted path
# ==================

def generate_sitemap():
    try:
        all_routes = STATIC_ROUTES.copy()

        # Add any ".py" pages from "pages" folder
        if os.path.exists("pages"):
            for filename in os.listdir("pages"):
                if filename.endswith(".py"):
                    route = f"pages/{filename.replace('.py', '')}"
                    if route not in all_routes:
                        all_routes.append(route)

        # Build XML content
        lines = ['<?xml version="1.0" encoding="UTF-8"?>']
        lines.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')

        for route in all_routes:
            url = f"{DOMAIN}/{route}" if route else DOMAIN
            lines.append("  <url>")
            lines.append(f"    <loc>{url}</loc>")
            lines.append(f"    <lastmod>{datetime.today().date()}</lastmod>")
            lines.append(f"    <changefreq>{CHANGEFREQ}</changefreq>")
            lines.append(f"    <priority>{PRIORITY}</priority>")
            lines.append("  </url>")

        lines.append("</urlset>")

        os.makedirs("static", exist_ok=True)
        with open(SITEMAP_FILENAME, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))

        print(f"✅ Sitemap generated at {SITEMAP_FILENAME}")
    except Exception as e:
        print(f"⚠️ Sitemap generation failed: {e}")

def ping_google():
    try:
        ping_url = f"https://www.google.com/ping?sitemap={SITEMAP_URL}"
        r = requests.get(ping_url, timeout=10)
        if r.status_code == 200:
            print(f"🚀 Google ping successful: {ping_url}")
        else:
            print(f"⚠️ Google ping returned status {r.status_code}")
    except Exception as e:
        print(f"❌ Error pinging Google: {e}")

def update_sitemap_and_ping():
    generate_sitemap()
    ping_google()

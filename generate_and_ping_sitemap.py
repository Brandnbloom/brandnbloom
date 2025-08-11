import os
import requests
from datetime import datetime

# ===== CONFIG =====
DOMAIN = "https://www.brand-n-bloom.com"
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
SITEMAP_URL = https://www.brand-n-bloom.com/static/sitemap.xml  # Must match your hosted path
# ==================

def generate_sitemap():
    all_routes = STATIC_ROUTES.copy()

    # Add .py pages from "pages" folder
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

def ping_google():
    ping_url = f"https://www.google.com/ping?sitemap={SITEMAP_URL}"
    try:
        r = requests.get(ping_url, timeout=10)
        if r.status_code == 200:
            print(f"🚀 Successfully pinged Google: {ping_url}")
        else:
            print(f"⚠ Google ping returned status {r.status_code}")
    except Exception as e:
        print(f"❌ Error pinging Google: {e}")

if __name__ == "__main__":
    generate_sitemap()
    ping_google()

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
SITEMAP_URL = f"{DOMAIN}/static/sitemap.xml"  # Must match hosted path
# ==================

def generate_sitemap():
    """Generates sitemap.xml for static pages and pages/*.py files."""
    all_routes = STATIC_ROUTES.copy()

    # Add .py pages from the "pages" folder
    pages_dir = "pages"
    if os.path.exists(pages_dir):
        for filename in os.listdir(pages_dir):
            if filename.endswith(".py"):
                route = f"{pages_dir}/{filename.replace('.py', '')}"
                if route not in all_routes:
                    all_routes.append(route)

    # Build XML content
    lines = ['<?xml version="1.0" encoding="UTF-8"?>']
    lines.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')

    today = datetime.today().date()
    for route in all_routes:
        url = f"{DOMAIN}/{route}" if route else DOMAIN
        lines.extend([
            "  <url>",
            f"    <loc>{url}</loc>",
            f"    <lastmod>{today}</lastmod>",
            f"    <changefreq>{CHANGEFREQ}</changefreq>",
            f"    <priority>{PRIORITY}</priority>",
            "  </url>"
        ])

    lines.append("</urlset>")

    # Ensure directory exists
    os.makedirs(os.path.dirname(SITEMAP_FILENAME), exist_ok=True)

    # Write sitemap.xml
    with open(SITEMAP_FILENAME, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"✅ Sitemap generated at {SITEMAP_FILENAME}")


def ping_google():
    """Pings Google to notify about sitemap update."""
    ping_url = f"https://www.google.com/ping?sitemap={SITEMAP_URL}"
    try:
        response = requests.get(ping_url, timeout=10)
        if response.status_code == 200:
            print(f"🚀 Successfully pinged Google: {ping_url}")
        else:
            print(f"⚠ Google ping returned status {response.status_code}")
    except Exception as e:
        print(f"❌ Error pinging Google: {e}")


if __name__ == "__main__":
    generate_sitemap()
    ping_google()

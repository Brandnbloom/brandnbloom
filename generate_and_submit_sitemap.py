import os
from datetime import datetime
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow

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
SCOPES = ['https://www.googleapis.com/auth/webmasters']
SITEMAP_FILENAME = "static/sitemap.xml"
SITEMAP_URL = f"{DOMAIN}/sitemap.xml"  # Make sure sitemap is hosted at this path
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

def submit_to_gsc():
    # Authenticate
    flow = InstalledAppFlow.from_client_secrets_file("client_secret.json", SCOPES)
    creds = flow.run_local_server(port=0)
    service = build('searchconsole', 'v1', credentials=creds)

    try:
        service.sitemaps().submit(siteUrl=DOMAIN, feedpath=SITEMAP_URL).execute()
        print(f"🚀 Sitemap submitted to Google Search Console: {SITEMAP_URL}")
    except Exception as e:
        print(f"❌ Error submitting sitemap: {e}")

if __name__ == "__main__":
    generate_sitemap()
    submit_to_gsc()

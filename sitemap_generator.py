import os
from datetime import datetime

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

def generate_sitemap():
    all_routes = STATIC_ROUTES.copy()

    # Add tool pages from pages/ folder
    for filename in os.listdir("pages"):
        if filename.endswith(".py"):
            route = f"pages/{filename.replace('.py', '')}"
            if route not in all_routes:
                all_routes.append(route)

    # Create XML
    lines = ['<?xml version="1.0" encoding="UTF-8"?>']
    lines.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')

    for route in all_routes:
        lines.append("  <url>")
        lines.append(f"    <loc>{DOMAIN}/{route}</loc>")
        lines.append(f"    <lastmod>{datetime.today().date()}</lastmod>")
        lines.append("    <changefreq>weekly</changefreq>")
        lines.append("    <priority>0.7</priority>")
        lines.append("  </url>")

    lines.append("</urlset>")

    # Save to static/sitemap.xml
    os.makedirs("static", exist_ok=True)
    with open("static/sitemap.xml", "w") as f:
        f.write("\n".join(lines))

    print("✅ Sitemap generated successfully.")

# Call this function only once during deployment
if _name_ == "_main_":
    generate_sitemap()

import os
import requests
from datetime import datetime
import xml.etree.ElementTree as ET

SITEMAP_FILE = "sitemap.xml"
BASE_URL = "https://www.brand-and-bloom.com"  # Change to your domain


def generate_sitemap():
    """Generate a sitemap.xml file if it doesn't exist."""
    urlset = ET.Element("urlset", xmlns="http://www.sitemaps.org/schemas/sitemap/0.9")

    # Example URLs — Add your actual pages here
    urls = [
        {"loc": BASE_URL, "priority": "1.0"},
        {"loc": f"{BASE_URL}/about", "priority": "0.8"},
        {"loc": f"{BASE_URL}/contact", "priority": "0.8"}
    ]

    for url in urls:
        url_tag = ET.SubElement(urlset, "url")
        ET.SubElement(url_tag, "loc").text = url["loc"]
        ET.SubElement(url_tag, "lastmod").text = datetime.utcnow().strftime("%Y-%m-%d")
        ET.SubElement(url_tag, "priority").text = url["priority"]

    tree = ET.ElementTree(urlset)
    tree.write(SITEMAP_FILE, encoding="utf-8", xml_declaration=True)


def ping_search_engines():
    """Ping Google and Bing to notify about updated sitemap."""
    sitemap_url = f"{BASE_URL}/{SITEMAP_FILE}"
    search_engines = {
        "Google": f"https://www.google.com/ping?sitemap={sitemap_url}",
        "Bing": f"https://www.bing.com/ping?sitemap={sitemap_url}"
    }

    results = {}
    for name, url in search_engines.items():
        try:
            response = requests.get(url, timeout=10)
            results[name] = response.status_code
        except Exception as e:
            results[name] = f"Error: {str(e)}"

    return results


def update_sitemap_and_ping():
    """Update sitemap.xml and ping search engines."""
    generate_sitemap()
    results = ping_search_engines()
    return results

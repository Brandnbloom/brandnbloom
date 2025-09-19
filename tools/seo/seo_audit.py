import streamlit as st
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

def basic_check(url):
    results = {}
    try:
        r = requests.get(url, timeout=8, headers={"User-Agent":"brandnbloom-bot/1.0"})
        results['status_code'] = r.status_code
        soup = BeautifulSoup(r.text, "html.parser")
        results['title'] = soup.title.string if soup.title else ""
        results['meta_description'] = (soup.find("meta", {"name":"description"}) or {}).get("content", "")
        results['h1'] = [h.get_text().strip() for h in soup.find_all("h1")]
        results['viewport'] = bool(soup.find("meta", {"name":"viewport"}))
        results['links'] = []
        for a in soup.find_all("a", href=True):
            href = urljoin(url, a['href'])
            results['links'].append(href)
    except Exception as e:
        results['error'] = str(e)
    return results

def find_broken_links(url, links):
    broken = []
    for link in set(links)[:200]:  # limit checks
        try:
            r = requests.head(link, allow_redirects=True, timeout=5)
            if r.status_code >= 400:
                broken.append({"link": link, "status": r.status_code})
        except Exception:
            broken.append({"link": link, "status": "error"})
    return broken

def show_seo_audit():
    st.title("SEO Audit Tool — Site Health Checker")
    url = st.text_input("Enter website URL (include https://)")
    if st.button("Run Audit"):
        st.info("Running audit (this runs simple checks, not a full crawl).")
        res = basic_check(url)
        st.json(res)
        if res.get("links"):
            st.write("Checking links (limited set)...")
            broken = find_broken_links(url, res['links'])
            st.write(f"Found {len(broken)} broken/errored links")
            st.dataframe(broken)

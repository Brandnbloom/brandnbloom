# tools/seo/seo_audit.py
import streamlit as st
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from collections import Counter, defaultdict
import math
import re
import json
import time
import socket
import ipaddress

USER_AGENT = {"User-Agent": "BrandnBloomBot/1.2 (+https://brandnbloom.ai)"}
REQUEST_TIMEOUT = 10
TOP_KEYWORDS = 15

# Basic English stopwords (small set; extend if needed)
STOPWORDS = {
    "the", "and", "a", "an", "in", "on", "for", "with", "to", "of", "is", "it",
    "this", "that", "by", "are", "as", "be", "or", "from", "at", "was", "were",
    "has", "have", "but", "not", "your", "you", "we", "our", "they", "their",
    "can", "will", "if", "so", "do", "does", "did", "about", "which"
}

# -------------------------
# Helper network functions
# -------------------------
def safe_get(url, method="get", timeout=REQUEST_TIMEOUT, allow_redirects=True, headers=USER_AGENT):
    """Perform a GET or HEAD safely; return dict {ok, status_code, text, headers, error}"""
      # Extra SSRF protection: verify actual destination IP is not private/reserved immediately before request
    try:
         parsed = urlparse(url)
        hostname = parsed.hostname
        if not hostname:
            return {"ok": False, "error": "Invalid URL"}
        try:
            results = socket.getaddrinfo(hostname, None)
            for result in results:
                ip = result[-1][0]
                if not is_url_allowed(f"http://{ip}"):
                    return {"ok": False, "error": f"Blocked: resolved IP {ip} is not allowed"}
        except Exception:
            return {"ok": False, "error": f"Could not resolve hostname {hostname}"}
        if method.lower() == "head":
            r = requests.head(url, timeout=timeout, allow_redirects=allow_redirects, headers=headers)
        else:
            r = requests.get(url, timeout=timeout, allow_redirects=allow_redirects, headers=headers)
        return {"ok": True, "status": r.status_code, "text": r.text if method.lower() != "head" else None, "headers": r.headers}
    except requests.exceptions.Timeout:
        return {"ok": False, "error": "timeout"}
    except requests.exceptions.RequestException as e:
        return {"ok": False, "error": str(e)}

# -------------------------
# Page fetch + parse
# -------------------------
def is_url_allowed(url):
    """
    Returns True if URL is not pointing to a private, loopback, localhost, or reserved IP.
    Blocks SSRF to internal infrastructure.
    """
    try:
        parts = urlparse(url)
        hostname = parts.hostname
        # Block empty hostname
        if not hostname:
            return False
        # Block localhost and common local domains
        blocked_hosts = {'localhost', '127.0.0.1', '::1', '0.0.0.0'}
        if hostname.lower() in blocked_hosts:
            return False
        # Try to resolve to IP
        ip = socket.gethostbyname(hostname)
        ip_obj = ipaddress.ip_address(ip)
        # Block private, loopback, link-local, reserved IPs
        if (
            ip_obj.is_private or
            ip_obj.is_loopback or
            ip_obj.is_link_local or
            ip_obj.is_reserved or
            ip_obj.is_multicast
        ):
            return False
        return True
    except Exception:
        # If unable to resolve/parse, block
        return False

def fetch_and_parse(url):
    """Fetch a URL and return (response_info, soup) where response_info is safe_get output."""
     if not is_url_allowed(url):
        return {"ok": False, "error": "URL points to a private, local, or blocked IP/domain."}, None
    info = safe_get(url, method="get")
    if not info.get("ok"):
        return info, None
    try:
        soup = BeautifulSoup(info["text"], "html.parser")
        return info, soup
    except Exception as e:
        return {"ok": False, "error": f"parsing error: {e}"}, None

# -------------------------
# On-page extraction
# -------------------------
def extract_basic_meta(soup, base_url):
    title = soup.title.get_text(strip=True) if soup.title else ""
    meta_desc_tag = soup.find("meta", attrs={"name": "description"})
    meta_desc = (meta_desc_tag.get("content") or "").strip() if meta_desc_tag else ""
    canonical_tag = soup.find("link", attrs={"rel": "canonical"})
    canonical = canonical_tag.get("href") if canonical_tag else ""
    robots_tag = soup.find("meta", attrs={"name": "robots"})
    robots = robots_tag.get("content") if robots_tag else ""
    viewport_tag = bool(soup.find("meta", attrs={"name": "viewport"}))
    # headings
    h1 = [h.get_text(strip=True) for h in soup.find_all("h1")]
    h2 = [h.get_text(strip=True) for h in soup.find_all("h2")]
    h3 = [h.get_text(strip=True) for h in soup.find_all("h3")]
    # paragraphs & word count
    paragraphs = [p.get_text(separator=" ", strip=True) for p in soup.find_all("p")]
    full_text = " ".join(paragraphs + h1 + h2 + h3)
    words = re.findall(r"\w+", full_text.lower())
    word_count = len(words)
    # images
    images = []
    for img in soup.find_all("img"):
        src = img.get("src") or img.get("data-src") or ""
        src = urljoin(base_url, src) if src else ""
        alt = (img.get("alt") or "").strip()
        images.append({"src": src, "alt": alt})
    # links classification
    links = []
    domain = urlparse(base_url).netloc
    for a in soup.find_all("a", href=True):
        href = urljoin(base_url, a["href"].strip())
        parsed = urlparse(href)
        if not parsed.scheme.startswith("http"):
            continue
        link_type = "internal" if parsed.netloc == domain else "external"
        links.append({"href": href, "type": link_type})
    # resources (scripts, css)
    scripts = [urljoin(base_url, s.get("src")) for s in soup.find_all("script", src=True)]
    stylesheets = [urljoin(base_url, l.get("href")) for l in soup.find_all("link", rel=lambda v: v and "stylesheet" in v)]
    return {
        "title": title,
        "meta_description": meta_desc,
        "canonical": canonical,
        "robots": robots,
        "viewport": viewport_tag,
        "h1": h1,
        "h2": h2,
        "h3": h3,
        "paragraphs": paragraphs,
        "word_count": word_count,
        "images": images,
        "links": links,
        "scripts": scripts,
        "stylesheets": stylesheets
    }

# -------------------------
# Keyword analysis
# -------------------------
def keyword_analysis(text, top_n=TOP_KEYWORDS):
    tokens = re.findall(r"\w+", text.lower())
    tokens = [t for t in tokens if t not in STOPWORDS and len(t) > 2]
    counts = Counter(tokens)
    total_words = len(re.findall(r"\w+", text))
    top = counts.most_common(top_n)
    density = []
    for k, c in top:
        density.append({"keyword": k, "count": c, "density_pct": round((c / total_words) * 100 if total_words else 0, 3)})
    return {"total_words": total_words, "top_keywords": top, "top_with_density": density}

# -------------------------
# Image audit
# -------------------------
def audit_images(images):
    """images: list of {'src','alt'}"""
    results = {"count": len(images), "missing_alt": 0, "missing_alt_percent": 0.0, "broken": [], "largest_by_bytes": None}
    sizes = []
    for img in images:
        alt = img.get("alt","").strip()
        if not alt:
            results["missing_alt"] += 1
        src = img.get("src")
        if not src:
            continue
        # head to get content-length
        info = safe_get(src, method="head")
        if info.get("ok") and info.get("headers"):
            cl = info["headers"].get("Content-Length")
            try:
                size = int(cl) if cl else None
            except Exception:
                size = None
        else:
            # fallback to GET with small timeout
            info2 = safe_get(src, method="get")
            if info2.get("ok") and info2.get("headers"):
                cl = info2["headers"].get("Content-Length")
                try:
                    size = int(cl) if cl else None
                except Exception:
                    size = None
            else:
                size = None
        sizes.append((src, size or 0))
        # check broken (status >=400)
        status_ok = True
        if info.get("ok"):
            status_ok = info["status"] < 400
        else:
            status_ok = False
        if not status_ok:
            results["broken"].append({"src": src, "status": info.get("status") or info.get("error")})
    results["missing_alt_percent"] = round((results["missing_alt"] / results["count"] * 100) if results["count"] else 0, 2)
    if sizes:
        largest = max(sizes, key=lambda t: t[1] or 0)
        results["largest_by_bytes"] = {"src": largest[0], "bytes": largest[1]}
    return results

# -------------------------
# Links audit + broken resources
# -------------------------
def classify_links(links):
    counts = Counter(l["type"] for l in links)
    by_type = defaultdict(list)
    for l in links:
        by_type[l["type"]].append(l["href"])
    return {"counts": counts, "by_type": dict(by_type)}

def check_broken_resources(resources, limit=200):
    broken = []
    checked = 0
    seen = set()
    for url in resources:
        if not url or url in seen:
            continue
        seen.add(url)
        if checked >= limit:
            break
        checked += 1
        info = safe_get(url, method="head")
        if not info.get("ok") or info.get("status", 0) >= 400 or info.get("status") == 405:
            # try GET fallback
            info2 = safe_get(url, method="get")
            if not info2.get("ok") or info2.get("status", 0) >= 400:
                broken.append({"url": url, "status": info2.get("status") or info2.get("error")})
    return broken

# -------------------------
# Performance insights
# -------------------------
def performance_insights(page_info, soup):
    # page_info from fetch_and_parse (headers)
    size_bytes = None
    if page_info.get("headers"):
        cl = page_info["headers"].get("Content-Length")
        try:
            size_bytes = int(cl) if cl else None
        except Exception:
            size_bytes = None
    resource_count = len(page_info.get("text") or "")  # simplistic fallback
    # count resources
    scripts = len(page_info.get("text") and soup.find_all("script") or [])
    images = len(soup.find_all("img"))
    css = len(soup.find_all("link", rel=lambda v: v and "stylesheet" in v))
    return {
        "page_bytes": size_bytes,
        "num_scripts": scripts,
        "num_images": images,
        "num_css": css
    }

# -------------------------
# Mobile friendliness (simple)
# -------------------------
def mobile_checks(soup):
    viewport = bool(soup.find("meta", {"name":"viewport"}))
    # naive font-size scan: look for inline styles with font-size < 12px
    small_fonts = 0
    for tag in soup.find_all(style=True):
        m = re.search(r"font-size\s*:\s*([0-9\.]+)px", tag["style"])
        if m:
            try:
                if float(m.group(1)) < 12.0:
                    small_fonts += 1
            except:
                pass
    tap_targets = len(soup.find_all("a"))  # crude
    recommendations = []
    if not viewport:
        recommendations.append("Add viewport meta tag for mobile responsiveness.")
    if small_fonts > 0:
        recommendations.append(f"Found {small_fonts} elements with font-size < 12px (inline). Consider larger fonts for mobile.")
    return {"viewport": viewport, "small_font_count": small_fonts, "tap_targets_estimate": tap_targets, "recommendations": recommendations}

# -------------------------
# Security checks
# -------------------------
def security_checks(url, soup):
    https_ok = urlparse(url).scheme == "https"
    mixed_content = False
    mixed_examples = []
    if https_ok:
        for tag in soup.find_all(["img","script","link"], src=True) + soup.find_all("link", href=True):
            # check attributes that might be http
            for attr in ("src","href"):
                val = tag.get(attr) or ""
                if val.startswith("http://"):
                    mixed_content = True
                    mixed_examples.append(val)
    return {"https": https_ok, "mixed_content": mixed_content, "mixed_examples": mixed_examples[:10]}

# -------------------------
# Sitemap & robots
# -------------------------
def fetch_robots_and_sitemaps(base_url):
    parsed = urlparse(base_url)
    root = f"{parsed.scheme}://{parsed.netloc}"
    robots_url = urljoin(root, "/robots.txt")
    robots = safe_get(robots_url, method="get")
    sitemap_urls = []
    if robots.get("ok") and robots.get("text"):
        text = robots["text"]
        for line in text.splitlines():
            if line.lower().startswith("sitemap:"):
                sitemap_urls.append(line.split(":",1)[1].strip())
    # if none, attempt common sitemap locations
    if not sitemap_urls:
        for candidate in ["/sitemap.xml", "/sitemap_index.xml"]:
            cand_url = urljoin(root, candidate)
            r = safe_get(cand_url, method="get")
            if r.get("ok") and r.get("text", "").strip().startswith("<?xml"):
                sitemap_urls.append(cand_url)
    # fetch and parse small sitemap (just get urls)
    sitemap_entries = []
    for s in sitemap_urls:
        r = safe_get(s, method="get")
        if r.get("ok") and r.get("text"):
            # naive extract <loc>
            locs = re.findall(r"<loc>(.*?)<\/loc>", r["text"], flags=re.I|re.S)
            sitemap_entries.extend(locs)
    return {"robots_text": robots.get("text") if robots.get("ok") else None, "sitemaps": sitemap_urls, "sitemap_entries": sitemap_entries[:500]}

# -------------------------
# On-page SEO scoring
# -------------------------
def compute_seo_score(meta, images_audit, links_summary, structure):
    """
    Weighted scoring (total 100)
    - Title (15): presence + ideal length 30-60 chars
    - Meta description (15): presence + ideal length 50-160
    - H1 presence (10)
    - H2/H3 structure (10)
    - Images alt (10)
    - Canonical tag (10)
    - Robots (5)
    - Links & internals (5)
    - Word count & content (10)
    - Mobile & security (10)
    """
    score = 0
    # Title
    title = meta.get("title","")
    if title:
        score += 10
        if 30 <= len(title) <= 60:
            score += 5
    # Meta description
    md = meta.get("meta_description","")
    if md:
        score += 8
        if 50 <= len(md) <= 160:
            score += 7
    # H1
    if meta.get("h1"):
        score += 10
    # H2/H3
    if meta.get("h2") or meta.get("h3"):
        score += 8
    # Images alt
    if images_audit["count"] > 0:
        alt_ok_ratio = 1 - (images_audit["missing_alt"] / images_audit["count"])
        score += round(10 * alt_ok_ratio)
    else:
        score += 6  # neutral if no images
    # Canonical
    if meta.get("canonical"):
        score += 10
    # Robots
    if meta.get("robots"):
        score += 5
    # Links: reward internal linking presence
    internal_count = len(links_summary["by_type"].get("internal", []))
    if internal_count > 0:
        score += 5
    # Word count: prefer >300 words
    wc = meta.get("word_count", 0)
    if wc >= 300:
        score += 10
    else:
        # partial credit
        score += round(10 * (wc / 300)) if wc>0 else 0
    # Mobile & security: small bonus
    mobile_security_bonus = 0
    if meta.get("viewport"):
        mobile_security_bonus += 5
    if meta.get("_security", {}).get("https"):
        mobile_security_bonus += 5
    score += mobile_security_bonus
    # clamp to 0-100
    score = max(0, min(100, int(score)))
    return score

# -------------------------
# AI recommendations (optional)
# -------------------------
def ai_recommendations(summary):
    """
    Try to call an AI text generator if available (services.openai_client or services.ai_client).
    This is optional — if not configured, function returns None.
    """
    try:
        # try new unified ai_client first
        from services.ai_client import generate_text
        prompt = (
            "You are an SEO advisor. Given the website summary below, "
            "provide 6 succinct, prioritized recommendations (bullet list) for improving SEO, "
            "title/meta, images, links and speed. Keep suggestions short.\n\n"
            f"Website summary:\n{json.dumps(summary, indent=2)[:3000]}"
        )
        out = generate_text(prompt, max_tokens=400)
        return out
    except Exception:
        try:
            from services.openai_client import generate_text
            prompt = (
                "You are an SEO advisor. Given the website summary below, "
                "provide 6 succinct, prioritized recommendations (bullet list) for improving SEO, "
                "title/meta, images, links and speed. Keep suggestions short.\n\n"
                f"Website summary:\n{json.dumps(summary, indent=2)[:3000]}"
            )
            out = generate_text(prompt, max_tokens=400)
            return out
        except Exception:
            return None

# -------------------------
# Streamlit UI: orchestrator
# -------------------------
def run_full_audit(url):
    # top-level runner: fetch page + parse
    page_info, soup = fetch_and_parse(url)
    if not page_info.get("ok"):
        st.error(f"Could not fetch page: {page_info.get('error')}")
        return

    base_url = url
    meta = extract_basic_meta(soup, base_url)
    # add security quick checks
    sec = security_checks(url, soup)
    meta["_security"] = sec

    # images audit
    images_a = audit_images(meta["images"])

    # links classification
    links_summary = classify_links(meta["links"])

    # performance
    perf = performance_insights(page_info, soup)

    # mobile
    mobile = mobile_checks(soup)

    # broken resources (images + scripts + css + links sample)
    resource_pool = [i["src"] for i in meta["images"] if i.get("src")] + meta["scripts"] + meta["stylesheets"] + list(links_summary["by_type"].get("external", [])[:100])
    broken_resources = check_broken_resources(resource_pool, limit=200)

    # sitemap + robots
    robots_smap = fetch_robots_and_sitemaps(base_url)

    # keyword analysis on combined page text
    combined_text = " ".join(meta.get("paragraphs", []) + meta.get("h1", []) + meta.get("h2", []) + meta.get("h3", []))
    keywords = keyword_analysis(combined_text)

    # structure
    structure = {
        "h1": meta.get("h1"),
        "h2": meta.get("h2"),
        "h3": meta.get("h3"),
        "paragraphs": len(meta.get("paragraphs", [])),
        "word_count": meta.get("word_count", 0)
    }

    # seo score
    seo_score = compute_seo_score(meta, images_a, links_summary, structure)

    # ai recommendations
    ai_reco = ai_recommendations({
        "title": meta.get("title"),
        "meta_description": meta.get("meta_description"),
        "seo_score": seo_score,
        "top_keywords": keywords.get("top_with_density"),
        "missing_image_alts_percent": images_a.get("missing_alt_percent"),
        "broken_resources_sample": broken_resources[:6],
        "sitemaps": robots_smap.get("sitemaps", [])
    })

    # Build final report dict
    report = {
        "url": url,
        "seo_score": seo_score,
        "meta": meta,
        "security": sec,
        "images": images_a,
        "links_summary": {"counts": links_summary["counts"], "samples": {k: links_summary["by_type"].get(k, [])[:10] for k in links_summary["by_type"]}},
        "performance": perf,
        "mobile": mobile,
        "broken_resources": broken_resources,
        "robots_and_sitemaps": robots_smap,
        "keywords": {"total_words": keywords["total_words"], "top_keywords": keywords["top_with_density"]},
        "structure": structure,
        "ai_recommendations": ai_reco
    }

    return report

# -------------------------
# Streamlit UI: display helpers
# -------------------------
def show_report_ui(report):
    st.header("SEO Summary")
    col1, col2 = st.columns([1, 3])
    with col1:
        st.metric("SEO Score", f"{report['seo_score']}/100")
        st.write("Top keyword(s):")
        top = report["keywords"]["top_keywords"][:5]
        for k in top:
            st.write(f"- {k['keyword']} ({k['count']}, {k['density_pct']}%)")
    with col2:
        st.subheader("Title & Meta")
        st.markdown(f"**Title:** {report['meta'].get('title','—')}")
        st.markdown(f"**Meta Description:** {report['meta'].get('meta_description','—')}")
        st.markdown(f"**Canonical:** {report['meta'].get('canonical','—')}")
        st.markdown(f"**Robots:** {report['meta'].get('robots','—')}")
    st.divider()

    st.subheader("Structure")
    st.write(f"H1s: {len(report['meta'].get('h1',[]))}  •  H2s: {len(report['meta'].get('h2',[]))}  •  H3s: {len(report['meta'].get('h3',[]))}")
    st.write(f"Paragraphs: {len(report['meta'].get('paragraphs',[]))}  •  Word count: {report['meta'].get('word_count',0)}")

    st.subheader("Images")
    st.write(f"Total images: {report['images']['count']} • Missing ALT: {report['images']['missing_alt']} ({report['images']['missing_alt_percent']}%)")
    if report['images']['largest_by_bytes']:
        st.write(f"Largest image (approx): {report['images']['largest_by_bytes']['bytes']} bytes")
        st.write(report['images']['largest_by_bytes']['src'])
    if report['images']['broken']:
        st.warning(f"{len(report['images']['broken'])} broken images found (sample):")
        st.dataframe(report['images']['broken'][:10])

    st.subheader("Links")
    counts = report['links_summary']['counts']
    st.write(f"Internal: {counts.get('internal',0)}  •  External: {counts.get('external',0)}")
    # chart: counts
    try:
        import pandas as pd
        df = pd.DataFrame.from_dict(counts, orient="index", columns=["count"])
        st.bar_chart(df)
    except Exception:
        pass

    st.subheader("Performance")
    perf = report['performance']
    st.write(f"Page size (bytes): {perf.get('page_bytes') or 'Unknown'}")
    st.write(f"Scripts: {perf.get('num_scripts')}, CSS files: {perf.get('num_css')}, Images: {perf.get('num_images')}")

    st.subheader("Mobile & Security")
    st.write(f"Viewport tag present: {report['mobile']['viewport']}")
    if report['mobile']['recommendations']:
        st.info("Mobile recommendations:")
        for r in report['mobile']['recommendations']:
            st.write(f"- {r}")
    st.write(f"HTTPS: {report['security']['https']}")
    if report['security']['mixed_content']:
        st.warning("Mixed content found (sample):")
        for m in report['security']['mixed_examples']:
            st.write(f"- {m}")

    st.subheader("Sitemap & Robots")
    st.write("Sitemaps discovered:", report['robots_and_sitemaps']['sitemaps'])
    if report['robots_and_sitemaps']['sitemap_entries']:
        st.write(f"Found {len(report['robots_and_sitemaps']['sitemap_entries'])} sitemap URLs (sample):")
        st.dataframe(report['robots_and_sitemaps']['sitemap_entries'][:20])

    st.subheader("Broken Resources (sample)")
    if report['broken_resources']:
        st.dataframe(report['broken_resources'][:50])
    else:
        st.success("No broken resources found in the checked sample.")

    st.subheader("Top Keywords")
    st.table(report['keywords']['top_keywords'][:TOP_KEYWORDS])

    st.subheader("Google SERP Preview")
    url = report['url']
    title = report['meta'].get('title') or "(no title)"
    meta_desc = report['meta'].get('meta_description') or "(no description)"
    st.markdown(f"**{title}**")
    st.caption(url)
    st.write(meta_desc)

    if report.get("ai_recommendations"):
        st.subheader("AI Recommendations")
        st.markdown(report["ai_recommendations"])

# -------------------------
# Public Streamlit wrapper
# -------------------------
def show_seo_audit():
    st.title("SEO Audit — Deep Site Health & Recommendations")
    url = st.text_input("Enter full page URL (include https://)", placeholder="https://example.com/page")
    run_button = st.button("Run full audit")
    if run_button:
        if not url or not urlparse(url).scheme.startswith("http"):
            st.error("Please enter a valid URL including http/https.")
            return
        with st.spinner("Running full SEO audit (this may take 10–30s)..."):
            start = time.time()
            report = run_full_audit(url)
            if not report:
                st.error("Failed to produce report.")
                return
            show_report_ui(report)
            st.success(f"Audit completed in {int(time.time()-start)}s")

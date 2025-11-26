# tools/seo/seo_audit.py
"""
Safe SEO auditor for Brand N Bloom — Option B (Smart Public Domain Only)

Key protections:
 - Blocks localhost / private / link-local / reserved / multicast IPs
 - Resolves hostnames and validates every resolved IP
 - Optional explicit allowlist via SEO_ALLOWED_DOMAINS env var
 - Safe requests with timeouts and user-agent
 - Streamlit UI with optional JWT gating (uses utils.jwt_helper.decode_access_token if present)
"""

from typing import Tuple, Optional, Dict, Any, List, Set
from urllib.parse import urlparse, urljoin
from collections import Counter, defaultdict
import socket
import ipaddress
import requests
from bs4 import BeautifulSoup
import re
import json
import time
import streamlit as st
import os

# Optional JWT helper integration
try:
    from utils.jwt_helper import decode_access_token  # your project's jwt helper
except Exception:
    def decode_access_token(token: str):
        return None  # fallback stub; treat as unauthenticated in UI

USER_AGENT = {"User-Agent": "BrandnBloomBot/1.2 (+https://brandnbloom.ai)"}
REQUEST_TIMEOUT = int(os.getenv("SEO_REQUEST_TIMEOUT", "10"))
TOP_KEYWORDS = 15

# Optional explicit domains allowlist (comma-separated env var)
# If set, audits will be limited to these domains (useful for highly restrictive deployments).
_ALLOWED_DOMAINS_ENV = os.getenv("SEO_ALLOWED_DOMAINS", "").strip()
ALLOWED_DOMAINS: Set[str] = set()
if _ALLOWED_DOMAINS_ENV:
    ALLOWED_DOMAINS = {d.strip().lower() for d in _ALLOWED_DOMAINS_ENV.split(",") if d.strip()}

# Basic stopwords (small set)
STOPWORDS = {
    "the", "and", "a", "an", "in", "on", "for", "with", "to", "of", "is", "it",
    "this", "that", "by", "are", "as", "be", "or", "from", "at", "was", "were",
    "has", "have", "but", "not", "your", "you", "we", "our", "they", "their",
    "can", "will", "if", "so", "do", "does", "did", "about", "which"
}


# -------------------------
# Hostname / IP safety helpers (Option B)
# -------------------------
def _resolve_ips_for_hostname(hostname: str) -> List[str]:
    """Return list of resolved IP strings for a hostname. Raises on resolution failure."""
    results = socket.getaddrinfo(hostname, None)
    ips = []
    for r in results:
        try:
            ip = r[-1][0]
            ips.append(ip)
        except Exception:
            continue
    return sorted(set(ips))


def _ip_is_public(ip_str: str) -> bool:
    """Return True if the IP is public (not private / loopback / link-local / reserved / multicast)."""
    try:
        ip_obj = ipaddress.ip_address(ip_str)
    except Exception:
        return False
    if ip_obj.is_private or ip_obj.is_loopback or ip_obj.is_link_local or ip_obj.is_reserved or ip_obj.is_multicast:
        return False
    return True


def is_hostname_allowed(hostname: str) -> bool:
    """
    Decide whether a hostname is allowed for auditing.

    Rules:
      - If ALLOWED_DOMAINS env var is set, the hostname must be an exact match or a subdomain of an allowed domain.
      - Otherwise, resolve hostname and ensure EVERY resolved IP is public (not private/reserved).
    """
    if not hostname:
        return False

    hostname = hostname.lower().strip()

    # If explicit allowlist present, only permit those domains (and their subdomains)
    if ALLOWED_DOMAINS:
        for allowed in ALLOWED_DOMAINS:
            if hostname == allowed or hostname.endswith("." + allowed):
                return True
        return False

    # Otherwise, resolve and verify all IPs are public
    try:
        ips = _resolve_ips_for_hostname(hostname)
        if not ips:
            return False
        for ip in ips:
            if not _ip_is_public(ip):
                return False
        return True
    except Exception:
        # If resolution fails, block by default
        return False


def is_url_allowed(url: str) -> bool:
    """
    Quick check for a URL string:
      - Must have http or https scheme
      - Hostname must be allowed via is_hostname_allowed
    """
    try:
        parsed = urlparse(url)
        if parsed.scheme not in ("http", "https"):
            return False
        hostname = parsed.hostname
        if not hostname:
            return False
        return is_hostname_allowed(hostname)
    except Exception:
        return False


# -------------------------
# Safe requests wrapper
# -------------------------
def safe_get(url: str, method: str = "get", timeout: int = REQUEST_TIMEOUT,
             allow_redirects: bool = True, headers: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
    """
    Perform GET or HEAD safely with SSRF protections.
    Returns a dict: { ok: bool, status: int|None, text: str|None, headers: dict|None, error: str|None }
    """
    headers = headers or USER_AGENT
    try:
        parsed = urlparse(url)
        if parsed.scheme not in ("http", "https"):
            return {"ok": False, "error": "Unsupported URL scheme"}

        hostname = parsed.hostname
        if not hostname:
            return {"ok": False, "error": "Invalid URL"}

        # Hostname must be authorized
        if not is_hostname_allowed(hostname):
  return {"ok": False, "error": f"Domain '{hostname}' is not allowed for audit. Only explicit allowlisted domains are permitted."}
        # Resolve and check each IP (extra safety)
        try:
            ips = _resolve_ips_for_hostname(hostname)
            for ip in ips:
                if not _ip_is_public(ip):
                    return {"ok": False, "error": f"Resolved IP {ip} for {hostname} is not allowed"}
        except Exception:
            return {"ok": False, "error": f"Could not resolve hostname {hostname}"}

        # Make the request
        if method.lower() == "head":
            resp = requests.head(url, timeout=timeout, allow_redirects=allow_redirects, headers=headers)
            text = None
        else:
            resp = requests.get(url, timeout=timeout, allow_redirects=allow_redirects, headers=headers)
            text = resp.text

        return {"ok": True, "status": resp.status_code, "text": text, "headers": resp.headers}
    except requests.exceptions.Timeout:
        return {"ok": False, "error": "timeout"}
    except requests.exceptions.RequestException as e:
        return {"ok": False, "error": str(e)}
    except Exception as e:
        return {"ok": False, "error": str(e)}


# -------------------------
# Page fetch + parse
# -------------------------
def fetch_and_parse(url: str) -> Tuple[Dict[str, Any], Optional[BeautifulSoup]]:
    """Fetch a URL and return (response_info, soup) where response_info is safe_get output."""
    if not is_url_allowed(url):
        return {"ok": False, "error": "URL not allowed (private/reserved or disallowed domain)"}, None

    info = safe_get(url, method="get")
    if not info.get("ok"):
        return info, None

    try:
        soup = BeautifulSoup(info["text"], "html.parser")
        return info, soup
    except Exception as e:
        return {"ok": False, "error": f"parsing error: {e}"}, None


# -------------------------
# On-page extraction & audits
# -------------------------
def extract_basic_meta(soup: BeautifulSoup, base_url: str) -> Dict[str, Any]:
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
    base_domain = urlparse(base_url).netloc
    for img in soup.find_all("img"):
        src = img.get("src") or img.get("data-src") or ""
        src = urljoin(base_url, src) if src else ""
        alt = (img.get("alt") or "").strip()
        images.append({"src": src, "alt": alt})
    # links classification
    links = []
    for a in soup.find_all("a", href=True):
        try:
            href = urljoin(base_url, a["href"].strip())
        except Exception:
            continue
        parsed = urlparse(href)
        if not parsed.scheme.startswith("http"):
            continue
        link_type = "internal" if parsed.netloc == base_domain else "external"
        links.append({"href": href, "type": link_type})
    # resources
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


def keyword_analysis(text: str, top_n: int = TOP_KEYWORDS) -> Dict[str, Any]:
    tokens = re.findall(r"\w+", text.lower())
    tokens = [t for t in tokens if t not in STOPWORDS and len(t) > 2]
    counts = Counter(tokens)
    total_words = len(re.findall(r"\w+", text))
    top = counts.most_common(top_n)
    density = []
    for k, c in top:
        density.append({"keyword": k, "count": c, "density_pct": round((c / total_words) * 100 if total_words else 0, 3)})
    return {"total_words": total_words, "top_keywords": [{"keyword": k, "count": c} for k, c in top], "top_with_density": density}


def audit_images(images: List[Dict[str, str]]) -> Dict[str, Any]:
    results = {"count": len(images), "missing_alt": 0, "missing_alt_percent": 0.0, "broken": [], "largest_by_bytes": None}
    sizes = []
    for img in images:
        alt = img.get("alt", "").strip()
        if not alt:
            results["missing_alt"] += 1
        src = img.get("src")
        if not src:
            continue
        info = safe_get(src, method="head")
        size = None
        if info.get("ok") and info.get("headers"):
            cl = info["headers"].get("Content-Length")
            try:
                size = int(cl) if cl else None
            except Exception:
                size = None
        else:
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
        status_ok = info.get("ok") and info.get("status", 0) < 400
        if not status_ok:
            results["broken"].append({"src": src, "status": info.get("status") or info.get("error")})
    results["missing_alt_percent"] = round((results["missing_alt"] / results["count"] * 100) if results["count"] else 0, 2)
    if sizes:
        largest = max(sizes, key=lambda t: t[1] or 0)
        results["largest_by_bytes"] = {"src": largest[0], "bytes": largest[1]}
    return results


def classify_links(links: List[Dict[str, str]]) -> Dict[str, Any]:
    counts = Counter(l["type"] for l in links)
    by_type = defaultdict(list)
    for l in links:
        by_type[l["type"]].append(l["href"])
    return {"counts": counts, "by_type": dict(by_type)}


def check_broken_resources(resources: List[str], limit: int = 200) -> List[Dict[str, Any]]:
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
            info2 = safe_get(url, method="get")
            if not info2.get("ok") or info2.get("status", 0) >= 400:
                broken.append({"url": url, "status": info2.get("status") or info2.get("error")})
    return broken


def performance_insights(page_info: Dict[str, Any], soup: BeautifulSoup) -> Dict[str, Any]:
    size_bytes = None
    if page_info.get("headers"):
        cl = page_info["headers"].get("Content-Length")
        try:
            size_bytes = int(cl) if cl else None
        except Exception:
            size_bytes = None
    scripts = len(soup.find_all("script")) if page_info.get("text") else 0
    images = len(soup.find_all("img"))
    css = len(soup.find_all("link", rel=lambda v: v and "stylesheet" in v))
    return {"page_bytes": size_bytes, "num_scripts": scripts, "num_images": images, "num_css": css}


def mobile_checks(soup: BeautifulSoup) -> Dict[str, Any]:
    viewport = bool(soup.find("meta", {"name": "viewport"}))
    small_fonts = 0
    for tag in soup.find_all(style=True):
        m = re.search(r"font-size\s*:\s*([0-9\.]+)px", tag["style"])
        if m:
            try:
                if float(m.group(1)) < 12.0:
                    small_fonts += 1
            except Exception:
                pass
    tap_targets = len(soup.find_all("a"))
    recommendations = []
    if not viewport:
        recommendations.append("Add viewport meta tag for mobile responsiveness.")
    if small_fonts > 0:
        recommendations.append(f"Found {small_fonts} elements with font-size < 12px (inline). Consider larger fonts for mobile.")
    return {"viewport": viewport, "small_font_count": small_fonts, "tap_targets_estimate": tap_targets, "recommendations": recommendations}


def security_checks(url: str, soup: BeautifulSoup) -> Dict[str, Any]:
    https_ok = urlparse(url).scheme == "https"
    mixed_content = False
    mixed_examples = []
    if https_ok:
        for tag in soup.find_all(["img", "script", "link"]):
            for attr in ("src", "href"):
                val = tag.get(attr) or ""
                if val.startswith("http://"):
                    mixed_content = True
                    mixed_examples.append(val)
    return {"https": https_ok, "mixed_content": mixed_content, "mixed_examples": mixed_examples[:10]}


def fetch_robots_and_sitemaps(base_url: str) -> Dict[str, Any]:
    parsed = urlparse(base_url)
    root = f"{parsed.scheme}://{parsed.netloc}"
    robots_url = urljoin(root, "/robots.txt")
    robots = safe_get(robots_url, method="get")
    sitemap_urls: List[str] = []
    if robots.get("ok") and robots.get("text"):
        text = robots["text"]
        for line in text.splitlines():
            if line.lower().startswith("sitemap:"):
                sitemap_urls.append(line.split(":", 1)[1].strip())
    if not sitemap_urls:
        for candidate in ["/sitemap.xml", "/sitemap_index.xml"]:
            cand_url = urljoin(root, candidate)
            r = safe_get(cand_url, method="get")
            if r.get("ok") and r.get("text", "").strip().startswith("<?xml"):
                sitemap_urls.append(cand_url)
    sitemap_entries: List[str] = []
    for s in sitemap_urls:
        r = safe_get(s, method="get")
        if r.get("ok") and r.get("text"):
            locs = re.findall(r"<loc>(.*?)<\/loc>", r["text"], flags=re.I | re.S)
            sitemap_entries.extend(locs)
    return {"robots_text": robots.get("text") if robots.get("ok") else None, "sitemaps": sitemap_urls, "sitemap_entries": sitemap_entries[:500]}


def compute_seo_score(meta: Dict[str, Any], images_audit: Dict[str, Any], links_summary: Dict[str, Any], structure: Dict[str, Any]) -> int:
    score = 0
    title = meta.get("title", "")
    if title:
        score += 10
        if 30 <= len(title) <= 60:
            score += 5
    md = meta.get("meta_description", "")
    if md:
        score += 8
        if 50 <= len(md) <= 160:
            score += 7
    if meta.get("h1"):
        score += 10
    if meta.get("h2") or meta.get("h3"):
        score += 8
    if images_audit["count"] > 0:
        alt_ok_ratio = 1 - (images_audit["missing_alt"] / images_audit["count"])
        score += round(10 * alt_ok_ratio)
    else:
        score += 6
    if meta.get("canonical"):
        score += 10
    if meta.get("robots"):
        score += 5
    internal_count = len(links_summary["by_type"].get("internal", []))
    if internal_count > 0:
        score += 5
    wc = meta.get("word_count", 0)
    if wc >= 300:
        score += 10
    else:
        score += round(10 * (wc / 300)) if wc > 0 else 0
    mobile_security_bonus = 0
    if meta.get("viewport"):
        mobile_security_bonus += 5
    if meta.get("_security", {}).get("https"):
        mobile_security_bonus += 5
    score += mobile_security_bonus
    score = max(0, min(100, int(score)))
    return score


def ai_recommendations(summary: Dict[str, Any]) -> Optional[str]:
    try:
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


def run_full_audit(url: str) -> Optional[Dict[str, Any]]:
    page_info, soup = fetch_and_parse(url)
    if not page_info.get("ok"):
        st.error(f"Could not fetch page: {page_info.get('error')}")
        return None

    base_url = url
    meta = extract_basic_meta(soup, base_url)
    sec = security_checks(url, soup)
    meta["_security"] = sec

    images_a = audit_images(meta["images"])
    links_summary = classify_links(meta["links"])
    perf = performance_insights(page_info, soup)
    mobile = mobile_checks(soup)

    resource_pool = [i["src"] for i in meta["images"] if i.get("src")] + meta["scripts"] + meta["stylesheets"] + list(links_summary["by_type"].get("external", [])[:100])
    broken_resources = check_broken_resources(resource_pool, limit=200)

    robots_smap = fetch_robots_and_sitemaps(base_url)
    combined_text = " ".join(meta.get("paragraphs", []) + meta.get("h1", []) + meta.get("h2", []) + meta.get("h3", []))
    keywords = keyword_analysis(combined_text)

    structure = {
        "h1": meta.get("h1"),
        "h2": meta.get("h2"),
        "h3": meta.get("h3"),
        "paragraphs": len(meta.get("paragraphs", [])),
        "word_count": meta.get("word_count", 0)
    }

    seo_score = compute_seo_score(meta, images_a, links_summary, structure)

    ai_reco = ai_recommendations({
        "title": meta.get("title"),
        "meta_description": meta.get("meta_description"),
        "seo_score": seo_score,
        "top_keywords": keywords.get("top_with_density"),
        "missing_image_alts_percent": images_a.get("missing_alt_percent"),
        "broken_resources_sample": broken_resources[:6],
        "sitemaps": robots_smap.get("sitemaps", [])
    })

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


def show_report_ui(report: Dict[str, Any]) -> None:
    st.header("SEO Summary")
    col1, col2 = st.columns([1, 3])
    with col1:
        st.metric("SEO Score", f"{report['seo_score']}/100")
        st.write("Top keyword(s):")
        top = report["keywords"]["top_keywords"][:5]
        for k in top:
            st.write(f"- {k['keyword']} ({k['count']})")
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
    try:
        import pandas as pd
        df = pd.DataFrame.from_dict(dict(counts), orient="index", columns=["count"])
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


def verify_jwt(token: str) -> Optional[Dict[str, Any]]:
    """Wrapper that safely decodes JWT using project's helper (if present)."""
    if not token:
        return None
    try:
        return decode_access_token(token)
    except Exception:
        return None


def show_seo_audit() -> None:
    """
    Streamlit UI wrapper for the SEO auditor.
    This UI optionally requires a JWT (if you want to gate usage).
    """
    st.title("SEO Audit — Deep Site Health & Recommendations")
    st.markdown("This audit uses a restricted-mode network policy: only public domains are allowed. Local or private networks are blocked.")

    # Optional token gate
    token = st.text_input("Access token (JWT) — optional", type="password")
    if token:
        payload = verify_jwt(token)
        if not payload:
            st.error("Invalid or expired token.")
            return
        st.success("Token validated.")

    url = st.text_input("Enter full page URL (include https://)", placeholder="https://example.com/page")
   if not ALLOWED_DOMAINS:
        st.warning("⚠️ No domains are authorized for audit. Set the SEO_ALLOWED_DOMAINS environment variable (comma-separated) to enable safe SEO audits for specified domains only.")
    run_button = st.button("Run full audit", disabled=not ALLOWED_DOMAINS)    if run_button:
        if not url or not urlparse(url).scheme.startswith("http"):
            st.error("Please enter a valid URL including http/https.")
            return

        # Final hostname check (and explicit allowed-domain check message)
        hostname = urlparse(url).hostname or ""
        if not is_hostname_allowed(hostname):
            if ALLOWED_DOMAINS:
                st.error("Domain not permitted. Allowed domains: " + ", ".join(sorted(ALLOWED_DOMAINS)))
            else:
    st.error("No allowlisted domains configured. Please set the SEO_ALLOWED_DOMAINS environment variable (comma-separated hostnames/domains) to permit audits for those sites.")            return

        with st.spinner("Running full SEO audit (this may take 10–30s)..."):
            start = time.time()
            report = run_full_audit(url)
            if not report:
                st.error("Failed to produce report.")
                return
            show_report_ui(report)
            st.success(f"Audit completed in {int(time.time() - start)}s")

# Playwright scraper with proxy rotation and session reuse (scaffold).
import os, random, re, json, time
from playwright.sync_api import sync_playwright, TimeoutError as PWTimeout
from bs4 import BeautifulSoup

PROXY_FILE = os.environ.get('PROXY_LIST_FILE', 'proxies.txt')
STORAGE_STATE = os.environ.get('STORAGE_STATE_PATH', 'scraper/storage_state.json')

USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 17_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1',
]

def _load_proxies():
    try:
        with open(PROXY_FILE) as f:
            return [l.strip() for l in f if l.strip() and not l.strip().startswith('#')]
    except FileNotFoundError:
        return []

def _choose_proxy():
    proxies = _load_proxies()
    return random.choice(proxies) if proxies else None

def _extract_json(html):
    m = re.search(r'window\._sharedData = (\{.*?\});', html, re.S)
    if m:
        try:
            return json.loads(m.group(1))
        except:
            pass
    soup = BeautifulSoup(html, 'html.parser')
    tag = soup.find('script', {'type':'application/ld+json'})
    if tag and tag.string:
        try:
            return json.loads(tag.string)
        except:
            pass
    return None

def fetch_profile_and_posts(handle, limit=20, tries=3, headless=True):
    last_exc = None
    for attempt in range(tries):
        proxy = _choose_proxy()
        ua = random.choice(USER_AGENTS)
        try:
            with sync_playwright() as p:
                launch_kwargs = {'headless': headless}
                if proxy:
                    launch_kwargs['proxy'] = {'server': proxy}
                browser = p.chromium.launch(**launch_kwargs)
                context_kwargs = {}
                if os.path.exists(STORAGE_STATE):
                    context_kwargs['storage_state'] = STORAGE_STATE
                context = browser.new_context(**context_kwargs, user_agent=ua)
                page = context.new_page()
                url = f'https://www.instagram.com/{handle}/'
                page.goto(url, timeout=30000)
                page.wait_for_timeout(1500)
                html = page.content()
                data = _extract_json(html)
                profile = {}
                posts = []
                if data and 'entry_data' in data:
                    try:
                        user = data['entry_data']['ProfilePage'][0]['graphql']['user']
                        profile = {
                            'id': user.get('id'),
                            'username': user.get('username'),
                            'full_name': user.get('full_name'),
                            'biography': user.get('biography'),
                            'followers': user.get('edge_followed_by', {}).get('count', 0),
                            'following': user.get('edge_follow', {}).get('count', 0),
                            'posts_count': user.get('edge_owner_to_timeline_media', {}).get('count', 0),
                            'profile_pic_url': user.get('profile_pic_url_hd') or user.get('profile_pic_url')
                        }
                        edges = user.get('edge_owner_to_timeline_media', {}).get('edges', [])[:limit]
                        for e in edges:
                            n = e.get('node', {})
                            posts.append({
                                'id': n.get('id'),
                                'shortcode': n.get('shortcode'),
                                'timestamp': n.get('taken_at_timestamp'),
                                'likes': n.get('edge_liked_by', {}).get('count', 0),
                                'comments': n.get('edge_media_to_comment', {}).get('count', 0),
                                'caption': (n.get('edge_media_to_caption', {}).get('edges') or [{}])[0].get('node', {}).get('text',''),
                                'display_url': n.get('display_url'),
                            })
                    except Exception:
                        pass
                else:
                    soup = BeautifulSoup(html, 'html.parser')
                    metas = {m.get('property') or m.get('name'): m.get('content') for m in soup.find_all('meta') if (m.get('property') or m.get('name')) and m.get('content')}
                    profile = {'username': handle, 'meta': metas}
                context.close()
                browser.close()
                return profile, posts
        except PWTimeout as e:
            last_exc = e
            time.sleep(2**attempt)
            continue
        except Exception as e:
            last_exc = e
            time.sleep(2**attempt)
            continue
    raise last_exc or RuntimeError('scrape failed')

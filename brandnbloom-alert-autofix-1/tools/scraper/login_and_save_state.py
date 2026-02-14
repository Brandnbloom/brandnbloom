# Run this once to manually log in to Instagram and save storage state (cookies/session).
from playwright.sync_api import sync_playwright
import os

OUT = os.environ.get('STORAGE_STATE_PATH', 'scraper/storage_state.json')

def login_and_save_state(login_url='https://www.instagram.com/accounts/login/'):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        page.goto(login_url)
        print('Please log in in the opened browser window. After logging in, press Enter to save state.')
        input('Press Enter after logging in...')
        os.makedirs(os.path.dirname(OUT), exist_ok=True)
        context.storage_state(path=OUT)
        print('Saved storage state to', OUT)
        browser.close()

if __name__ == '__main__':
    login_and_save_state()

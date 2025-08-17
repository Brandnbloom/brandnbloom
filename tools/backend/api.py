from flask import Flask, request, jsonify
from scraper.playwright_scraper import fetch_profile_and_posts
from backend.crud import upsert_account, insert_posts
from backend.db import create_tables
import os

app = Flask(__name__)
create_tables()

@app.route('/scrape', methods=['POST'])
def scrape():
    data = request.json or {}
    handle = data.get('handle')
    limit = data.get('limit', 20)
    if not handle:
        return jsonify({'error':'handle required'}), 400
    try:
        profile, posts = fetch_profile_and_posts(handle, limit=limit)
        acc_id = upsert_account(handle, profile)
        if posts:
            insert_posts(acc_id, posts)
        return jsonify({'profile': profile, 'posts_count': len(posts)})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health')
def health():
    return jsonify({'status':'ok'})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    app.run(host='0.0.0.0', port=port)

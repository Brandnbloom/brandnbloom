import streamlit as st
from backend.db import SessionLocal
from backend.db import Account, Post
import pandas as pd
st.set_page_config(layout='wide', page_title='BloomInsight Live')

st.title('BloomInsight — Live (Playwright Scraper)')

with st.sidebar:
    st.header('Controls')
    handle = st.text_input('Instagram handle (no @)', value='natgeo')
    if st.button('Refresh now'):
        import requests, os
        url = os.environ.get('BACKEND_SCRAPE_URL', 'http://localhost:8000/scrape')
        r = requests.post(url, json={'handle':handle,'limit':25}, timeout=120)
        st.write(r.json())

db = SessionLocal()
acc = db.query(Account).filter(Account.handle==handle).first() if handle else None
if acc:
    st.metric('Followers', acc.followers or 0)
    st.metric('Last Pull', acc.last_pull)
    posts = db.query(Post).filter(Post.account_id==acc.id).order_by(Post.timestamp.desc()).limit(30).all()
    if posts:
        df = pd.DataFrame([{'timestamp':p.timestamp, 'caption': p.caption[:120] if p.caption else '', 'likes':p.like_count, 'comments':p.comment_count} for p in posts])
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        st.dataframe(df)
        st.line_chart(df.set_index('timestamp')[['likes','comments']])
else:
    st.info('No data yet — press Refresh now after the backend runs and you logged in via Playwright.')
db.close()

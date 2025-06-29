import streamlit as st
import pandas as pd
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
import os

SCOPES = ['https://www.googleapis.com/auth/webmasters.readonly']

def get_service():
    flow = InstalledAppFlow.from_client_secrets_file("client_secret.json", SCOPES)
    creds = flow.run_local_server(port=0)
    service = build('searchconsole', 'v1', credentials=creds)
    return service

def fetch_search_analytics(service, site_url):
    request = {
        'startDate': '2024-06-01',
        'endDate': '2024-06-30',
        'dimensions': ['query'],
        'rowLimit': 10
    }
    response = service.searchanalytics().query(siteUrl=site_url, body=request).execute()
    return response.get('rows', [])

st.title("🔎 Google Search Console Dashboard")
st.write("Track your website’s SEO performance with real data from Google.")

site_url = st.text_input("Enter your verified site URL:", "https://brand-n-bloom.com")

if st.button("Connect & Fetch Data"):
    service = get_service()
    data = fetch_search_analytics(service, site_url)
    
    if data:
        df = pd.DataFrame(data)
        df[['query', 'clicks', 'impressions', 'ctr', 'position']] = pd.DataFrame(df['keys'].tolist())
        st.dataframe(df[['query', 'clicks', 'impressions']])
    else:
        st.warning("No data found or site not verified.")

import streamlit as st
import pandas as pd
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
import os

SCOPES = ['https://www.googleapis.com/auth/webmasters.readonly']

def get_service():
    try:
        flow = InstalledAppFlow.from_client_secrets_file("client_secret.json", SCOPES)
        creds = flow.run_local_server(port=0)
        service = build('searchconsole', 'v1', credentials=creds)
        return service
    except FileNotFoundError:
        st.error("❌ Missing client_secret.json file. Please upload it to proceed.")
        return None

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
    if service:
        data = fetch_search_analytics(service, site_url)
        
        if data:
            df = pd.DataFrame([
                {
                    "query": row["keys"][0],
                    "clicks": row.get("clicks", 0),
                    "impressions": row.get("impressions", 0),
                    "ctr": row.get("ctr", 0),
                    "position": row.get("position", 0)
                }
                for row in data
            ])
            st.dataframe(df)
        else:
            st.warning("No data found or site not verified.")

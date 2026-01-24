import pandas as pd
import os
import requests
from dotenv import load_dotenv

load_dotenv()

CUSTOMER_API_URL = os.getenv("CUSTOMER_API_URL")  # e.g., your CRM endpoint
CUSTOMER_API_KEY = os.getenv("CUSTOMER_API_KEY")  # API key for auth

def get_customer_data(limit: int = 1000) -> pd.DataFrame:
    """
    Fetch real customer transactional data from CRM/API.
    Returns a pandas DataFrame with:
    - CustomerID, LastPurchaseDate, TotalSpent, NumberOfPurchases, ChurnFlag (if available)
    """
    try:
        headers = {"Authorization": f"Bearer {CUSTOMER_API_KEY}"}
        params = {"limit": limit}
        response = requests.get(CUSTOMER_API_URL, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()

        # Convert to DataFrame
        df = pd.DataFrame(data)
        # Ensure key columns exist
        for col in ["CustomerID", "LastPurchaseDate", "TotalSpent", "NumberOfPurchases"]:
            if col not in df.columns:
                df[col] = 0
        return df

    except Exception as e:
        print(f"Error fetching customer data: {e}")
        return pd.DataFrame()

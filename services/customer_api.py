import pandas as pd

def get_customer_data():
    return pd.DataFrame({
        "customer_id": [1,2,3],
        "orders": [5,2,8],
        "revenue": [1200, 400, 3200],
        "last_purchase_days": [30, 180, 15]
    })

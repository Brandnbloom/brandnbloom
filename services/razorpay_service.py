import razorpay
import pandas as pd
import os
from datetime import datetime

client = razorpay.Client(
    auth=(
        os.getenv("RAZORPAY_KEY_ID"),
        os.getenv("RAZORPAY_SECRET")
    )
)

def get_razorpay_customers():

    payments = client.payment.all({"count": 100})

    rows = []

    for p in payments["items"]:

        email = p.get("email")
        amount = p["amount"] / 100
        created = datetime.fromtimestamp(p["created_at"])

        rows.append({
            "email": email,
            "amount": amount,
            "last_purchase": created
        })

    df = pd.DataFrame(rows)

    if df.empty:
        return pd.DataFrame(columns=[
            "email",
            "total_spent",
            "num_purchases",
            "last_purchase"
        ])

    final = df.groupby("email").agg(
        total_spent=("amount", "sum"),
        num_purchases=("amount", "count"),
        last_purchase=("last_purchase", "max")
    ).reset_index()

    return final

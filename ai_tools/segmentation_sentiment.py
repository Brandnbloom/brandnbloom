from services.customer_api import get_customer_data
from services.instagram_api import get_posts

def run():
    df_customers = get_customer_data()
    social_df = get_posts("brand")

    # RFM + Sentiment logic here

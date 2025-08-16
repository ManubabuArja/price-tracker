# core/tracker.py

from etl.amazon import get_amazon_price
from etl.flipkart import get_flipkart_price
from notify.emailer import send_drop_alert
import pandas as pd
import os

DATA_FILE = os.path.join("data", "warehouse.xlsx")

def check_price_drops():
    """Check for price drops and send alerts"""
    if not os.path.exists(DATA_FILE):
        return

    df = pd.read_excel(DATA_FILE)

    for index, row in df.iterrows():
        url = row["url"]
        target_price = row["target_price"]
        platform = row["platform"]

        # Fetch current price
        if platform.lower() == "amazon":
            current_price = get_amazon_price(url)
        elif platform.lower() == "flipkart":
            current_price = get_flipkart_price(url)
        else:
            continue

        # If price dropped, send alert
        if current_price is not None and current_price <= target_price:
            send_drop_alert(row["email"], row["product_name"], url, current_price)
            print(f"✅ Alert sent for {row['product_name']} - {current_price}")

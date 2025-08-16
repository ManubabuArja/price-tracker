from etl.amazon import scrape_amazon
from etl.flipkart import scrape_flipkart

def scrape_product(url: str) -> dict:
    """
    Route the scraping request based on the platform URL.
    Supports Amazon and Flipkart.
    """
    if "amazon" in url.lower():
        return scrape_amazon(url)
    elif "flipkart" in url.lower():
        return scrape_flipkart(url)
    else:
        return {
            "name": None,
            "price": None,
            "url": url,
            "platform": "Unknown"
        }

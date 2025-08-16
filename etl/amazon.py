import requests
from bs4 import BeautifulSoup

def scrape_amazon(url: str) -> dict:
    """
    Scrape product details from Amazon product page.
    Returns dictionary with product name and price in ₹.
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/115.0 Safari/537.36"
    }

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        return {"name": None, "price": None}

    soup = BeautifulSoup(response.content, "html.parser")

    # Try to extract product title
    title = soup.find(id="productTitle")
    product_name = title.get_text().strip() if title else "Amazon Product"

    # Try to extract price
    price_span = soup.find("span", {"class": "a-price-whole"})
    fraction_span = soup.find("span", {"class": "a-price-fraction"})
    if price_span:
        price_text = price_span.get_text().replace(",", "")
        if fraction_span:
            price_text += "." + fraction_span.get_text()
        try:
            price = float(price_text)
        except ValueError:
            price = None
    else:
        price = None

    return {
        "name": product_name,
        "price": price,
        "url": url,
        "platform": "Amazon"
    }

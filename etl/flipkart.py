import requests
from bs4 import BeautifulSoup

def scrape_flipkart(url: str) -> dict:
    """
    Scrape product details from Flipkart product page.
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

    # Extract product title
    title = soup.find("span", {"class": "B_NuCI"})
    product_name = title.get_text().strip() if title else "Flipkart Product"

    # Extract price
    price_div = soup.find("div", {"class": "_30jeq3 _16Jk6d"})
    if price_div:
        price_text = price_div.get_text().replace("₹", "").replace(",", "").strip()
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
        "platform": "Flipkart"
    }

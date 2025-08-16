from bs4 import BeautifulSoup
from .base import BaseScraper, ScrapeResult
from .normalize import parse_inr
from .http_helper import get


class AjioScraper(BaseScraper):
    sites = ["ajio.com"]

    def fetch(self, url: str) -> ScrapeResult:
        r = get(url)
        soup = BeautifulSoup(r.text, "lxml")

        title_el = soup.select_one("h1.prod-name") or soup.select_one("h1")
        price_el = soup.select_one("div.price .price-now") or soup.find(
            ["span", "div"], string=lambda t: t and "₹" in t
        )

        if not title_el or not price_el:
            raise RuntimeError("Ajio layout not recognized")

        title = title_el.get_text(strip=True)
        price_text = (
            price_el.get_text(strip=True)
            if hasattr(price_el, "get_text")
            else str(price_el)
        )

        return ScrapeResult(title=title, price=parse_inr(price_text), currency="INR")

from bs4 import BeautifulSoup
from .base import BaseScraper, ScrapeResult
from .normalize import parse_inr
from .http_helper import get


class MyntraScraper(BaseScraper):
    sites = ["myntra.com"]

    def fetch(self, url: str) -> ScrapeResult:
        r = get(url)
        soup = BeautifulSoup(r.text, "lxml")

        title_el = soup.select_one("h1.pdp-title") or soup.select_one("h1")
        brand_el = soup.select_one("h1.pdp-title .pdp-title") or soup.select_one(".pdp-title")
        subtitle_el = soup.select_one(".pdp-name")

        # Construct a decent title from available bits
        bits = []
        for el in (brand_el, title_el, subtitle_el):
            if el and el.get_text(strip=True) not in bits:
                bits.append(el.get_text(strip=True))
        title = " ".join([b for b in bits if b]) or (title_el.get_text(strip=True) if title_el else "")

        price_el = (
            soup.select_one("span.pdp-price") or
            soup.select_one(".pdp-price .pdp-price") or
            soup.find(["span", "div"], string=lambda t: t and "₹" in t)
        )
        price_text = (
            price_el.get_text(strip=True)
            if hasattr(price_el, "get_text")
            else (price_el or "")
        )

        if not title or not price_text:
            raise RuntimeError("Myntra layout not recognized")

        return ScrapeResult(title=title, price=parse_inr(price_text), currency="INR")

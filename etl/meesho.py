from bs4 import BeautifulSoup
from .base import BaseScraper, ScrapeResult
from .normalize import parse_inr
from .http_helper import get


class MeeshoScraper(BaseScraper):
    sites = ["meesho.com"]

    def fetch(self, url: str) -> ScrapeResult:
        r = get(url)
        soup = BeautifulSoup(r.text, "lxml")

        # Title falls under h1 or meta tags sometimes
        title_el = soup.select_one("h1") or soup.find("meta", {"property": "og:title"})
        title = (
            title_el.get_text(strip=True)
            if hasattr(title_el, "get_text")
            else (title_el["content"].strip() if title_el and title_el.has_attr("content") else "")
        )

        # Price text: look for ₹ in spans/divs
        price_el = soup.select_one("h4") or soup.find(
            ["span", "div"], string=lambda t: t and "₹" in t
        )
        price_text = (
            price_el.get_text(strip=True)
            if hasattr(price_el, "get_text")
            else (price_el or "")
        )

        if not title or not price_text:
            raise RuntimeError("Meesho layout not recognized")

        return ScrapeResult(title=title, price=parse_inr(price_text), currency="INR")

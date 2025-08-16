import os
import random
import time
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

UA_POOL = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/123.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 "
    "(KHTML, like Gecko) Version/17.0 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/120.0 Safari/537.36",
]

SCRAPE_MIN_DELAY_MS = int(os.getenv("SCRAPE_MIN_DELAY_MS", "800"))
SCRAPE_MAX_DELAY_MS = int(os.getenv("SCRAPE_MAX_DELAY_MS", "1800"))
HTTP_PROXY = os.getenv("HTTP_PROXY", "").strip() or None


def _session() -> requests.Session:
    s = requests.Session()
    retries = Retry(
        total=3, backoff_factor=0.6, status_forcelist=[429, 500, 502, 503, 504]
    )
    s.mount("http://", HTTPAdapter(max_retries=retries))
    s.mount("https://", HTTPAdapter(max_retries=retries))
    return s


def get(url: str) -> requests.Response:
    """Polite GET with a random User-Agent, retry, optional proxy, and delay."""
    time.sleep(random.uniform(SCRAPE_MIN_DELAY_MS/1000, SCRAPE_MAX_DELAY_MS/1000))
    headers = {"User-Agent": random.choice(UA_POOL)}
    proxies = {"http": HTTP_PROXY, "https": HTTP_PROXY} if HTTP_PROXY else None
    s = _session()
    r = s.get(url, headers=headers, timeout=25, proxies=proxies)
    r.raise_for_status()
    return r

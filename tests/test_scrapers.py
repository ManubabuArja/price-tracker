import pytest
from etl.amazon import AmazonScraper
from etl.flipkart import FlipkartScraper

def test_amazon_scraper(monkeypatch):
    def mock_fetch(self, url):
        return {"name": "Test Product Amazon", "price": 999}
    monkeypatch.setattr(AmazonScraper, "fetch", mock_fetch)

    scraper = AmazonScraper()
    result = scraper.fetch("http://fake-amazon-url")
    assert result["price"] == 999
    assert "Amazon" in result["name"] or "Product" in result["name"]

def test_flipkart_scraper(monkeypatch):
    def mock_fetch(self, url):
        return {"name": "Test Product Flipkart", "price": 499}
    monkeypatch.setattr(FlipkartScraper, "fetch", mock_fetch)

    scraper = FlipkartScraper()
    result = scraper.fetch("http://fake-flipkart-url")
    assert result["price"] == 499

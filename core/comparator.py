# core/comparator.py

from etl.base import scrape_product
from typing import List, Dict
import requests
from bs4 import BeautifulSoup
import re
import time
import random

def compare_urls(urls: List[str]) -> List[Dict]:
    """
    Compare multiple product URLs and return their details
    """
    results = []
    
    for url in urls:
        try:
            result = scrape_product(url)
            results.append({
                'url': url,
                'name': result['name'],
                'price': result['price'],
                'platform': result['platform'],
                'status': 'success'
            })
        except Exception as e:
            results.append({
                'url': url,
                'name': None,
                'price': None,
                'platform': 'Unknown',
                'status': 'error',
                'error': str(e)
            })
    
    return results

def get_mock_data(product_name: str) -> List[Dict]:
    """Get mock data for demonstration when websites are blocked"""
    mock_data = {
        "iphone 15": [
            {
                'name': 'Apple iPhone 15 (128GB) - Black',
                'price': 79999.0,
                'rating': 4.5,
                'platform': 'Amazon',
                'url': 'https://www.amazon.in/Apple-iPhone-15-128GB-Black/dp/B0CM5KJ8L8',
                'image': '',
                'reviews_count': 1250
            },
            {
                'name': 'iPhone 15 128GB Black',
                'price': 78999.0,
                'rating': 4.3,
                'platform': 'Flipkart',
                'url': 'https://www.flipkart.com/apple-iphone-15-black-128-gb/p/itm',
                'image': '',
                'reviews_count': 890
            },
            {
                'name': 'Apple iPhone 15 128GB',
                'price': 80999.0,
                'rating': 4.4,
                'platform': 'Myntra',
                'url': 'https://www.myntra.com/apple-iphone-15',
                'image': '',
                'reviews_count': 567
            }
        ],
        "nike shoes": [
            {
                'name': 'Nike Air Max 270 Running Shoes',
                'price': 12995.0,
                'rating': 4.6,
                'platform': 'Amazon',
                'url': 'https://www.amazon.in/Nike-Air-Max-270-Running/dp/B07KXK8Q8M',
                'image': '',
                'reviews_count': 2340
            },
            {
                'name': 'Nike Air Force 1 Low Sneakers',
                'price': 11995.0,
                'rating': 4.4,
                'platform': 'Flipkart',
                'url': 'https://www.flipkart.com/nike-air-force-1-low-sneakers/p/itm',
                'image': '',
                'reviews_count': 1567
            },
            {
                'name': 'Nike Revolution 6 Running Shoes',
                'price': 3995.0,
                'rating': 4.2,
                'platform': 'Myntra',
                'url': 'https://www.myntra.com/nike-revolution-6-running-shoes',
                'image': '',
                'reviews_count': 890
            },
            {
                'name': 'Nike Zoom Fly 4 Running Shoes',
                'price': 15995.0,
                'rating': 4.5,
                'platform': 'Meesho',
                'url': 'https://www.meesho.com/nike-zoom-fly-4-running-shoes/p/itm',
                'image': '',
                'reviews_count': 445
            }
        ],
        "vivo y100": [
            {
                'name': 'Vivo Y100 5G (8GB RAM, 128GB Storage)',
                'price': 24999.0,
                'rating': 4.3,
                'platform': 'Amazon',
                'url': 'https://www.amazon.in/Vivo-Y100-5G-Storage-Black/dp/B0BT8KX8Q8',
                'image': '',
                'reviews_count': 567
            },
            {
                'name': 'Vivo Y100 5G Smartphone',
                'price': 23999.0,
                'rating': 4.2,
                'platform': 'Flipkart',
                'url': 'https://www.flipkart.com/vivo-y100-5g-smartphone/p/itm',
                'image': '',
                'reviews_count': 423
            },
            {
                'name': 'Vivo Y100 5G Mobile Phone',
                'price': 25999.0,
                'rating': 4.1,
                'platform': 'Meesho',
                'url': 'https://www.meesho.com/vivo-y100-5g-mobile-phone/p/itm',
                'image': '',
                'reviews_count': 234
            }
        ],
        "samsung galaxy": [
            {
                'name': 'Samsung Galaxy S24 Ultra (12GB RAM, 256GB)',
                'price': 124999.0,
                'rating': 4.7,
                'platform': 'Amazon',
                'url': 'https://www.amazon.in/Samsung-Galaxy-S24-Ultra-256GB/dp/B0CM5KJ8L8',
                'image': '',
                'reviews_count': 890
            },
            {
                'name': 'Samsung Galaxy S24+ 5G Smartphone',
                'price': 99999.0,
                'rating': 4.6,
                'platform': 'Flipkart',
                'url': 'https://www.flipkart.com/samsung-galaxy-s24-plus-5g/p/itm',
                'image': '',
                'reviews_count': 567
            },
            {
                'name': 'Samsung Galaxy A55 5G Mobile',
                'price': 39999.0,
                'rating': 4.3,
                'platform': 'Myntra',
                'url': 'https://www.myntra.com/samsung-galaxy-a55-5g-mobile',
                'image': '',
                'reviews_count': 234
            }
        ],
        "laptop": [
            {
                'name': 'HP Pavilion 15.6-inch Laptop (Intel i5, 8GB RAM, 512GB SSD)',
                'price': 45999.0,
                'rating': 4.4,
                'platform': 'Amazon',
                'url': 'https://www.amazon.in/HP-Pavilion-15-6-inch-Laptop/dp/B08N5WRWNW',
                'image': '',
                'reviews_count': 1234
            },
            {
                'name': 'Dell Inspiron 15 3000 Series Laptop',
                'price': 42999.0,
                'rating': 4.3,
                'platform': 'Flipkart',
                'url': 'https://www.flipkart.com/dell-inspiron-15-3000-series-laptop/p/itm',
                'image': '',
                'reviews_count': 987
            },
            {
                'name': 'Lenovo IdeaPad 3 15.6-inch Laptop',
                'price': 39999.0,
                'rating': 4.2,
                'platform': 'Myntra',
                'url': 'https://www.myntra.com/lenovo-ideapad-3-15-6-inch-laptop',
                'image': '',
                'reviews_count': 654
            }
        ],
        "headphones": [
            {
                'name': 'Sony WH-1000XM4 Wireless Noise Cancelling Headphones',
                'price': 24990.0,
                'rating': 4.8,
                'platform': 'Amazon',
                'url': 'https://www.amazon.in/Sony-WH-1000XM4-Cancelling-Headphones/dp/B0863TXGM3',
                'image': '',
                'reviews_count': 2156
            },
            {
                'name': 'Bose QuietComfort 45 Wireless Headphones',
                'price': 28990.0,
                'rating': 4.7,
                'platform': 'Flipkart',
                'url': 'https://www.flipkart.com/bose-quietcomfort-45-wireless-headphones/p/itm',
                'image': '',
                'reviews_count': 1432
            },
            {
                'name': 'JBL Live 650BTNC Wireless Headphones',
                'price': 8999.0,
                'rating': 4.5,
                'platform': 'Meesho',
                'url': 'https://www.meesho.com/jbl-live-650btnc-wireless-headphones/p/itm',
                'image': '',
                'reviews_count': 789
            }
        ],
        "smartwatch": [
            {
                'name': 'Apple Watch Series 9 (GPS, 41mm)',
                'price': 41999.0,
                'rating': 4.6,
                'platform': 'Amazon',
                'url': 'https://www.amazon.in/Apple-Watch-Series-GPS-41mm/dp/B0CM5KJ8L8',
                'image': '',
                'reviews_count': 567
            },
            {
                'name': 'Samsung Galaxy Watch 6 Classic',
                'price': 34999.0,
                'rating': 4.5,
                'platform': 'Flipkart',
                'url': 'https://www.flipkart.com/samsung-galaxy-watch-6-classic/p/itm',
                'image': '',
                'reviews_count': 432
            },
            {
                'name': 'Fitbit Versa 4 Smartwatch',
                'price': 19999.0,
                'rating': 4.3,
                'platform': 'Myntra',
                'url': 'https://www.myntra.com/fitbit-versa-4-smartwatch',
                'image': '',
                'reviews_count': 321
            }
        ]
    }
    
    # Find the best match for the product name
    product_lower = product_name.lower()
    for key, data in mock_data.items():
        if key in product_lower or any(word in product_lower for word in key.split()):
            return data
    
    # If no exact match, return some generic results based on product type
    if any(word in product_lower for word in ['phone', 'mobile', 'smartphone']):
        return mock_data.get("iphone 15", [])
    elif any(word in product_lower for word in ['shoe', 'sneaker', 'footwear']):
        return mock_data.get("nike shoes", [])
    elif any(word in product_lower for word in ['laptop', 'computer']):
        return mock_data.get("laptop", [])
    elif any(word in product_lower for word in ['headphone', 'earphone', 'audio']):
        return mock_data.get("headphones", [])
    elif any(word in product_lower for word in ['watch', 'smartwatch']):
        return mock_data.get("smartwatch", [])
    
    # Generic fallback
    return [
        {
            'name': f'{product_name} - Sample Product 1',
            'price': random.randint(1000, 50000),
            'rating': round(random.uniform(3.5, 4.8), 1),
            'platform': 'Amazon',
            'url': f'https://www.amazon.in/s?k={product_name.replace(" ", "+")}',
            'image': '',
            'reviews_count': random.randint(100, 1000)
        },
        {
            'name': f'{product_name} - Sample Product 2',
            'price': random.randint(1000, 50000),
            'rating': round(random.uniform(3.5, 4.8), 1),
            'platform': 'Flipkart',
            'url': f'https://www.flipkart.com/search?q={product_name.replace(" ", "%20")}',
            'image': '',
            'reviews_count': random.randint(100, 1000)
        }
    ]

def search_products_by_name(product_name: str) -> List[Dict]:
    """
    Search for products by name across multiple e-commerce websites
    """
    results = []
    all_platforms_blocked = True
    
    # Clean and normalize the search query
    clean_query = product_name.lower().strip()
    
    # Search across different platforms
    platforms = [
        ('amazon', search_amazon),
        ('flipkart', search_flipkart),
        ('myntra', search_myntra),
        ('meesho', search_meesho)
    ]
    
    for platform_name, search_func in platforms:
        try:
            print(f"Searching {platform_name} for: {product_name}")
            platform_results = search_func(product_name)
            print(f"Found {len(platform_results)} results from {platform_name}")
            
            if platform_results:
                all_platforms_blocked = False
                results.extend(platform_results)
            
            # Random delay to avoid being blocked
            time.sleep(random.uniform(1, 3))
        except Exception as e:
            print(f"Error searching {platform_name}: {e}")
    
    # If all platforms are blocked or return no results, use mock data
    if all_platforms_blocked or len(results) == 0:
        print("All platforms blocked or no results found. Using mock data for demonstration.")
        mock_results = get_mock_data(clean_query)
        results.extend(mock_results)
    
    print(f"Total results found: {len(results)}")
    return results

def search_amazon(product_name: str) -> List[Dict]:
    """Search Amazon for products"""
    results = []
    
    try:
        # Create search URL
        search_query = product_name.replace(' ', '+')
        search_url = f"https://www.amazon.in/s?k={search_query}"
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
        }
        
        response = requests.get(search_url, headers=headers, timeout=15)
        if response.status_code != 200:
            print(f"Amazon response status: {response.status_code}")
            return results
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Multiple possible selectors for product cards
        product_selectors = [
            'div[data-component-type="s-search-result"]',
            'div.s-result-item',
            'div[data-asin]',
            'div.a-section.a-spacing-base'
        ]
        
        product_cards = []
        for selector in product_selectors:
            product_cards = soup.select(selector)
            if product_cards:
                break
        
        print(f"Found {len(product_cards)} product cards on Amazon")
        
        for card in product_cards[:8]:  # Limit to first 8 results
            try:
                # Multiple selectors for product name
                name_selectors = [
                    'h2 a span',
                    'h2.a-size-mini a',
                    'h2.a-size-base-plus a',
                    'h2.a-size-medium a',
                    'h2 a',
                    'span.a-size-medium'
                ]
                
                name = None
                for selector in name_selectors:
                    name_elem = card.select_one(selector)
                    if name_elem:
                        name = name_elem.get_text().strip()
                        if name and len(name) > 5:
                            break
                
                if not name:
                    continue
                
                # Multiple selectors for price
                price_selectors = [
                    'span.a-price-whole',
                    'span.a-price span.a-offscreen',
                    'span.a-price',
                    'span.a-color-price'
                ]
                
                price = None
                for selector in price_selectors:
                    price_elem = card.select_one(selector)
                    if price_elem:
                        price_text = price_elem.get_text().replace('₹', '').replace(',', '').replace('.', '')
                        try:
                            price = float(price_text)
                            break
                        except ValueError:
                            continue
                
                if not price:
                    continue
                
                # Multiple selectors for rating
                rating_selectors = [
                    'span.a-icon-alt',
                    'i.a-icon-star-small span',
                    'span[aria-label*="stars"]'
                ]
                
                rating = 0.0
                for selector in rating_selectors:
                    rating_elem = card.select_one(selector)
                    if rating_elem:
                        rating_text = rating_elem.get_text()
                        rating_match = re.search(r'(\d+\.?\d*)', rating_text)
                        if rating_match:
                            try:
                                rating = float(rating_match.group(1))
                                break
                            except ValueError:
                                continue
                
                # Extract URL
                url = ""
                link_elem = card.select_one('h2 a')
                if link_elem and link_elem.has_attr('href'):
                    url = "https://www.amazon.in" + link_elem['href']
                
                if url and name and price:
                    results.append({
                        'name': name,
                        'price': price,
                        'rating': rating,
                        'platform': 'Amazon',
                        'url': url,
                        'image': '',
                        'reviews_count': 0
                    })
                
            except Exception as e:
                print(f"Error parsing Amazon product: {e}")
                continue
    
    except Exception as e:
        print(f"Error searching Amazon: {e}")
    
    return results

def search_flipkart(product_name: str) -> List[Dict]:
    """Search Flipkart for products"""
    results = []
    
    try:
        # Create search URL
        search_query = product_name.replace(' ', '%20')
        search_url = f"https://www.flipkart.com/search?q={search_query}"
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
        }
        
        response = requests.get(search_url, headers=headers, timeout=15)
        if response.status_code != 200:
            print(f"Flipkart response status: {response.status_code}")
            return results
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Multiple possible selectors for product cards
        product_selectors = [
            'div._1AtVbE',
            'div[data-id]',
            'div._2kHMtA',
            'div._1xHGtK',
            'div[class*="product"]'
        ]
        
        product_cards = []
        for selector in product_selectors:
            product_cards = soup.select(selector)
            if product_cards:
                break
        
        print(f"Found {len(product_cards)} product cards on Flipkart")
        
        for card in product_cards[:8]:  # Limit to first 8 results
            try:
                # Multiple selectors for product name
                name_selectors = [
                    'div._4rR01T',
                    'a[title]',
                    'div[class*="title"]',
                    'div[class*="name"]',
                    'a[class*="title"]'
                ]
                
                name = None
                for selector in name_selectors:
                    name_elem = card.select_one(selector)
                    if name_elem:
                        name = name_elem.get_text().strip()
                        if name and len(name) > 5:
                            break
                
                if not name:
                    continue
                
                # Multiple selectors for price
                price_selectors = [
                    'div._30jeq3',
                    'div[class*="price"]',
                    'span[class*="price"]',
                    'div._1_WHN1'
                ]
                
                price = None
                for selector in price_selectors:
                    price_elem = card.select_one(selector)
                    if price_elem:
                        price_text = price_elem.get_text().replace('₹', '').replace(',', '').replace('.', '')
                        try:
                            price = float(price_text)
                            break
                        except ValueError:
                            continue
                
                if not price:
                    continue
                
                # Multiple selectors for rating
                rating_selectors = [
                    'div._3LWZlK',
                    'div[class*="rating"]',
                    'span[class*="rating"]'
                ]
                
                rating = 0.0
                for selector in rating_selectors:
                    rating_elem = card.select_one(selector)
                    if rating_elem:
                        try:
                            rating = float(rating_elem.get_text())
                            break
                        except ValueError:
                            continue
                
                # Extract URL
                url = ""
                link_selectors = [
                    'a._1fQZEK',
                    'a[href*="/p/"]',
                    'a[class*="link"]'
                ]
                
                for selector in link_selectors:
                    link_elem = card.select_one(selector)
                    if link_elem and link_elem.has_attr('href'):
                        url = "https://www.flipkart.com" + link_elem['href']
                        break
                
                if url and name and price:
                    results.append({
                        'name': name,
                        'price': price,
                        'rating': rating,
                        'platform': 'Flipkart',
                        'url': url,
                        'image': '',
                        'reviews_count': 0
                    })
                
            except Exception as e:
                print(f"Error parsing Flipkart product: {e}")
                continue
    
    except Exception as e:
        print(f"Error searching Flipkart: {e}")
    
    return results

def search_myntra(product_name: str) -> List[Dict]:
    """Search Myntra for products"""
    results = []
    
    try:
        # Create search URL - Myntra uses different URL structure
        search_query = product_name.replace(' ', '-').lower()
        search_url = f"https://www.myntra.com/search?query={search_query}"
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
        }
        
        response = requests.get(search_url, headers=headers, timeout=15)
        if response.status_code != 200:
            print(f"Myntra response status: {response.status_code}")
            return results
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Multiple possible selectors for product cards
        product_selectors = [
            'li.product-base',
            'div[class*="product"]',
            'div[class*="ProductCard"]',
            'li[class*="product"]'
        ]
        
        product_cards = []
        for selector in product_selectors:
            product_cards = soup.select(selector)
            if product_cards:
                break
        
        print(f"Found {len(product_cards)} product cards on Myntra")
        
        for card in product_cards[:8]:  # Limit to first 8 results
            try:
                # Multiple selectors for product name
                name_selectors = [
                    'h3.product-brand',
                    'h4[class*="product"]',
                    'div[class*="product-title"]',
                    'span[class*="product-name"]'
                ]
                
                name = None
                for selector in name_selectors:
                    name_elem = card.select_one(selector)
                    if name_elem:
                        name = name_elem.get_text().strip()
                        if name and len(name) > 5:
                            break
                
                if not name:
                    continue
                
                # Multiple selectors for price
                price_selectors = [
                    'span.product-discountedPrice',
                    'span[class*="price"]',
                    'div[class*="price"]',
                    'span[class*="discounted"]'
                ]
                
                price = None
                for selector in price_selectors:
                    price_elem = card.select_one(selector)
                    if price_elem:
                        price_text = price_elem.get_text().replace('Rs. ', '').replace('₹', '').replace(',', '').replace('.', '')
                        try:
                            price = float(price_text)
                            break
                        except ValueError:
                            continue
                
                if not price:
                    continue
                
                # Multiple selectors for rating
                rating_selectors = [
                    'div.product-ratings',
                    'div[class*="rating"]',
                    'span[class*="rating"]'
                ]
                
                rating = 0.0
                for selector in rating_selectors:
                    rating_elem = card.select_one(selector)
                    if rating_elem:
                        try:
                            rating_text = rating_elem.get_text()
                            rating_match = re.search(r'(\d+\.?\d*)', rating_text)
                            if rating_match:
                                rating = float(rating_match.group(1))
                                break
                        except ValueError:
                            continue
                
                # Extract URL
                url = ""
                link_selectors = [
                    'a.product-base-link',
                    'a[href*="/"]',
                    'a[class*="link"]'
                ]
                
                for selector in link_selectors:
                    link_elem = card.select_one(selector)
                    if link_elem and link_elem.has_attr('href'):
                        url = "https://www.myntra.com" + link_elem['href']
                        break
                
                if url and name and price:
                    results.append({
                        'name': name,
                        'price': price,
                        'rating': rating,
                        'platform': 'Myntra',
                        'url': url,
                        'image': '',
                        'reviews_count': 0
                    })
                
            except Exception as e:
                print(f"Error parsing Myntra product: {e}")
                continue
    
    except Exception as e:
        print(f"Error searching Myntra: {e}")
    
    return results

def search_meesho(product_name: str) -> List[Dict]:
    """Search Meesho for products"""
    results = []
    
    try:
        # Create search URL - Meesho uses different URL structure
        search_query = product_name.replace(' ', '%20')
        search_url = f"https://www.meesho.com/search?q={search_query}"
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
        }
        
        response = requests.get(search_url, headers=headers, timeout=15)
        if response.status_code != 200:
            print(f"Meesho response status: {response.status_code}")
            return results
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Multiple possible selectors for product cards
        product_selectors = [
            'div.ProductList__GridCol',
            'div[class*="ProductCard"]',
            'div[class*="product"]',
            'div[class*="card"]'
        ]
        
        product_cards = []
        for selector in product_selectors:
            product_cards = soup.select(selector)
            if product_cards:
                break
        
        print(f"Found {len(product_cards)} product cards on Meesho")
        
        for card in product_cards[:8]:  # Limit to first 8 results
            try:
                # Multiple selectors for product name
                name_selectors = [
                    'div.ProductCard__Title',
                    'div[class*="title"]',
                    'div[class*="name"]',
                    'span[class*="title"]'
                ]
                
                name = None
                for selector in name_selectors:
                    name_elem = card.select_one(selector)
                    if name_elem:
                        name = name_elem.get_text().strip()
                        if name and len(name) > 5:
                            break
                
                if not name:
                    continue
                
                # Multiple selectors for price
                price_selectors = [
                    'span.ProductCard__Price',
                    'span[class*="price"]',
                    'div[class*="price"]',
                    'span[class*="amount"]'
                ]
                
                price = None
                for selector in price_selectors:
                    price_elem = card.select_one(selector)
                    if price_elem:
                        price_text = price_elem.get_text().replace('₹', '').replace(',', '').replace('.', '')
                        try:
                            price = float(price_text)
                            break
                        except ValueError:
                            continue
                
                if not price:
                    continue
                
                # Meesho might not have ratings
                rating = 0.0
                
                # Extract URL
                url = ""
                link_elem = card.select_one('a')
                if link_elem and link_elem.has_attr('href'):
                    url = "https://www.meesho.com" + link_elem['href']
                
                if url and name and price:
                    results.append({
                        'name': name,
                        'price': price,
                        'rating': rating,
                        'platform': 'Meesho',
                        'url': url,
                        'image': '',
                        'reviews_count': 0
                    })
                
            except Exception as e:
                print(f"Error parsing Meesho product: {e}")
                continue
    
    except Exception as e:
        print(f"Error searching Meesho: {e}")
    
    return results

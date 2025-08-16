# core/tracker.py

import pandas as pd
import os
from datetime import datetime
from etl.base import scrape_product
import json

DATA_FILE = os.path.join("data", "warehouse.xlsx")
HISTORY_FILE = os.path.join("data", "history.xlsx")

# Ensure data directory exists
os.makedirs("data", exist_ok=True)

def ensure_data_files():
    """Create data files if they don't exist"""
    if not os.path.exists(DATA_FILE) or os.path.getsize(DATA_FILE) == 0:
        df = pd.DataFrame(columns=['product_id', 'title', 'url', 'site', 'last_seen_price', 'target_price', 'email', 'updated_at'])
        df.to_excel(DATA_FILE, index=False, engine='openpyxl')
    
    if not os.path.exists(HISTORY_FILE) or os.path.getsize(HISTORY_FILE) == 0:
        df = pd.DataFrame(columns=['product_id', 'price', 'timestamp'])
        df.to_excel(HISTORY_FILE, index=False, engine='openpyxl')

def get_next_product_id():
    """Get next available product ID"""
    if not os.path.exists(DATA_FILE) or os.path.getsize(DATA_FILE) == 0:
        return 1
    
    try:
        df = pd.read_excel(DATA_FILE, engine='openpyxl')
        if df.empty:
            return 1
        return df['product_id'].max() + 1
    except Exception:
        return 1

def track_once(url: str):
    """Track a product once and return product_id and result"""
    ensure_data_files()
    
    # Scrape product details
    result = scrape_product(url)
    
    if result['name'] is None or result['price'] is None:
        raise Exception("Failed to extract product information")
    
    # Create product record
    product_id = get_next_product_id()
    product_data = {
        'product_id': product_id,
        'title': result['name'],
        'url': url,
        'site': result['platform'],
        'last_seen_price': result['price'],
        'target_price': None,
        'email': None,
        'updated_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    
    # Add to main data
    try:
        df = pd.read_excel(DATA_FILE, engine='openpyxl')
    except Exception:
        df = pd.DataFrame(columns=['product_id', 'title', 'url', 'site', 'last_seen_price', 'target_price', 'email', 'updated_at'])
    
    df = pd.concat([df, pd.DataFrame([product_data])], ignore_index=True)
    df.to_excel(DATA_FILE, index=False, engine='openpyxl')
    
    # Add to history
    try:
        history_df = pd.read_excel(HISTORY_FILE, engine='openpyxl')
    except Exception:
        history_df = pd.DataFrame(columns=['product_id', 'price', 'timestamp'])
    
    history_data = {
        'product_id': product_id,
        'price': result['price'],
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    history_df = pd.concat([history_df, pd.DataFrame([history_data])], ignore_index=True)
    history_df.to_excel(HISTORY_FILE, index=False, engine='openpyxl')
    
    return product_id, result

def list_products():
    """List all tracked products"""
    ensure_data_files()
    
    if not os.path.exists(DATA_FILE) or os.path.getsize(DATA_FILE) == 0:
        return []
    
    try:
        df = pd.read_excel(DATA_FILE, engine='openpyxl')
        if df.empty:
            return []
        
        # Convert to list of dictionaries
        products = []
        for _, row in df.iterrows():
            products.append({
                'product_id': int(row['product_id']),
                'title': row['title'],
                'url': row['url'],
                'site': row['site'],
                'last_seen_price': float(row['last_seen_price']) if pd.notna(row['last_seen_price']) else 0.0,
                'target_price': float(row['target_price']) if pd.notna(row['target_price']) else None,
                'email': row['email'],
                'updated_at': row['updated_at']
            })
        
        return products
    except Exception as e:
        print(f"Error reading products: {e}")
        return []

def get_history(product_id: int):
    """Get price history for a specific product"""
    ensure_data_files()
    
    if not os.path.exists(HISTORY_FILE) or os.path.getsize(HISTORY_FILE) == 0:
        return []
    
    try:
        history_df = pd.read_excel(HISTORY_FILE, engine='openpyxl')
        product_history = history_df[history_df['product_id'] == product_id]
        
        if product_history.empty:
            return []
        
        # Sort by timestamp
        product_history = product_history.sort_values('timestamp', ascending=False)
        
        history = []
        for _, row in product_history.iterrows():
            history.append({
                'price': float(row['price']),
                'timestamp': row['timestamp']
            })
        
        return history
    except Exception as e:
        print(f"Error reading history: {e}")
        return []

def ensure_alert(product_id: int, email: str = None, target_price: float = None):
    """Set up price alert for a product"""
    ensure_data_files()
    
    if not os.path.exists(DATA_FILE) or os.path.getsize(DATA_FILE) == 0:
        return False
    
    try:
        df = pd.read_excel(DATA_FILE, engine='openpyxl')
        product_idx = df[df['product_id'] == product_id].index
        
        if len(product_idx) == 0:
            return False
        
        # Update the product record
        if email is not None:
            df.loc[product_idx[0], 'email'] = email
        if target_price is not None:
            df.loc[product_idx[0], 'target_price'] = target_price
        
        df.to_excel(DATA_FILE, index=False, engine='openpyxl')
        return True
    except Exception as e:
        print(f"Error updating alert: {e}")
        return False

def check_price_drops():
    """Check for price drops and send alerts"""
    ensure_data_files()
    
    if not os.path.exists(DATA_FILE) or os.path.getsize(DATA_FILE) == 0:
        return

    try:
        df = pd.read_excel(DATA_FILE, engine='openpyxl')
        
        for index, row in df.iterrows():
            url = row["url"]
            target_price = row["target_price"]
            platform = row["site"]
            
            if pd.isna(target_price):
                continue

            # Fetch current price
            try:
                result = scrape_product(url)
                current_price = result['price']
                
                if current_price is not None and current_price <= target_price:
                    print(f"✅ Price drop alert for {row['title']} - Current: ₹{current_price}, Target: ₹{target_price}")
                    
                    # Update the price in main data
                    df.loc[index, 'last_seen_price'] = current_price
                    df.loc[index, 'updated_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    
                    # Add to history
                    try:
                        history_df = pd.read_excel(HISTORY_FILE, engine='openpyxl')
                    except Exception:
                        history_df = pd.DataFrame(columns=['product_id', 'price', 'timestamp'])
                    
                    history_data = {
                        'product_id': int(row['product_id']),
                        'price': current_price,
                        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    }
                    history_df = pd.concat([history_df, pd.DataFrame([history_data])], ignore_index=True)
                    history_df.to_excel(HISTORY_FILE, index=False, engine='openpyxl')
                    
            except Exception as e:
                print(f"Error checking price for {row['title']}: {e}")
        
        # Save updated main data
        df.to_excel(DATA_FILE, index=False, engine='openpyxl')
    except Exception as e:
        print(f"Error in check_price_drops: {e}")

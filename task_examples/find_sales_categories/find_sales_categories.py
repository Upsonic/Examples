# task_examples/find_sales_categories/find_sales_categories.py

import os
import requests
import json
import re

# Load your Serper API key from env
SERPER_API_KEY = os.getenv("SERPER_API_KEY")
SEARCH_URL = "https://google.serper.dev/search"
SCRAPE_URL = "https://scrape.serper.dev"


def find_sales_categories(company_name: str):
    """
    Find website and extract sales categories for an ecommerce company.
    Returns: website_url, categories_list
    """
    if not SERPER_API_KEY:
        print("Error: Set SERPER_API_KEY environment variable")
        return None, []
    
    print(f"Finding website for {company_name}...")
    
    # Step 1: Find website
    headers = {"X-API-KEY": SERPER_API_KEY, "Content-Type": "application/json"}
    search_payload = {"q": f"{company_name} official website store"}
    
    try:
        response = requests.post(SEARCH_URL, headers=headers, json=search_payload, timeout=30)
        response.raise_for_status()
        results = response.json()
        
        if "organic" not in results or not results["organic"]:
            print(f"No website found for {company_name}")
            return None, []
        
        website_url = results["organic"][0]["link"]
        print(f"Found website: {website_url}")
        
    except Exception as e:
        print(f"Error finding website: {e}")
        return None, []
    
    # Step 2: Scrape website
    print(f"Scraping website content...")
    scrape_payload = json.dumps({"url": website_url})
    
    try:
        response = requests.post(SCRAPE_URL, headers=headers, data=scrape_payload, timeout=60)
        response.raise_for_status()
        data = response.json()
        
        text_content = data.get('text', '').lower()
        print(f"Scraped {len(text_content)} characters")
        
    except Exception as e:
        print(f"Error scraping website: {e}")
        return website_url, []
    
    # Step 3: Extract categories
    categories = set()
    
    # Simple category keywords
    category_words = [
        'men', 'women', 'kids', 'children', 'baby',
        'clothing', 'fashion', 'apparel', 'shoes', 'footwear',
        'electronics', 'tech', 'phones', 'laptops',
        'home', 'furniture', 'kitchen', 'decor',
        'beauty', 'cosmetics', 'makeup', 'skincare',
        'sports', 'fitness', 'outdoor', 'exercise',
        'books', 'games', 'toys', 'jewelry', 'accessories',
        'automotive', 'health', 'pets', 'garden'
    ]
    
    for word in category_words:
        if word in text_content:
            categories.add(word.title())
    
    categories_list = sorted(list(categories))
    print(f"Found categories: {', '.join(categories_list) if categories_list else 'None'}")
    
    return website_url, categories_list


if __name__ == "__main__":
    # Test with a few companies
    companies = ["Amazon", "Adidas", "Nike"]
    
    for company in companies:
        print(f"\n{'='*50}")
        print(f"Analyzing: {company}")
        print(f"{'='*50}")
        
        website, categories = find_sales_categories(company)
        
        if website:
            print(f"Website: {website}")
            print(f"Categories: {', '.join(categories) if categories else 'None found'}")
        else:
            print(f"Failed to analyze {company}")

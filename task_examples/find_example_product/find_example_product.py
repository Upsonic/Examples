import os
import sys
import json
import requests
from typing import Optional
from pydantic import BaseModel
from dotenv import load_dotenv

# Ensure repo root path for Upsonic imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from upsonic import Agent, Task
from task_examples.find_company_website.find_company_website import find_company_website

# --- Config ---
load_dotenv()
SERPER_API_KEY = os.getenv("SERPER_API_KEY")

if not SERPER_API_KEY:
    raise ValueError("SERPER_API_KEY missing in .env file.")


# --- Response Model ---
class ProductInfo(BaseModel):
    product_name: str
    product_price: Optional[str]
    product_brand: Optional[str]
    availability: Optional[str]
    url: Optional[str]


# --- Website Scraping Tool using Serper ---
def website_scraping(url: str) -> dict:
    """
    Use Serper API to fetch website content.
    Returns a dict with {url, content}.
    """
    endpoint = "https://google.serper.dev/scrape"
    headers = {"X-API-KEY": SERPER_API_KEY, "Content-Type": "application/json"}
    payload = {"url": url}

    try:
        resp = requests.post(endpoint, headers=headers, json=payload, timeout=30)
        resp.raise_for_status()
        data = resp.json()
        return {"url": url, "content": data.get("text", "")}
    except Exception as e:
        print(f"⚠️ Serper scraping failed for {url}: {e}")
        return {"url": url, "content": ""}


# --- Agent Setup ---
example_product_agent = Agent(name="example_product_agent")

def find_example_product_tool(company_name: str) -> ProductInfo:
    """
    Tool wrapper for Upsonic Task.
    The LLM will handle exploration using website_scraping.
    """
    site = find_company_website(company_name)
    website_url = str(site.website) if site and site.website else None
    if not website_url:
        return ProductInfo(
            product_name="Website not found",
            product_price=None,
            product_brand=company_name,
            availability=None,
            url=None,
        )

    print(f"🌍 Found website: {website_url}")
    return ProductInfo(
        product_name="LLM Exploration Needed",
        product_price=None,
        product_brand=company_name,
        availability=None,
        url=website_url,
    )


# --- CLI + Task definition ---
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Find an example product from a company's website using Serper & LLM.")
    parser.add_argument("--company", required=True, help="Company name, e.g. 'Nike', 'Adidas', 'Mavi'")
    args = parser.parse_args()

    # Define Task prompt
    task_prompt = f"""
You are an intelligent agent tasked with finding an example product from {args.company}'s website.

Steps:
1. Use the `find_example_product_tool` to get the official company website.
2. Then use `website_scraping` to read the website content.
3. Identify relevant sublinks or sections that likely contain product information (e.g., products, shop, catalog, collections, items).
4. Use `website_scraping` again to fetch those subpages as needed.
5. If you find a valid product page, extract:
   - product_name
   - product_price
   - product_brand
   - availability
   - url (the product page link)
6. Return the structured data as `ProductInfo`.
If you cannot find a product, retry with different relevant sublinks before giving up.
    """

    task = Task(
        description=task_prompt.strip(),
        tools=[website_scraping, find_example_product_tool],
        response_format=ProductInfo,
    )

    result = example_product_agent.do(task)
    print("\n" + "="*60)
    print("📦 FINAL RESULT")
    print("="*60)
    print(result.model_dump_json(indent=2))
    print("="*60)

import os
import re
import sys
import json
import requests
from typing import Optional, Iterable
from urllib.parse import urljoin, urlparse

from bs4 import BeautifulSoup
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


# Output model
class ProductInfo(BaseModel):
    product_name: str
    product_price: Optional[str]
    product_brand: Optional[str]
    availability: Optional[str]


# HTTP helpers (Direct scraping with fallback)
def scrape_url(url: str) -> str:
    """Fetch HTML content directly with proper headers."""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
    }
    
    try:
        resp = requests.get(url, headers=headers, timeout=30)
        resp.raise_for_status()
        return resp.text
    except requests.RequestException as e:
        print(f"⚠️ Failed to scrape {url}: {e}")
        return ""


# Link discovery on the site (robust & local; no Serper search noise)
_ALLOWED_PATH_HINTS: tuple[str, ...] = (
    "/product", "/products/", "/collections/", "/category/", "/catalog/",
    "/shop", "/buy", "/item", "/t/", "/p/", "/dp/", "/gp/product"
)

_EXCLUDE_SUBDOMAINS: set[str] = {
    "sellercentral", "support", "help", "press", "investor", "ir",
    "about", "careers", "jobs", "news", "blog", "community", "forums"
}


def _same_brand_host(link_host: str, brand_host: str) -> bool:
    """True if link host belongs to the same brand host."""
    if not link_host or not brand_host:
        return False
    link_host = link_host.lower()
    brand_host = brand_host.lower()
    if link_host == brand_host:
        return True
    return link_host.endswith("." + brand_host)


def _allowed_host(link_host: str) -> bool:
    """Filter out known non-store subdomains."""
    if not link_host:
        return False
    parts = link_host.split(".")
    # subdomain is everything before the last two labels
    if len(parts) > 2:
        sub = parts[0]
        if sub in _EXCLUDE_SUBDOMAINS:
            return False
    return True


def _rank_product_links(links: Iterable[str]) -> list[str]:
    """Simple ranking: deeper, with product-ish hints first."""
    def score(u: str) -> int:
        s = 0
        low = u.lower()
        for hint in _ALLOWED_PATH_HINTS:
            if hint in low:
                s += 10
        # deeper paths tend to be product pages
        s += min(20, low.count("/"))
        # shorter querystrings look nicer
        if "?" not in low:
            s += 3
        return s
    return sorted(set(links), key=score, reverse=True)


def find_product_link_from_site(home_url: str) -> Optional[str]:
    """Scrape homepage, then obvious collection pages to find a likely product URL."""
    base_html = scrape_url(home_url)
    if not base_html:
        return None

    brand_host = urlparse(home_url).netloc

    def collect_links(html: str, base: str) -> list[str]:
        soup = BeautifulSoup(html, "html.parser")
        out: list[str] = []
        for a in soup.find_all("a", href=True):
            href = a["href"].strip()
            if not href or href.startswith("#") or href.startswith("javascript:"):
                continue
            full = urljoin(base, href)
            p = urlparse(full)
            if not _same_brand_host(p.netloc, brand_host):
                continue
            if not _allowed_host(p.netloc):
                continue
            low = p.path.lower()
            if any(h in low for h in _ALLOWED_PATH_HINTS):
                out.append(full)
        return out

    # 1) Try homepage links
    links = collect_links(base_html, home_url)
    if links:
        return _rank_product_links(links)[0]

    # 2) Try common collection/category endpoints
    candidates = ["/products", "/collections", "/catalog", "/category", "/shop", "/buy"]
    for path in candidates:
        url = urljoin(home_url, path)
        html = scrape_url(url)
        if not html:
            continue
        links = collect_links(html, url)
        if links:
            return _rank_product_links(links)[0]

    return None


# Extraction utilities
_CURRENCY_RE = re.compile(r"[\$€£¥₺]\s?[\d,]+(?:\.\d{2})?")
_AVAIL_PATTERNS: list[tuple[re.Pattern, str]] = [
    (re.compile(r"in\s*stock", re.I), "In Stock"),
    (re.compile(r"out\s*of\s*stock|sold\s*out|unavailable", re.I), "Out of Stock"),
    (re.compile(r"pre[-\s]?order|coming\s*soon", re.I), "Pre-Order"),
    (re.compile(r"backorder|limited|few\s+left|only\s+\d+\s+left", re.I), "Limited Availability"),
    (re.compile(r"discontinued|no longer available", re.I), "Discontinued"),
]


def _first_text(el) -> Optional[str]:
    if not el:
        return None
    t = el.get_text(" ", strip=True)
    return t if t and len(t) >= 2 else None


def extract_product_info(product_html: str, fallback_brand: str) -> ProductInfo:
    """Extract name, price, brand, availability with robust fallbacks."""
    soup = BeautifulSoup(product_html, "html.parser")
    text = soup.get_text(" ", strip=True)

    # 1) JSON-LD Product first (most reliable)
    name, price, brand, availability = None, None, None, None
    for script in soup.find_all("script", attrs={"type": "application/ld+json"}):
        try:
            data = json.loads(script.string or "")
        except Exception:
            continue
        items = data if isinstance(data, list) else [data]
        for d in items:
            # Sometimes @graph holds everything
            if isinstance(d, dict) and "@graph" in d and isinstance(d["@graph"], list):
                items.extend(d["@graph"])
                continue
            if not isinstance(d, dict):
                continue
            typ = d.get("@type")
            # @type can be "Product" or ["Product", ...]
            is_product = (typ == "Product") or (isinstance(typ, list) and "Product" in typ)
            if not is_product:
                continue
            if not name:
                name = d.get("name") or name
            if not brand:
                b = d.get("brand")
                if isinstance(b, dict):
                    brand = b.get("name") or brand
                elif isinstance(b, str):
                    brand = b
            if not price:
                offers = d.get("offers")
                if isinstance(offers, dict):
                    p = offers.get("price")
                    c = offers.get("priceCurrency")
                    price = f"{c} {p}" if (p and c and not _CURRENCY_RE.search(str(p))) else (str(p) if p else price)
                elif isinstance(offers, list) and offers:
                    o = offers[0]
                    if isinstance(o, dict):
                        p = o.get("price")
                        c = o.get("priceCurrency")
                        price = f"{c} {p}" if (p and c and not _CURRENCY_RE.search(str(p))) else (str(p) if p else price)
            if not availability:
                offers = d.get("offers")
                av = None
                if isinstance(offers, dict):
                    av = offers.get("availability")
                elif isinstance(offers, list) and offers:
                    av = offers[0].get("availability")
                if isinstance(av, str):
                    if av.lower().endswith("/instock"):
                        availability = "In Stock"
                    elif av.lower().endswith("/outofstock"):
                        availability = "Out of Stock"

    # 2) OpenGraph / product meta fallbacks
    if not name:
        ogt = soup.find("meta", property="og:title")
        name = (ogt.get("content") if ogt and ogt.get("content") else None)
    if not brand:
        meta_brand = soup.find("meta", attrs={"name": "brand"}) or soup.find("meta", property="product:brand")
        if meta_brand and meta_brand.get("content"):
            brand = meta_brand["content"]
    if not price:
        meta_amount = soup.find("meta", property="product:price:amount")
        if meta_amount and meta_amount.get("content"):
            price = meta_amount["content"]
        else:
            m = _CURRENCY_RE.search(text)
            if m:
                price = m.group(0)

    # 3) Visible selectors
    if not name:
        for sel in ("h1", ".product-title", ".product-name", "[data-testid*=product]"):
            el = soup.select_one(sel)
            t = _first_text(el)
            if t:
                name = t
                break

    # 4) Availability text fallback
    if not availability:
        for pat, label in _AVAIL_PATTERNS:
            if pat.search(text):
                availability = label
                break

    # Finalize with fallbacks
    name = name or "Unknown Product"
    price = price or "Price not found"
    brand = brand or fallback_brand
    availability = availability or "Unknown"

    return ProductInfo(
        product_name=name,
        product_price=price,
        product_brand=brand,
        availability=availability,
    )


# Orchestration
def get_example_product(company_name: str) -> ProductInfo:
    """
    1) Find official website
    2) Discover a likely product URL from site links
    3) Scrape product page (rendered)
    4) Extract product info (JSON-LD/meta/regex fallbacks)
    """
    site = find_company_website(company_name)
    website_url = str(site.website) if (site and site.website) else ""
    if not website_url:
        return ProductInfo(product_name="Website not found", product_price=None, product_brand=company_name, availability=None)

    print(f"🌍 Found website: {website_url}")

    product_url = find_product_link_from_site(website_url)
    if not product_url:
        print("⚠️ No product-like URL discovered on the site.")
        return ProductInfo(product_name="No product found", product_price=None, product_brand=company_name, availability=None)

    print(f"🛒 Product candidate: {product_url}")

    html = scrape_url(product_url)
    if not html:
        return ProductInfo(product_name="Could not load product page", product_price=None, product_brand=company_name, availability=None)

    info = extract_product_info(html, fallback_brand=company_name)
    return info



# Upsonic Agent & CLI
example_product_agent = Agent(name="example_product_agent")

def find_example_product_tool(company_name: str) -> ProductInfo:
    """Tool wrapper for Upsonic to use inside the Task."""
    return get_example_product(company_name)

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Find an example product from a company's ecommerce website.")
    parser.add_argument("--company", required=True, help="Company name, e.g. 'Nike', 'Mavi', 'Adidas'")
    args = parser.parse_args()

    # Define Upsonic Task
    task = Task(
        description=f"Find an example product from {args.company}'s website",
        tools=[find_example_product_tool],
        response_format=ProductInfo,
    )

    # Execute through the Upsonic agent
    result = example_product_agent.do(task)
    print("\n" + "="*60)
    print("📦 FINAL RESULT")
    print("="*60)
    print(result.model_dump_json(indent=2))
    print("="*60)
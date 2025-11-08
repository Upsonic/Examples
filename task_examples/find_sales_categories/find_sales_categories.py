# task_examples/find_sales_categories/find_sales_categories.py

"""
Sales Category Agent (Generalized + Batch Support)
--------------------------------------------------
Finds a company's official website and extracts its top-level ecommerce
sales categories, such as major departments or product collections.

Usage:
    Single company:
        uv run task_examples/find_sales_categories/find_sales_categories.py --company "Nike"

    Multiple companies:
        uv run task_examples/find_sales_categories/find_sales_categories.py --companies "Nike, Lululemon, Apple"
"""

import argparse
import json
import os
import re
import sys
import requests
from bs4 import BeautifulSoup
from upsonic import Agent, Task, tool

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from task_examples.find_company_website.find_company_website import (  # noqa: E402
    agent as website_agent,
    get_company_candidates,
    WebsiteResponse,
)


# ======================================================
# 1. Website Finder Wrapper
# ======================================================

def find_company_website(company_name: str) -> WebsiteResponse:
    """Invoke the website-finder agent and return its structured response."""
    task = Task(
        description=(
            "Use the get_company_candidates tool to locate the official website for "
            f"'{company_name}'. Prefer domains that match the brand name and avoid social "
            "or news hosts. Return the best candidate with reasoning and confidence."
        ),
        tools=[get_company_candidates],
        response_format=WebsiteResponse,
    )
    return website_agent.do(task)


# ======================================================
# 2. Helper to Normalize Model Output
# ======================================================

def _normalize_categories(raw_result) -> list[str]:
    if isinstance(raw_result, list):
        return [str(item).strip() for item in raw_result if str(item).strip()]

    if isinstance(raw_result, dict):
        for key in ("categories", "result", "data"):
            value = raw_result.get(key)
            if isinstance(value, list):
                return [str(item).strip() for item in value if str(item).strip()]
            if isinstance(value, str):
                raw_result = value
                break
        else:
            return []

    if isinstance(raw_result, str):
        cleaned = raw_result.strip()
        if cleaned.startswith("```") and cleaned.endswith("```"):
            cleaned = cleaned.strip("`").strip()
            if "\n" in cleaned:
                _, cleaned = cleaned.split("\n", 1)
        cleaned = cleaned.strip()
        try:
            parsed = json.loads(cleaned)
            if isinstance(parsed, list):
                return [str(item).strip() for item in parsed if str(item).strip()]
        except json.JSONDecodeError:
            pass
        return [line.strip() for line in cleaned.splitlines() if line.strip()]

    return []


# ======================================================
# 3. Tool: Extract Ecommerce Categories
# ======================================================

@tool
def extract_categories(website_url: str) -> list[str]:
    """Scrape potential ecommerce category labels from navigation menus."""
    if not website_url:
        return []

    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        resp = requests.get(website_url, headers=headers, timeout=10)
        resp.raise_for_status()
    except Exception as e:
        print(f"Error fetching {website_url}: {e}")
        return []

    soup = BeautifulSoup(resp.text, "html.parser")

    candidate_roots = soup.select(
        "nav, header, [class*='menu'], [id*='menu'], [class*='nav'], "
        "[id*='nav'], [class*='category'], [id*='category'], [class*='departments']"
    )
    if not candidate_roots:
        candidate_roots = [soup]

    disallowed = {
        "home","about","contact","blog","support","faq","login","signup","account",
        "search","cart","wishlist","privacy","terms","careers","help","investors",
        "feedback","site map","accessibility","language","english","français","español"
    }

    cats, seen = [], set()
    for root in candidate_roots:
        for link in root.find_all("a", href=True):
            text = link.get_text(" ", strip=True)
            if not text:
                continue
            clean = re.sub(r"\s+", " ", text).strip()
            lower = clean.lower()
            if len(lower) < 3 or len(lower) > 40:
                continue
            if lower in disallowed:
                continue
            if not any(c.isalpha() for c in lower):
                continue
            if lower in seen:
                continue
            seen.add(lower)
            cats.append(clean)

    return cats


# ======================================================
# 4. Agent and Orchestration
# ======================================================

sales_category_agent = Agent(name="sales_category_agent")

def find_sales_categories(company_name: str) -> dict:
    """Find company website and extract its main shopping categories."""
    website_result = find_company_website(company_name)
    if not website_result.website:
        return {
            "company": company_name,
            "website": "",
            "categories": [],
            "reason": website_result.reasoning,
        }

    # Step 1: Extract candidate labels via HTML
    raw_categories = extract_categories(str(website_result.website))

    # Step 2: Let the LLM interpret the real shopping categories
    task = Task(
        description=(
            f"You are analyzing the ecommerce structure of {company_name}'s official website. "
            f"From the list below, identify the website's *main shopping or product categories* — "
            f"these represent the top-level departments or sections that customers browse when shopping.\n\n"
            f"Focus on categories that describe products, collections, or departments (e.g., 'Women', 'Men', 'Accessories', 'Electronics', 'Outdoor', 'Furniture', etc.).\n"
            f"Exclude any links related to customer service, login, privacy, help, language, or region selection.\n\n"
            f"Candidate categories:\n{raw_categories}\n\n"
            f"Return a clean JSON list of the main shopping categories only."
        ),
        agent=sales_category_agent,
    )

    refined = sales_category_agent.do(task)
    categories = _normalize_categories(refined)

    return {
        "company": company_name,
        "website": str(website_result.website),
        "categories": categories,
        "reason": website_result.reasoning,
    }


# ======================================================
# 5. CLI Entry Point (Single or Batch)
# ======================================================

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Find ecommerce sales categories for company or companies")
    parser.add_argument("--company", help="Single company name, e.g. 'Nike'")
    parser.add_argument("--companies", help="Comma-separated list, e.g. 'Nike, Lululemon, Apple'")
    args = parser.parse_args()

    if args.company:
        companies = [args.company.strip()]
    elif args.companies:
        companies = [c.strip() for c in args.companies.split(",") if c.strip()]
    else:
        parser.error("Please provide either --company or --companies")

    results = []
    for company in companies:
        print(f"\n🔍 Processing: {company}")
        result = find_sales_categories(company)
        results.append(result)
        print(f"\n✅ Result for {company}: {result}\n")

    if len(results) > 1:
        os.makedirs("outputs", exist_ok=True)
        output_path = "outputs/sales_categories.json"
        with open(output_path, "w") as f:
            json.dump(results, f, indent=2)
        print(f"\n📦 All results saved to {output_path}")

# task_examples/find_company_website/serper_client.py

import os
import requests
from dotenv import load_dotenv

load_dotenv()

SERPER_API_KEY = os.getenv("SERPER_API_KEY")
SERPER_URL = "https://google.serper.dev/search"

# Common junk domains we don't want to consider as "official websites"
BAD_DOMAINS = [
    "wikipedia.org",
    "linkedin.com",
    "crunchbase.com",
    "facebook.com",
    "twitter.com",
    "x.com",
    "youtube.com",
    "instagram.com",
    "glassdoor.com",
    "indeed.com",
]


def search_company(query: str) -> dict:
    """Search for the company using Serper API."""
    if not SERPER_API_KEY:
        raise ValueError("Missing SERPER_API_KEY in .env")
    headers = {"X-API-KEY": SERPER_API_KEY, "Content-Type": "application/json"}
    resp = requests.post(SERPER_URL, headers=headers, json={"q": query})
    resp.raise_for_status()
    return resp.json()


def find_company_candidates(company_name: str, top_k: int = 5) -> list[str]:
    """Return top candidate links, skipping known irrelevant domains."""
    results = search_company(company_name)
    raw_links = [r["link"] for r in results.get("organic", []) if "link" in r]

    candidates = []
    for url in raw_links:
        if any(bad in url for bad in BAD_DOMAINS):
            continue
        candidates.append(url)
        if len(candidates) >= top_k:
            break

    return candidates
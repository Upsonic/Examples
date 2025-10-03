import re
from urllib.parse import urljoin, urlparse
import requests
from bs4 import BeautifulSoup
from upsonic import tool


@tool
def extract_categories(website_url: str) -> list[str]:
    """
    Tool: Extract ecommerce sales categories from a website.
    """
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

    parsed_url = urlparse(website_url)
    base_domain = parsed_url.netloc

    disallowed = {
        "home","about","contact","blog","support","faq","login","signup",
        "account","search","cart","wishlist","privacy","terms","careers"
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
            if lower in seen:
                continue
            if not any(c.isalpha() for c in lower):
                continue

            seen.add(lower)
            cats.append(clean)

    return cats

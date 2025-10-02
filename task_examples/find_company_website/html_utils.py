# task_examples/find_company_website/html_utils.py

import requests
from bs4 import BeautifulSoup


DEFAULT_HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; UpsonicExamples/1.0)",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
}

def fetch(url: str, timeout: int = 10) -> str:
    """Fetch HTML text for a given URL."""
    resp = requests.get(url, headers=DEFAULT_HEADERS, timeout=timeout)
    resp.raise_for_status()
    return resp.text


def extract_text_signals(html: str) -> dict:
    """Extract simple signals: title and h1 tags."""
    soup = BeautifulSoup(html, "lxml")
    title = soup.title.string.strip() if soup.title else ""
    h1s = [h.get_text(" ", strip=True) for h in soup.find_all("h1")]
    return {"title": title, "h1": h1s}

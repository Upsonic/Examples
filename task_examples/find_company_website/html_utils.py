import re
import json
from typing import List, Dict, Optional, Tuple
from urllib.parse import urlparse, urljoin

import requests
from bs4 import BeautifulSoup

DEFAULT_HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; UpsonicExamples/1.0; +https://example.com/bot)",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
}

def normalize_domain(url: str) -> str:
    """Return effective hostname without scheme/port/www., lowercase."""
    parsed = urlparse(url)
    host = (parsed.netloc or parsed.path).lower()
    host = host.split(":")[0]
    host = host[4:] if host.startswith("www.") else host
    return host

def canonical_url(url: str) -> str:
    """Strip fragments/query, ensure scheme, no trailing slash (except root)."""
    if not url.startswith(("http://", "https://")):
        url = "https://" + url
    parsed = urlparse(url)
    path = parsed.path if parsed.path not in ("", "/") else ""
    return f"{parsed.scheme}://{parsed.netloc}{path}"

def fetch(url: str, timeout: int = 10) -> Tuple[str, str]:
    """
    GET the URL with redirects. Return (final_url, text). Raise for bad status.
    """
    resp = requests.get(url, headers=DEFAULT_HEADERS, timeout=timeout, allow_redirects=True)
    resp.raise_for_status()
    return (resp.url, resp.text)

def parse_json_ld(soup: BeautifulSoup) -> List[Dict]:
    data = []
    for tag in soup.find_all("script", type="application/ld+json"):
        try:
            loaded = json.loads(tag.string or "{}")
            if isinstance(loaded, dict):
                data.append(loaded)
            elif isinstance(loaded, list):
                data.extend(loaded)
        except Exception:
            continue
    return data

def extract_text_signals(html: str) -> Dict[str, List[str] | str]:
    soup = BeautifulSoup(html, "lxml")
    title = (soup.title.string or "").strip() if soup.title else ""
    h1s = [h.get_text(" ", strip=True) for h in soup.find_all("h1")]
    foot = soup.find("footer")
    footer_text = foot.get_text(" ", strip=True) if foot else ""
    metas = {m.get("property") or m.get("name"): m.get("content", "")
             for m in soup.find_all("meta") if (m.get("property") or m.get("name"))}
    json_ld = parse_json_ld(soup)
    return {
        "title": title,
        "h1": h1s,
        "footer": footer_text,
        "metas": metas,
        "json_ld": json_ld,
    }

def normalize_text(s: str) -> str:
    """
    Normalize text for matching:
    - Uppercase
    - Handle common encoding issues and special characters
    """
    if s is None:
        return ""
    s = s.upper()
    # Handle common encoding issues and special characters
    s = s.replace("–", "-").replace("—", "-").replace(""", "\"").replace(""", "\"")
    s = s.replace("â", "A").replace("ê", "E").replace("î", "I").replace("ô", "O").replace("û", "U")
    s = s.replace("Â", "A").replace("Ê", "E").replace("Î", "I").replace("Ô", "O").replace("Û", "U")
    # Handle Turkish characters (for compatibility)
    s = s.replace("Ş", "S").replace("Ğ", "G").replace("Ç", "C").replace("Ö", "O").replace("Ü", "U")
    s = s.replace("İ", "I")
    s = re.sub(r"\s+", " ", s)
    return s.strip()

OFFICIAL_SUFFIXES = [
    "INC", "LLC", "CORP", "CORPORATION", "LTD", "LIMITED",
    "A.S.", "AS", "ANONIM SIRKETI", "ANONİM ŞİRKETİ",
    "LTD. ŞTİ.", "LTD STI", "LIMITED SIRKETI", "LİMİTED ŞİRKETİ"
]

def name_match_score(company_name: str, signals: Dict) -> float:
    """
    Heuristic score:
    +0.7 if normalized company name appears in title/h1/footer/og:site_name
    +0.5 if Organization JSON-LD 'name' matches (normalized)
    +0.3 if any official suffix appears near name in the page text signals
    threshold >= 0.5 => accept
    """
    target = normalize_text(company_name)
    score = 0.0

    title = normalize_text(signals.get("title", ""))
    h1 = " ".join(normalize_text(x) for x in signals.get("h1", []))
    footer = normalize_text(signals.get("footer", ""))
    metas = signals.get("metas", {}) or {}
    og_site = normalize_text(metas.get("og:site_name", "") or metas.get("og:title", ""))

    # Extract company name without suffixes for partial matching
    company_words = target.split()
    company_base = company_words[0] if company_words else target  # First word (usually company name)

    # Check for full company name match
    if target and (target in title or target in h1 or target in footer or target in og_site):
        score += 0.7
    # Check for partial match (company name without suffixes)
    elif company_base and len(company_base) > 3 and (company_base in title or company_base in h1 or company_base in footer or company_base in og_site):
        score += 0.5

    for obj in signals.get("json_ld", []):
        try:
            if isinstance(obj, dict) and (obj.get("@type") in ("Organization", "Corporation", "LocalBusiness")):
                name = normalize_text(obj.get("name", ""))
                if name and target and (name == target or target in name or name in target):
                    score += 0.5
        except Exception:
            continue

    # suffix proximity (rough check)
    blob = " ".join([title, h1, footer, og_site])
    for suf in OFFICIAL_SUFFIXES:
        if suf in blob:
            score += 0.3
            break

    return score

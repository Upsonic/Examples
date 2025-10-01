import argparse
from typing import Optional

from pydantic import BaseModel, HttpUrl

try:
    from .html_utils import (
        fetch, extract_text_signals, normalize_domain, canonical_url, name_match_score
    )
    from .serper_client import search_company
except ImportError:
    from html_utils import (
        fetch, extract_text_signals, normalize_domain, canonical_url, name_match_score
    )
    from serper_client import search_company

# Local helper: get multiple candidates (duplicated here to keep this file standalone runnable)
def find_company_candidates(company_name: str, top_k: int = 5) -> list[str]:
    results = search_company(company_name)
    raw = [r["link"] for r in results.get("organic", []) if "link" in r][: max(10, top_k)]
    # filter and dedupe by domain
    bad_hosts = ("linkedin.", "wikipedia.", "crunchbase.", "facebook.", "instagram.", "twitter.", "x.com", "youtube.", "medium.")
    seen = set()
    out = []
    for url in raw:
        host = normalize_domain(url)
        if any(b in host for b in bad_hosts):
            continue
        if host in seen:
            continue
        seen.add(host)
        out.append(canonical_url(url))
        if len(out) >= top_k:
            break
    return out

class ValidationResult(BaseModel):
    company: str
    website: Optional[HttpUrl] = None
    validated: bool = False
    checked: int = 0
    reason: Optional[str] = None

def validate_candidate(company: str, url: str) -> bool:
    try:
        final_url, html = fetch(url, timeout=10)
        signals = extract_text_signals(html)
        score = name_match_score(company, signals)
        return score >= 0.5  # Fixed threshold
    except Exception:
        return False

if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Validate company website ownership with retry.")
    ap.add_argument("--company", required=True, help='Company legal name, e.g. "Upsonic Teknoloji A.Ş"')
    ap.add_argument("--top-k", type=int, default=5, help="Max candidates to try from Serper")
    args = ap.parse_args()

    candidates = find_company_candidates(args.company, top_k=args.top_k)
    result = ValidationResult(company=args.company, checked=0)

    for idx, site in enumerate(candidates, 1):
        print(f"[{idx}/{len(candidates)}] Validating {site} ...")
        ok = validate_candidate(args.company, site)
        if ok:
            result.website = site  # type: ignore
            result.validated = True
            result.checked = idx
            print(f"Valid: {args.company} → {site}")
            break
    else:
        result.checked = len(candidates)
        result.validated = False
        result.reason = "No candidate reached threshold"

    # Final human-friendly print (JSON could be added later if needed)
    print("----")
    print("Company:", result.company)
    print("Validated:", result.validated)
    print("Website:", result.website or "N/A")
    print("Checked:", result.checked)
    if result.reason:
        print("Reason:", result.reason)
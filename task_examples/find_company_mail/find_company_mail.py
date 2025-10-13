import sys
import os
import argparse
from typing import Optional
from urllib.parse import urlparse

# Allow running as a script
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from pydantic import BaseModel

try:
    from task_examples.find_company_mail.serper_client import search_mail_query
    from task_examples.find_company_mail.email_utils import extract_emails_from_text
except ImportError:
    from serper_client import search_mail_query
    from email_utils import extract_emails_from_text


class MailResponse(BaseModel):
    company: str
    email: Optional[str] = None
    source: Optional[str] = None


def _normalize_to_domain(company_or_url: str) -> str:
    """Accepts a domain (e.g., linktera.com) or URL (https://linktera.com/) and returns the domain."""
    text = company_or_url.strip()
    if not text:
        return text
    has_scheme = text.startswith("http://") or text.startswith("https://")
    to_parse = text if has_scheme else f"http://{text}"
    parsed = urlparse(to_parse)
    host = parsed.netloc or parsed.path
    host = host.strip().lower()
    if host.startswith("www."):
        host = host[4:]
    # Remove trailing slashes if any leaked into host
    host = host.split("/")[0]
    return host


def find_company_mail(company: str) -> MailResponse:
    domain = _normalize_to_domain(company)
    query = f"mail: {domain}" if domain else f"mail: {company}"

    try:
        data = search_mail_query(query)
    except Exception as e:
        return MailResponse(company=company, email=None, source=None)

    # Try to extract from organic results: titles, snippets, links
    candidates = []
    sources = []
    for item in data.get("organic", []):
        page_link = item.get("link")
        for field in ("title", "snippet"):
            val = item.get(field)
            if val:
                emails = extract_emails_from_text(val)
                if emails:
                    candidates.extend(emails)
                    sources.extend([page_link] * len(emails))
        link = item.get("link")
        if link:
            emails = extract_emails_from_text(link)
            if emails:
                candidates.extend(emails)
                sources.extend([link] * len(emails))

    # De-duplicate while preserving order
    seen = set()
    unique_candidates = []
    unique_sources = []
    for idx, c in enumerate(candidates):
        if c not in seen:
            seen.add(c)
            unique_candidates.append(c)
            # align the corresponding source if available
            src = sources[idx] if idx < len(sources) else None
            unique_sources.append(src)

    # Prefer emails that match the provided domain
    if domain:
        for idx, email in enumerate(unique_candidates):
            email_l = email.lower()
            if email_l.endswith("@" + domain) or email_l.endswith("@www." + domain):
                return MailResponse(company=company, email=email, source=unique_sources[idx])

    if unique_candidates:
        return MailResponse(company=company, email=unique_candidates[0], source=unique_sources[0])
    return MailResponse(company=company, email=None, source=None)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Find a company's email via web search")
    parser.add_argument("--company", required=True, help="Company name")
    args = parser.parse_args()

    result = find_company_mail(args.company)
    print(result.model_dump_json(indent=2))



# task_examples/find_company_website/validate_company_website.py

import argparse
from upsonic import Agent, Task
from pydantic import BaseModel, HttpUrl
from typing import Optional
from urllib.parse import urlparse

from html_utils import fetch, extract_text_signals
from bs4 import BeautifulSoup


class ValidationResult(BaseModel):
    company: str
    website: Optional[HttpUrl] = None
    validated: bool = False
    score: float = 0.0
    reason: Optional[str] = None


def validate_candidate(company: str, url: str) -> ValidationResult:
    """
    Validate whether the given URL belongs to the specified company.
    - Strongly prefer domains that contain the brand token.
    - Accept matches in title, h1, or footer text.
    """
    try:
        html = fetch(url, timeout=10)
        signals = extract_text_signals(html)

        company_upper = company.upper()
        brand = company_upper.split()[0] 
        title = signals.get("title", "").upper()
        h1s = " ".join(signals.get("h1", [])).upper()

        # Footer text
        soup = BeautifulSoup(html, "lxml")
        footer = soup.find("footer")
        footer_text = footer.get_text(" ", strip=True).upper() if footer else ""

        domain = urlparse(url).netloc.lower()

        # Strong signal: brand in domain
        if brand.lower() in domain:
            return ValidationResult(company=company, website=url, validated=True, score=0.9, reason="Brand in domain")

        # Full company name in title, h1, or footer
        if company_upper in title or company_upper in h1s or company_upper in footer_text:
            return ValidationResult(company=company, website=url, validated=True, score=0.8, reason="Full name match in title/h1/footer")

        # Brand token in title, h1, or footer
        if brand in title or brand in h1s or brand in footer_text:
            return ValidationResult(company=company, website=url, validated=True, score=0.6, reason="Brand match in title/h1/footer")

        return ValidationResult(company=company, website=url, validated=False, score=0.0, reason="No match in title/h1/footer")
    except Exception as e:
        return ValidationResult(company=company, website=url, validated=False, score=0.0, reason=str(e))


def validate_tool(company: str, url: str) -> ValidationResult:
    """Tool: Validate if the given URL is the official website of the company."""
    return validate_candidate(company, url)


agent = Agent(name="website_validator")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Validate a company website.")
    parser.add_argument("--company", required=True, help="Company name, e.g. 'Amazon Inc'")
    parser.add_argument("--url", required=True, help="Website URL, e.g. 'https://www.amazon.com/'")
    args = parser.parse_args()

    task = Task(
        description=f"Validate if {args.url} belongs to {args.company}",
        tools=[validate_tool],
        response_format=ValidationResult,
    )

    result = agent.do(task)
    print(result.model_dump_json(indent=2))

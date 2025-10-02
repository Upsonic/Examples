# task_examples/find_company_website/find_company_website.py

import argparse
from upsonic import Agent, Task
from pydantic import BaseModel, HttpUrl
from typing import Optional

from serper_client import find_company_candidates
from validate_company_website import validate_candidate, ValidationResult


class WebsiteResponse(BaseModel):
    company: str
    website: Optional[HttpUrl] = None
    validated: bool = False
    score: float = 0.0
    reason: Optional[str] = None


def find_company_website(company: str) -> WebsiteResponse:
    """
    Find the official website for a company using Serper search + validation.
    - Validate all candidates and return the one with the highest score.
    """
    try:
        candidates = find_company_candidates(company, top_k=5)

        best_result: Optional[ValidationResult] = None
        for url in candidates:
            result: ValidationResult = validate_candidate(company, url)
            if not best_result or result.score > best_result.score:
                best_result = result

        if best_result:
            return WebsiteResponse(
                company=company,
                website=best_result.website,
                validated=best_result.validated,
                score=best_result.score,
                reason=best_result.reason,
            )

        return WebsiteResponse(company=company, website=None, validated=False, reason="No valid site found")

    except Exception as e:
        return WebsiteResponse(company=company, website=None, validated=False, reason=str(e))


def find_tool(company: str) -> WebsiteResponse:
    """Tool: Find the official website for a company using Serper + validation."""
    return find_company_website(company)


agent = Agent(name="website_finder")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Find a company's official website.")
    parser.add_argument("--company", required=True, help="Company name, e.g. 'Amazon Inc'")
    args = parser.parse_args()

    task = Task(
        description=f"Find the official website of {args.company}",
        tools=[find_tool],
        response_format=WebsiteResponse,
    )

    result = agent.do(task)
    print(result.model_dump_json(indent=2))

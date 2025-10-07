import os
import sys
import requests
from typing import List, Optional
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


# --- Response Models ---
class AgreementLink(BaseModel):
    url: str
    is_available: Optional[bool] = None
    is_agreement_page: Optional[bool] = None


class AgreementLinksResponse(BaseModel):
    company_name: str
    website: Optional[str]
    agreements: List[AgreementLink]


# --- Website Scraping Tool (Serper API) ---
def website_scraping(url: str) -> dict:
    """
    Use Serper API to fetch website content.
    Returns a dict with {url, content, links}.
    """
    endpoint = "https://google.serper.dev/scrape"
    headers = {"X-API-KEY": SERPER_API_KEY, "Content-Type": "application/json"}
    payload = {"url": url}

    try:
        resp = requests.post(endpoint, headers=headers, json=payload, timeout=30)
        resp.raise_for_status()
        data = resp.json()
        return {"url": url, "content": data.get("text", ""), "links": data.get("links", [])}
    except Exception as e:
        print(f"⚠️ Serper scraping failed for {url}: {e}")
        return {"url": url, "content": "", "links": []}


# --- Agent Setup ---
agreement_agent = Agent(name="agreement_agent")


# --- CLI + Task Definition ---
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Find agreement or policy links from a company's website.")
    parser.add_argument("--company", required=True, help="Company name, e.g. 'Nike', 'Adidas', 'Mavi'")
    args = parser.parse_args()

    # Define Task prompt — LLM handles all logic
    task_prompt = f"""
You are an intelligent autonomous LLM agent tasked with discovering and verifying all *agreement or policy* pages on {args.company}'s website.

### Your Mission
Find and confirm links to pages that define company agreements, policies, or legal terms such as:
- Privacy Policy
- Terms of Service / Terms & Conditions
- Cookie Policy
- Return or Refund Policy
- Legal Notice / GDPR / Data Policy / User Agreement

### Instructions
1. Use the `find_company_website` tool to get the company's official website.
2. Use `website_scraping` to fetch and read the homepage content.
   - If the homepage doesn’t include relevant links, explore subpages like `/help`, `/support`, `/legal`, `/info`, `/about`, or `/footer`.
3. Identify links or sections that are likely related to agreements or policies.
   - Look for keywords: privacy, terms, policy, refund, cookie, gdpr, legal, agreement, compliance, data, protection, conditions.
4. For each candidate link:
   - Use `website_scraping` again to fetch the subpage content.
   - Determine if the page is reachable (status 200) and if its text contextually describes an agreement/policy.
   - Confirm based on patterns like:
     * mentions of "personal data", "user consent", "terms of use", "cookies", "privacy", "legal rights", "disclaimer", "data processing".
5. Prioritize pages that explicitly appear to be legal, policy, or terms documents.
6. If no valid pages are found, retry by exploring deeper navigation pages or help sections.
7. Return your final structured JSON result using this format:

{{
  "company_name": "{args.company}",
  "website": "<official website>",
  "agreements": [
    {{
      "url": "<page_url>",
      "is_available": true,
      "is_agreement_page": true
    }}
  ]
}}

### Rules
- Be persistent. Explore multiple subpages if necessary.
- Never return an empty list unless you have verified there are truly no agreement or policy pages.
- Only use the provided tools (`find_company_website` and `website_scraping`) to explore.
- Keep responses factual, structured, and concise.
"""



    task = Task(
        description=task_prompt.strip(),
        tools=[website_scraping, find_company_website],
        response_format=AgreementLinksResponse,
    )

    result = agreement_agent.do(task)
    print("\n" + "=" * 60)
    print("📄 AGREEMENT LINKS RESULT")
    print("=" * 60)
    print(result.model_dump_json(indent=2))
    print("=" * 60)

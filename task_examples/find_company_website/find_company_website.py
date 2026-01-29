"""
Find Company Website Agent (Upsonic Reasoning Demo)

This example demonstrates how an Upsonic Agent can:
1. Use a simple tool to gather candidate websites (via Serper)
2. Reason about which one is official based on names, domains, and context
3. Produce a structured, validated response — autonomously

Educational focus: letting the Agent, not the code, make the reasoning decisions.
"""

import os, json, requests
from typing import Optional
from pydantic import BaseModel, HttpUrl
from upsonic import Agent, Task
from dotenv import load_dotenv

load_dotenv()

SERPER_API_KEY = os.getenv("SERPER_API_KEY")
SERPER_URL = "https://google.serper.dev/search"
HEADERS = {"X-API-KEY": SERPER_API_KEY, "Content-Type": "application/json"}

BAD_DOMAINS = [
    "linkedin.com", "facebook.com", "twitter.com", "x.com",
    "youtube.com", "crunchbase.com", "wikipedia.org", "glassdoor.com"
]


# --- Pydantic response model ---
class WebsiteResponse(BaseModel):
    company: str
    website: Optional[HttpUrl] = None
    validated: bool = False
    reasoning: Optional[str] = None
    confidence: float = 0.0


# --- TOOL: Fetch candidate websites ---
def get_company_candidates(company: str) -> list[str]:
    """Simple search tool to get top candidate URLs for a company."""
    resp = requests.post(SERPER_URL, headers=HEADERS, json={"q": company})
    resp.raise_for_status()
    data = resp.json()
    links = [r["link"] for r in data.get("organic", []) if "link" in r]
    return [u for u in links if not any(bad in u for bad in BAD_DOMAINS)]


# --- MAIN AGENT ---
agent = Agent(name="find_company_website_agent")


# --- Reusable function for finding company website ---
def find_company_website(company: str) -> str:
    """
    Find a company's official website using Upsonic agent reasoning.
    
    Args:
        company: Company name to search for
        
    Returns:
        The official website URL as a string, or empty string if not found
    """
    task = Task(
        description=f"""
        Use the 'get_company_candidates' tool to find potential websites for {company}.
        Evaluate which URL is most likely the company's *official website* by reasoning about:
        - Domain name similarity to the brand
        - Presence of the brand or company name in the URL
        - Likelihood that it's not a social or news site
        Return the best website with reasoning and confidence.
        """,
        tools=[get_company_candidates],
        response_format=WebsiteResponse,
    )
    
    result = agent.do(task)
    return str(result.website) if result.website else ""


async def afind_company_website(company: str) -> str:
    """
    Async version of find_company_website.
    
    Args:
        company: Company name to search for
        
    Returns:
        The official website URL as a string, or empty string if not found
    """
    task = Task(
        description=f"""
        Use the 'get_company_candidates' tool to find potential websites for {company}.
        Evaluate which URL is most likely the company's *official website* by reasoning about:
        - Domain name similarity to the brand
        - Presence of the brand or company name in the URL
        - Likelihood that it's not a social or news site
        Return the best website with reasoning and confidence.
        """,
        tools=[get_company_candidates],
        response_format=WebsiteResponse,
    )
    
    result = await agent.do_async(task)
    return str(result.website) if result.website else ""


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Find a company's official website using Upsonic reasoning.")
    parser.add_argument("--company", required=True, help="Company name, e.g. 'OpenAI'")
    args = parser.parse_args()

    # Create the reasoning task
    task = Task(
        description=f"""
        Use the 'get_company_candidates' tool to find potential websites for {args.company}.
        Evaluate which URL is most likely the company's *official website* by reasoning about:
        - Domain name similarity to the brand
        - Presence of the brand or company name in the URL
        - Likelihood that it's not a social or news site
        Return the best website with reasoning and confidence.
        """,
        tools=[get_company_candidates],
        response_format=WebsiteResponse,
    )

    # Let the Upsonic Agent handle reasoning and output generation
    result = agent.do(task)
    print(json.dumps(result.model_dump(), indent=2))
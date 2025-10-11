import os
import sys
import requests
from typing import List
from pydantic import BaseModel
from dotenv import load_dotenv

# --- Config ---
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
load_dotenv()
SERPER_API_KEY = os.getenv("SERPER_API_KEY")
if not SERPER_API_KEY:
    raise ValueError("SERPER_API_KEY missing in .env file.")

SERPER_SCRAPE = "https://google.serper.dev/scrape"
HEADERS = {"X-API-KEY": SERPER_API_KEY, "Content-Type": "application/json"}


# --- Pydantic Models ---
class AgreementLink(BaseModel):
    url: str
    is_available: bool
    is_agreement_page: bool


class AgreementLinksResponse(BaseModel):
    company_name: str
    website: str
    agreements: List[AgreementLink]


# --- Single Tool: Website Scraping ---
def website_scraping(url: str) -> dict:
    """
    Scrape a webpage via Serper /scrape endpoint.

    Args:
        url: The URL to scrape (can be a Google search page or any website)

    Returns:
        A dictionary with:
        - url: The scraped URL
        - content: The text content of the page
        - links: A list of links found on the page
    """
    try:
        resp = requests.post(
            SERPER_SCRAPE,
            headers=HEADERS,
            json={"url": url},
            timeout=40
        )
        resp.raise_for_status()
        data = resp.json()
        return {
            "url": url,
            "content": data.get("text", ""),
            "links": data.get("links", [])
        }
    except Exception as e:
        return {
            "url": url,
            "content": f"Error scraping: {str(e)}",
            "links": []
        }


# --- Main Execution ---
if __name__ == "__main__":
    import argparse
    from upsonic import Agent, Task

    parser = argparse.ArgumentParser(
        description="Find agreement/policy links for a company using only LLM reasoning."
    )
    parser.add_argument(
        "--website",
        required=True,
        help="Company website URL (e.g., 'https://www.nike.com')"
    )
    args = parser.parse_args()

    website = args.website.strip().rstrip("/")
    # Extract company name from domain for display
    from urllib.parse import urlparse
    domain = urlparse(website).netloc.replace("www.", "")
    company_name = domain.split(".")[0].title()

    print(f"\n🚀 Running Agreement Links Finder for: {website}\n")

    # --- Task Prompt: All logic is handled by the LLM ---
    task_prompt = f"""
You are a web exploration agent. Your task is to find agreement/policy pages on {website}.

TOOL AVAILABLE:
- website_scraping(url) → returns {{"url": str, "content": str, "links": [str, ...]}}

YOUR WORKFLOW (MANDATORY STEPS):

STEP 1: Scrape the homepage
→ Call website_scraping("{website}")
→ You'll receive a dictionary with "links" array

STEP 2: Search through the links array
→ Look for URLs containing: "privacy", "terms", "policy", "legal", "cookie", "return", "shipping"
→ Identify at least 3-5 candidate URLs

STEP 3: Verify EACH candidate URL
→ For EACH promising URL, call website_scraping(candidate_url)
→ Check if the content contains policy/legal text
→ Keep a list of verified policy pages

STEP 4: If you find fewer than 2 policies
→ Look for additional links (e.g., "/legal", "/policies", "/help")
→ Try common policy URLs like: "{website}/privacy-policy" or "{website}/terms"
→ Scrape and verify those too

STEP 5: Return your findings
→ Only include URLs you actually scraped and confirmed contain policy content

---

EXAMPLE WORKFLOW:

Call 1: website_scraping("{website}")
→ Response shows links array with 50+ links
→ You spot: "/privacy-policy", "/terms-of-use", "/cookie-policy"

Call 2: website_scraping("{website}/privacy-policy")
→ Content contains "Privacy Policy... we collect data..."
→ VERIFIED ✓ Add to results

Call 3: website_scraping("{website}/terms-of-use")  
→ Content contains "Terms of Service... by using..."
→ VERIFIED ✓ Add to results

Call 4: website_scraping("{website}/cookie-policy")
→ Content contains "Cookie Policy... we use cookies..."
→ VERIFIED ✓ Add to results

Return: 3 verified policy URLs

---

CRITICAL RULES:

🚨 You MUST make at least 5-8 tool calls (explore multiple links)
🚨 Do NOT return a result until you've verified at least 2-3 policy pages
🚨 Do NOT skip verification - always scrape each candidate URL
🚨 Do NOT make up URLs - only use discovered links or standard patterns
🚨 If first attempt fails, try alternative approaches (search footer links, try common paths)

---

EXPECTED OUTPUT JSON:

{{
  "company_name": "{company_name}",
  "website": "{website}",
  "agreements": [
    {{"url": "verified_url_1", "is_available": true, "is_agreement_page": true}},
    {{"url": "verified_url_2", "is_available": true, "is_agreement_page": true}}
  ]
}}

---

BEGIN EXPLORATION:
Start by calling website_scraping("{website}") and begin your multi-step exploration process.
Do not stop until you've found and verified at least 2 policy pages.
"""

    # --- Create Agent and Task ---
    agent = Agent(name="agreement_finder_agent")
    task = Task(
        description=task_prompt.strip(),
        tools=[website_scraping],
        response_format=AgreementLinksResponse,
    )

    # --- Execute: Let the LLM handle all reasoning ---
    print("🤖 Agent is working...\n")
    result = agent.do(task)

    # --- Display Results ---
    print("\n" + "=" * 70)
    print("📋 AGREEMENT LINKS RESULT")
    print("=" * 70)
    print(f"\nCompany:  {result.company_name}")
    print(f"Website:  {result.website}")
    print(f"\nAgreements found: {len(result.agreements)}\n")

    if result.agreements:
        for i, link in enumerate(result.agreements, 1):
            print(f"{i}. {link.url}")
            print(f"   ✓ Available: {link.is_available}")
            print(f"   ✓ Is Agreement Page: {link.is_agreement_page}\n")
    else:
        print("No agreement/policy links found.\n")

    print("=" * 70)

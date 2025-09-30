# task_examples/find_company_website/find_company_website.py

from pydantic import BaseModel, HttpUrl
from serper_client import search_company

class WebsiteResponse(BaseModel):
    company_name: str
    website: HttpUrl | None

def find_company_website(company_name: str) -> WebsiteResponse:
    results = search_company(company_name)
    website = None
    for r in results.get("organic", []):
        if "link" in r:
            website = r["link"]
            break
    return WebsiteResponse(company_name=company_name, website=website)

if __name__ == "__main__":
    company = "Upsonic Teknoloji"
    result = find_company_website(company)
    print("Company:", result.company_name)
    print("Website:", result.website)

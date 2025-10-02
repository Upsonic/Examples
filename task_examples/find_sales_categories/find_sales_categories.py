import sys, os, argparse
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from upsonic import Direct, Task
from task_examples.find_company_website.find_company_website import find_company_website
from task_examples.find_sales_categories.category_extractor import extract_categories

# Define a new agent
sales_category_agent = Direct(name="sales_category_agent")

# Define the orchestration function
def find_sales_categories(company_name: str) -> dict:
    """
    Given a company name, find its website and extract sales categories.
    """
    # Step 1: Use existing agent to find & validate website
    website_result = find_company_website(company_name)
    if not website_result.website:
        return {"website": "", "categories": [], "reason": website_result.reason}

    # Step 2: Extract categories from that website
    categories = extract_categories(str(website_result.website))
    
    return {
        "website": str(website_result.website), 
        "categories": categories,
        "validated": website_result.validated,
        "score": website_result.score
    }

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Find sales categories for a company")
    parser.add_argument("--company", required=True, help="Company name, e.g. 'Nike'")
    args = parser.parse_args()

    # Create a task
    task = Task(
        description=f"Find website and extract sales categories for {args.company}",
        tools=[find_company_website, extract_categories],
        agent=sales_category_agent
    )
    
    # Execute the task
    result = sales_category_agent.do(task)
    print(f"\nResult for {args.company}: {result}")

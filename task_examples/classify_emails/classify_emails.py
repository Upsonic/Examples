from pydantic import BaseModel
from upsonic import Agent, Task

# --- Example Emails -----------------------------------------------------------

email_1 = """
Dear Operations Team,

We are requesting detailed account statements for the last six months regarding the following customer.
Please include all transaction records, account balance history, and any associated documents.

This request is made in accordance with the Financial Supervision Act.
Sincerely,
Ministry of Finance - Audit Department
"""

email_2 = """
To Whom It May Concern,

Please be advised that a lien has been placed on the following bank account pursuant to the court order No. 2025/482.
All transactions from this account should be temporarily frozen until further notice.

Best regards,
Tax Collection Office
"""

# --- Response Model -----------------------------------------------------------

class ClassificationResult(BaseModel):
    category: str  # "information_request" or "lien_on_bank_account"


# --- Agent Setup --------------------------------------------------------------

classification_agent = Agent(name="email_classification_agent")


# --- CLI + Task Definition ----------------------------------------------------

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Classify incoming fintech operation emails.")
    parser.add_argument(
        "--email_id",
        type=int,
        default=1,
        help="Email number to classify (1 or 2)"
    )
    args = parser.parse_args()

    selected_email = email_1 if args.email_id == 1 else email_2

    # Prompt (LLM does all reasoning)
    task_prompt = f"""
You are an intelligent email classification agent working for a fintech company's operations department.

Your task is to classify the following email into one of two categories:
1. information_request — The sender requests account data, statements, or other informational documents.
2. lien_on_bank_account — The sender notifies about a lien, freeze, or legal restriction on a bank account.

Email content:
---
{selected_email}
---

Guidelines:
- If the email includes terms like "provide account information", "requesting data", "audit", "statements", "supervision" → classify as "information_request".
- If it mentions "lien", "freeze", "court order", "funds held", or "blocked account" → classify as "lien_on_bank_account".
- Return the result as a JSON object with field `category` and value either "information_request" or "lien_on_bank_account".
    """

    task = Task(
        description=task_prompt.strip(),
        response_format=ClassificationResult,
    )

    result = classification_agent.do(task)
    print("\n" + "=" * 60)
    print("📧 EMAIL CLASSIFICATION RESULT")
    print("=" * 60)
    print(result.model_dump_json(indent=2))
    print("=" * 60)

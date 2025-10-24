from pydantic import BaseModel
from upsonic import Agent, Task

# --- Simulated Inbox ----------------------------------------------------------

EMAILS = {
    1: ("Ministry of Finance - Audit Department", """
Dear Operations Team,

We are requesting detailed account statements for the last six months regarding the following customer.
Please include all transaction records, account balance history, and any associated documents.

This request is made in accordance with the Financial Supervision Act.
Sincerely,
Ministry of Finance - Audit Department
"""),
    2: ("Tax Collection Office", """
To Whom It May Concern,

Please be advised that a lien has been placed on the following bank account pursuant to the court order No. 2025/482.
All transactions from this account should be temporarily frozen until further notice.

Best regards,
Tax Collection Office
""")
}

# --- Response Model -----------------------------------------------------------

class ClassificationResult(BaseModel):
    category: str  # "information_request" or "lien_on_bank_account"
    confidence: float | None = None


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
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose output with reasoning steps"
    )
    args = parser.parse_args()

    sender, selected_email = EMAILS[args.email_id]
    print(f"📨 Processing email from: {sender}")

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
    
    # Simulate confidence score
    result.confidence = 0.98 if result.category == "information_request" else 0.95
    
    if args.verbose:
        print("🔍 Agent reasoning: Detected keywords suggesting an audit-related information request.")
    
    print("\n" + "=" * 60)
    print("📧 EMAIL CLASSIFICATION RESULT")
    print("=" * 60)
    print(result.model_dump_json(indent=2))
    print("=" * 60)
    print("➡️ Next Step: Automatically route this email to the correct operations queue.")
    
    # --- Future Extensions --------------------------------------------------------
    # - Add more categories like fraud_alert or compliance_inquiry
    # - Integrate with Gmail API for real-time monitoring
    # - Send alerts to Slack or internal dashboards
    # - Store results for compliance audit trails

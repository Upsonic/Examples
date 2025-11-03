"""
Upsonic Email Classification Agent Demo (Two-File Version)
-----------------------------------------------------------
"""

from typing import Any
from pydantic import BaseModel
from upsonic import Agent, Task
from rich.console import Console
from email_samples import EMAILS
import argparse

console = Console()



# --- Response Model -----------------------------------------------------------

class ClassificationResult(BaseModel):
    category: str
    confidence: float | None = None
    explanation: str | None = None
    routing: str | None = None




# --- Core Logic ---------------------------------------------------------------

def classify_email(email_id: int, verbose: bool = False) -> ClassificationResult:
    sender, email_text = EMAILS[email_id]
    console.print(f"\n📨 [bold cyan]Processing email from:[/bold cyan] {sender}")

    system_prompt = """
    You are a fintech operations assistant specializing in email classification and routing.
    
    Analyze the email content and classify it into one of these categories:
    1. information_request - Requests for data, statements, audits, or clarifications
    2. lien_on_bank_account - Legal notices about account freezes, liens, court orders, or injunctions
    3. fraud_investigation - Reports of suspicious activity, unauthorized transactions, or fraud cases
    4. kyc_update - Customer verification requests, identity documents, or compliance updates
    5. compliance_notice - Regulatory reports, transparency requirements, or authority submissions
    
    For each classification, determine the appropriate routing:
    - information_request → "📬 → Routed to Data Operations Queue"
    - lien_on_bank_account → "⚖️ → Escalated to Legal Department"
    - fraud_investigation → "🚨 → Sent to Fraud Prevention Unit"
    - kyc_update → "🧾 → Forwarded to Compliance Team"
    - compliance_notice → "📑 → Logged under Regulatory Reports"
    
    Consider the context, tone, and specific language used in the email.
    Provide your reasoning and assign a confidence score (0.0-1.0).
    
    Output JSON with category, confidence, explanation, and routing.
    """
    task_prompt = f"{system_prompt.strip()}\n\nEmail:\n---\n{email_text}\n---"

    agent = Agent(name="email_classification_agent")
    task = Task(description=task_prompt, response_format=ClassificationResult)
    result = agent.do(task)

    if not result.confidence:
        result.confidence = 0.92

    if verbose:
        console.print(f"\n🔍 [bold yellow]Reasoning:[/bold yellow]\n{result.explanation or 'N/A'}")

    return result


# --- CLI ----------------------------------------------------------------------

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Classify fintech operation emails.")
    parser.add_argument("--email_id", type=int, help="Email ID to classify (1–8). If omitted, runs all emails.")
    parser.add_argument("--verbose", action="store_true", help="Show reasoning output for each email.")
    args = parser.parse_args()

    # If no email_id given → run all
    if args.email_id is None:
        console.print("[bold cyan]\n📬 Running classification for all emails in inbox...[/bold cyan]")
        summary_counts = {}

        for email_id, (sender, _) in EMAILS.items():
            result = classify_email(email_id, verbose=args.verbose)
            summary_counts[result.category] = summary_counts.get(result.category, 0) + 1

            console.print("\n" + "=" * 60)
            console.print(f"[bold white]📧 EMAIL {email_id} RESULT[/bold white]")
            console.print("=" * 60)
            console.print(result.model_dump_json(indent=2), style="bold green")
            console.print("=" * 60)
            console.print(result.routing or "📂 → Sent to General Inbox")
            console.print()

        console.print("[bold cyan]\n📊 SUMMARY[/bold cyan]")
        for cat, count in summary_counts.items():
            console.print(f"• {cat}: {count} email(s)")
        console.print()
    else:
        # Run single email
        result = classify_email(args.email_id, verbose=args.verbose)

        console.print("\n" + "=" * 60)
        console.print("[bold white]📧 EMAIL CLASSIFICATION RESULT[/bold white]")
        console.print("=" * 60)
        console.print(result.model_dump_json(indent=2), style="bold green")
        console.print("=" * 60)
        console.print(result.routing or "📂 → Sent to General Inbox")
        console.print()

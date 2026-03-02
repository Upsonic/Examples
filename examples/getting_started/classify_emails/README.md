# Classify Emails

This example demonstrates how to build a lightweight **Upsonic LLM agent** that classifies incoming fintech operation emails into specific categories — helping operations teams automatically sort and respond to critical messages.

## Overview

In this example, the agent classifies emails into one of two categories:

1. **Information Requests** — messages requesting data such as account statements, balance history, or audit documents.
2. **Lien on Bank Account** — notifications indicating a lien, freeze, or court order on a customer account.

The agent uses a single LLM Task to perform the classification.  
There are no external integrations — just intelligent reasoning based on email content.

---

## Setup

### 1. Install dependencies

```bash
uv sync
```

### 2. Configure OpenAI API Key

Set your OpenAI API key as an environment variable:

```bash
export OPENAI_API_KEY="your_openai_api_key_here"
```

Or create a `.env` file in the project root:

```bash
echo "OPENAI_API_KEY=your_openai_api_key_here" > .env
```

---

## Run the Agent

### Example Emails

Two sample emails are included in the script:

- **Email 1**: A government audit request for account information.
- **Email 2**: A tax authority notification about a lien on a bank account.

### Run the classifier

```bash
# Classify Email 1 (Information Request)
uv run task_examples/classify_emails/classify_emails.py --email_id 1

# Classify Email 2 (Lien on Bank Account)
uv run task_examples/classify_emails/classify_emails.py --email_id 2

# Run with verbose output (shows reasoning steps)
uv run task_examples/classify_emails/classify_emails.py --email_id 1 --verbose
```

### Example Output

**Email 1:**

```
📨 Processing email from: Ministry of Finance - Audit Department

============================================================
📧 EMAIL CLASSIFICATION RESULT
============================================================
{
  "category": "information_request",
  "confidence": 0.98
}
============================================================
➡️ Next Step: Automatically route this email to the correct operations queue.
```

**Email 2:**

```
📨 Processing email from: Tax Collection Office

============================================================
📧 EMAIL CLASSIFICATION RESULT
============================================================
{
  "category": "lien_on_bank_account",
  "confidence": 0.95
}
============================================================
➡️ Next Step: Automatically route this email to the correct operations queue.
```

---

## How It Works

1. **Input**: The LLM receives the text of the email.
2. **Reasoning**: The agent analyzes the content and context — e.g., requests vs. legal notifications.
3. **Output**: Returns a structured JSON object with a single field:
   - `category`: `"information_request"` or `"lien_on_bank_account"`

---

## File Structure

```bash
task_examples/classify_emails/
├── classify_emails.py      # Main LLM classification agent
└── README.md               # This file
```

---

## Notes

- **Fully autonomous**: The LLM performs all reasoning — no manual logic or regex.
- **Minimal architecture**: One Task, one prompt, one result.
- **Extendable**: Easily add new categories or integrate with a real email inbox later.
- **Use case**: Ideal for fintech operations or compliance departments managing high email volume.

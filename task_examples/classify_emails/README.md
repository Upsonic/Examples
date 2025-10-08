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
```

### Example Output

**Email 1:**

```json
{
  "category": "information_request"
}
```

**Email 2:**

```json
{
  "category": "lien_on_bank_account"
}
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

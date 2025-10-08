# Find Agreement Links

This example demonstrates how to build an **Upsonic LLM agent** that can autonomously find and verify agreement or policy pages on a company's ecommerce website — such as Privacy Policy, Terms of Use, or Cookie Policy — using the Serper API for scraping and LLM reasoning for exploration and validation.

## Overview

In this task, the agent:

1. **Finds** the official company website using the `find_company_website` agent.
2. **Explores** the website intelligently using a single `website_scraping` tool powered by Serper.
3. **Identifies** links that are likely related to agreements or policies (e.g., privacy, terms, refund, cookie, legal).
4. **Follows** those links autonomously and determines whether each page is a valid agreement or policy document.
5. **Returns** structured results, including link availability and verification.

Unlike traditional scripts, this task delegates all exploration and reasoning to the LLM agent — keeping the implementation lightweight and adaptable.

---

## Setup

### 1. Install dependencies

```bash
uv sync
```

### 2. Add your Serper API key

Copy `.env.example` to `.env`:

```bash
cp .env.example .env
```

Then edit `.env` and add your key:

```ini
SERPER_API_KEY=your_serper_api_key_here
```

Get a free API key at [https://serper.dev](https://serper.dev).

---

## Run the Agent

Run the agent with any company name:

```bash
uv run task_examples/find_agreement_links/find_agreement_links.py --company "Nike"
```

**Example output:**

```json
{
  "company_name": "Nike",
  "website": "https://www.nike.com/",
  "agreements": [
    {
      "url": "https://www.nike.com/legal/privacy-policy",
      "is_available": true,
      "is_agreement_page": true
    },
    {
      "url": "https://www.nike.com/legal/terms-of-use",
      "is_available": true,
      "is_agreement_page": true
    }
  ]
}
```

Try with other companies:

```bash
uv run task_examples/find_agreement_links/find_agreement_links.py --company "Adidas"
uv run task_examples/find_agreement_links/find_agreement_links.py --company "Mavi"
uv run task_examples/find_agreement_links/find_agreement_links.py --company "Zara"
```

---

## How It Works

### 1. Website Discovery

- The LLM uses `find_company_website` to locate the company's official homepage.

### 2. Intelligent Exploration

- The agent uses the `website_scraping` tool (Serper API) to analyze the main site content.
- It identifies subpages likely to contain legal or policy-related text (privacy, terms, legal, gdpr, etc.).
- It autonomously follows these links and checks accessibility.

### 3. Agreement Verification

- The LLM determines whether each reachable page is an agreement/policy page based on textual context (mentions of user data, consent, cookies, terms, etc.).
- Results are returned as structured Pydantic models.

---

## File Structure

```bash
task_examples/find_agreement_links/
├── find_agreement_links.py      # Main LLM agent script
└── README.md                    # This file

.env.example                     # Example environment file (root)
```

---

## Notes

- **Lightweight architecture**: The entire process is handled within one Task; Python only defines the tools.
- **Serper-based scraping**: Uses Serper's API to fetch and parse rendered web content.
- **No hardcoded logic**: The LLM autonomously explores and verifies.
- **Structured output**: Type-safe Pydantic schema (`AgreementLinksResponse`).

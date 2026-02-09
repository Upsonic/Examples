# Find Sales Categories

This example demonstrates how to build an Upsonic agent that discovers a company's official ecommerce site and summarises its top-level shopping categories (e.g. Men, Women, Electronics, Sale). It reuses the `find_company_website` agent, scrapes navigation menus, and lets an LLM refine the final category list.

## What the example does

- Finds the company's official website with Upsonic tools.
- Scrapes navigation menus for potential sales labels.
- Asks an LLM to keep only the genuine shopping departments and returns a clean JSON list.

---

## Prerequisites

1. Install dependencies:
   ```bash
   uv sync
   ```
2. Add your Serper API key (the website finder relies on it):
   ```bash
   cp .env.example .env
   ```

   Edit `.env` and set `SERPER_API_KEY` (see [Serper.dev](https://serper.dev/)).

---

## Running the agent

Single company:

```bash
uv run task_examples/find_sales_categories/find_sales_categories.py --company "Nike"
```

Batch of companies (comma-separated):

```bash
uv run task_examples/find_sales_categories/find_sales_categories.py --companies "Nike, Lululemon, Apple"
```

Batch runs save a combined JSON report to `outputs/sales_categories.json`.

### Example result (single company)

```json
{
  "company": "Nike",
  "website": "https://www.nike.com/",
  "categories": [
    "Men",
    "Women",
    "Kids",
    "Shoes",
    "Clothing",
    "Accessories",
    "Training",
    "Sale"
  ],
  "reason": "The domain 'nike.com' directly matches the brand name and is the official ecommerce presence."
}
```

The `categories` field is always a plain JSON list (no Markdown code fences).

---

## How it works

1. **Website finder wrapper** calls the existing `find_company_website` agent and returns a structured `WebsiteResponse`.
2. **`extract_categories` tool** scrapes navigation/menu DOM nodes for candidate labels, filtering obvious non-product links.
3. **LLM normalisation** instructs the agent to keep only the main departments and outputs a clean list.
4. **Batch CLI** loops over companies and collects results (writing a report when multiple companies are provided).

---

## Files

```bash
task_examples/find_sales_categories/
├── find_sales_categories.py   # Orchestrates website finding, scraping, LLM refinement, CLI
├── category_extractor.py      # Stand-alone scraping tool (legacy/minimal variant)
└── README.md                  # This guide
```

> ℹ️ The example depends on the `find_company_website` task. Ensure its instructions and `.env` configuration are completed first.

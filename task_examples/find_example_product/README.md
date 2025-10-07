# Find Example Product

This example demonstrates how to build **Upsonic LLM agents** that can autonomously explore ecommerce websites and extract structured product data — powered by the Serper API for web scraping and LLM-driven reasoning for navigation.

## Overview

In this task, the agent:

1. **Finds** the official website of a company using the `find_company_website` agent.
2. **Explores** the site intelligently using a `website_scraping` tool (Serper API).
3. **Extracts** structured product information — including name, price, brand, availability, and URL — from one of the product pages.

Unlike static scrapers, this agent uses **LLM reasoning** to decide which pages to explore and when to retry.

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

Edit `.env` and add your Serper API key:

```ini
SERPER_API_KEY=your_serper_api_key_here
```

You can get a free API key at [https://serper.dev](https://serper.dev).

---

## Run the Agent

Run the agent with any company name:

```bash
uv run task_examples/find_example_product/find_example_product.py --company "Mavi"
```

**Example output:**

```json
{
  "product_name": "STEVE ATHLETIC FIT JEANS IN DARK INK SUPERMOVE",
  "product_price": "$128.00",
  "product_brand": "Mavi",
  "availability": "In Stock",
  "url": "https://us.mavi.com/products/steve-dark-ink-supermove"
}
```

Try it with other companies:

```bash
uv run task_examples/find_example_product/find_example_product.py --company "Nike"
uv run task_examples/find_example_product/find_example_product.py --company "Adidas"
uv run task_examples/find_example_product/find_example_product.py --company "Apple"
```

---

## How It Works

### 1. Website Discovery

- Uses the existing `find_company_website` agent to find and validate the company's homepage.

### 2. Intelligent Exploration

- Uses the `website_scraping` tool (Serper API) to fetch website content.
- The LLM agent reads the scraped text, identifies relevant sublinks, and autonomously decides which pages to follow.
- It may retry multiple times until it finds a valid product page.

### 3. Product Extraction

The agent extracts:
- `product_name`
- `product_price`
- `product_brand`
- `availability`
- `url`

Returns structured output in the Pydantic `ProductInfo` format.

---

## File Structure

```bash
task_examples/find_example_product/
├── find_example_product.py      # Main LLM agent
└── README.md                    # This file

.env.example                     # Example environment file (root)
```

---

## Notes

- **Serper-based scraping**: Uses Serper's scraping API to fetch rendered web content.
- **No path restrictions** — the LLM decides where to explore.
- **Single Task architecture**: Website discovery → exploration → extraction all occur in one task.
- **Type-safe results**: Structured `ProductInfo` output validated by Pydantic.
- Requires the `find_company_website` example to work properly.

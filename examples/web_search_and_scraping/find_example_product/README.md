# Find Example Product

This example demonstrates how to build **Upsonic LLM agents** that autonomously explore ecommerce websites and extract structured product data — powered by the Serper API for web scraping and LLM-driven reasoning for intelligent navigation.

## Overview

In this task, the agent:

1. **Finds** the official website of a company using the `find_company_website` agent.
2. **Explores** the site intelligently using a `website_scraping` tool (Serper API).
3. **Extracts** structured product information — including name, price, brand, availability, and URL — from one of the product pages.

Unlike traditional scrapers, this agent uses **LLM reasoning** to decide which pages to explore, how to navigate the site, and when to retry.

---

## Setup

### 1. Install dependencies

```bash
uv sync
```

### 2. Configure your Serper API key

Copy `.env.example` to `.env`:

```bash
cp .env.example .env
```

Then edit `.env` and add your API key:

```ini
SERPER_API_KEY=your_serper_api_key_here
```

You can get a free key from [https://serper.dev](https://serper.dev).

---

## Run the Agent

Run the agent for any company name:

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

- Uses `find_company_website` to locate and validate the company's official homepage.

### 2. Intelligent Exploration

- The LLM agent uses the `website_scraping` tool (Serper API) to fetch page content.
- It identifies product-related sublinks such as `/shop`, `/products`, `/collections`, etc.
- It navigates autonomously through relevant subpages until it finds a valid product.

### 3. Product Extraction

Once a product page is found, the LLM extracts:
- `product_name`
- `product_price`
- `product_brand`
- `availability`
- `url`

The extracted data is returned in a validated `ProductInfo` Pydantic model.

---

## File Structure

```bash
task_examples/find_example_product/
├── find_example_product.py      # Main LLM agent script
└── README.md                    # This file

.env.example                     # Example environment file (root)
```

---

## Notes

- **No custom scraping** — all content retrieval uses Serper's API.
- **No path or subdomain restrictions** — the LLM determines navigation dynamically.
- **Unified Task design**: website discovery → exploration → extraction handled within one Task object.
- **Type-safe output** using the Pydantic `ProductInfo` model.
- Requires the `find_company_website` example for website lookup.

# Firecrawl Shopping Scraper

A product extraction agent built with the **Upsonic AI Agent Framework** and **FirecrawlTools**. Point it at any shopping website and it scrapes the page, extracts product names, prices, and descriptions, and returns the results as a clean, sorted table.

The example targets [books.toscrape.com](http://books.toscrape.com), a publicly available scraping-safe demo bookstore, but the same pattern works for any publicly accessible e-commerce site.

## Features

- **Single-page scraping**: Fetches a shop page and converts it to clean Markdown via Firecrawl
- **LLM-powered extraction**: The agent reads the Markdown and pulls out structured product data without custom parsers or CSS selectors
- **Minimal tool surface**: Only `scrape_url` is enabled so the agent cannot accidentally crawl, search, or batch-scrape
- **Sorted output**: Products are returned as a Markdown table ordered by price descending, with a summary line showing total count and price range
- **Extensible**: Switch to `crawl_website` for multi-page crawling or `extract_data` for schema-driven JSON extraction

## Prerequisites

- Python 3.10+
- Firecrawl API key (sign up for free at [firecrawl.dev](https://firecrawl.dev))
- Anthropic API key (or swap the model for any Upsonic-supported provider)

## Installation

1. Navigate to this directory:

   ```bash
   cd examples/firecrawl_shopping_scraper
   ```

2. Create and activate a virtual environment:

   ```bash
   # With uv (recommended)
   uv venv && source .venv/bin/activate

   # With pip
   python3 -m venv .venv && source .venv/bin/activate
   ```

3. Install dependencies:

   ```bash
   # With uv
   uv pip install -r requirements.txt

   # With pip
   pip install -r requirements.txt
   ```

4. Set up your environment variables:

   ```bash
   cp .env.example .env
   ```

   Then open `.env` and fill in your keys:

   ```bash
   FIRECRAWL_API_KEY=fc-your-key-here
   ANTHROPIC_API_KEY=your-anthropic-key-here
   ```

## Usage

Run the agent:

```bash
python main.py
# or
uv run main.py
```

Example output:

```
Found 20 products · Price range: £10.00 - £59.69

| #  | Book Title                                   | Price  | Rating |
|----|----------------------------------------------|--------|--------|
| 1  | Libertarianism for Beginners                 | £59.69 | Two    |
| 2  | It's Only the Himalayas                      | £52.29 | Two    |
| 3  | The Black Maria                              | £52.15 | One    |
| 4  | Starving Hearts (Triangular Trade Trilogy...) | £13.99 | Two    |
...
```

To target a different shop, change the URL in the task description inside `main.py`:

```python
task = Task(
    description="""
    Scrape https://your-target-shop.com and extract all visible products.
    For each product return name, price, and a short description (1-2 sentences).
    Format as a Markdown table sorted by price descending.
    """
)
```

## Project Structure

```
firecrawl_shopping_scraper/
├── main.py          # Agent setup and task definition
├── requirements.txt # Python dependencies
├── .env.example     # Environment variable template
└── README.md        # This file
```

## How It Works

1. **FirecrawlTools is configured** with only `scrape_url` enabled. This keeps the agent focused and prevents it from issuing unnecessary crawl or search calls.

2. **The task description** tells the agent what page to scrape and exactly what to extract. No custom parser is needed; the LLM reads the Markdown Firecrawl returns and identifies product blocks by structure and context.

3. **Firecrawl fetches the page** and returns it as clean Markdown, stripping navigation, ads, and boilerplate so the LLM gets a compact, structured representation of the content.

4. **The agent extracts and formats** each product row into a Markdown table, sorts by price descending, and prepends a summary line.

### Extending the example

To crawl multiple pages instead of just the homepage, enable `crawl_website`:

```python
firecrawl = FirecrawlTools(
    enable_scrape=False,
    enable_crawl=True,
    enable_crawl_management=True,
)

task = Task(
    description="""
    Crawl http://books.toscrape.com up to 5 pages and extract every product:
    name, price, and rating. Return a single Markdown table sorted by price descending.
    """
)
```

To get structured JSON output directly from Firecrawl's LLM extraction layer, enable `extract_data`:

```python
firecrawl = FirecrawlTools(
    enable_scrape=False,
    enable_extract=True,
)

task = Task(
    description="""
    Use extract_data on http://books.toscrape.com/* with this schema:
    {"products": [{"name": "string", "price": "string", "rating": "string"}]}
    Return the raw result.
    """
)
```

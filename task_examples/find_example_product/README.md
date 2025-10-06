# Find Example Product

This example shows how to build **Upsonic LLM agents** that can:

1. **Find** the official website of a company using the Serper API.
2. **Discover** product pages on that website by analyzing site structure.
3. **Extract** structured product information including name, price, brand, and availability.

---

## Setup

1. Install dependencies:

```bash
uv sync
```

2. Copy `.env.example` to `.env` and add your Serper API key:

```bash
cp .env.example .env
```

3. Edit `.env` and replace the placeholder with your real key:

```ini
SERPER_API_KEY=your_api_key_here
```

You can get a free API key at https://serper.dev.

## Find an Example Product

Run the finder agent with a company name:

```bash
uv run python task_examples/find_example_product/find_example_product.py --company "Mavi"
```

**Example output:**

```json
{
  "product_name": "STEVE ATHLETIC FIT JEANS IN DARK INK SUPERMOVE",
  "product_price": "USD 128.0",
  "product_brand": "Mavi",
  "availability": "In Stock"
}
```

Try with other companies:

```bash
uv run python task_examples/find_example_product/find_example_product.py --company "Nike"
uv run python task_examples/find_example_product/find_example_product.py --company "Adidas"
```

## How It Works

The flow is split into reusable components:

### Website Finder
- Uses the `find_company_website` agent to locate the official website.
- Validates candidate websites and returns the best match.

### Product Discovery
- Scrapes the homepage to find product-like links.
- Tries common ecommerce paths (`/products`, `/collections`, etc.).
- Ranks candidates by relevance and depth.

### Product Extraction
- Scrapes the product page HTML.
- Extracts structured data using JSON-LD, meta tags, and CSS selectors.
- Handles multiple fallback strategies for robust extraction.

## File Structure

```bash
task_examples/find_example_product/
├── find_example_product.py    # Main agent script
├── config.py                  # Configuration (unused)
└── README.md                  # This file

# Root directory
.env.example                   # Example env file for API keys (in root)
```

## Notes

- **Robust extraction**: Uses multiple fallback strategies (JSON-LD, meta tags, CSS selectors) for reliable product data extraction.
- **Direct scraping**: Uses direct HTTP requests with proper browser headers instead of external scraping services.
- **Graceful degradation**: If specific fields cannot be extracted, they will be `null` in the output.
- **Dependencies**: Requires the `find_company_website` example for website discovery.

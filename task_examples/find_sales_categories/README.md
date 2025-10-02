# Find Sales Categories

This task example shows how to build an Upsonic LLM agent that:

- Reuses the `find_company_website` agent to find and validate the official website of a company (via Serper API).
- Chains the result into the `extract_categories` tool to scrape ecommerce sales categories from that website.

## Setup

1. Install dependencies:

```bash
uv sync
```

2. Copy the example environment file and add your Serper API key:

```bash
cp .env.example .env
```

3. Edit `.env` and replace the placeholder with your key:

```ini
SERPER_API_KEY=your_api_key_here
```

You can get a free API key from [Serper.dev](https://serper.dev/).

## Run

Run the sales categories agent with any company name:

```bash
uv run task_examples/find_sales_categories/find_sales_categories.py --company "Nike"
```

**Example output:**

```
Result for Nike: The official website for Nike is [https://www.nike.com/](https://www.nike.com/).

The sales categories on Nike's website include:

- Men: Shoes, Clothing, Accessories
- Women: Bras, Leggings, Skirts & Dresses, Tops
- Kids: Big Kids, Little Kids, Baby & Toddler
- Sports: Basketball, Soccer, Running, Training, Golf
- Collections: Nike Air, Nike FlyEase, Nike React
- Sale: Discounted Shoes, Clothing, Accessories
```

You can replace "Nike" with any other company, e.g.:

```bash
uv run task_examples/find_sales_categories/find_sales_categories.py --company "Mavi"
uv run task_examples/find_sales_categories/find_sales_categories.py --company "Adidas"
```

## How It Works

The flow is split into two reusable components:

### Website Finder
- Uses Serper to search for the company.
- Validates candidate websites.
- Returns the best match as a structured `WebsiteResponse`.

### Category Extractor
- Fetches the website HTML.
- Looks for navigation and menu elements.
- Extracts category names, filtering out non-sales links.

### Sales Categories Agent
- Orchestrates the two steps above.
- **Input**: Company name.
- **Output**: JSON containing website, validation info, and extracted categories.

## File Structure

```bash
task_examples/find_sales_categories/
├── find_sales_categories.py    # Agent: orchestrates website finder + category extractor
├── category_extractor.py       # Tool: scrapes ecommerce categories
└── README.md                   # This file
```

## Note

This agent depends on the `find_company_website` example. Make sure you have its code and `.env` setup in place.

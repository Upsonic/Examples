# Find Sales Categories

Find company websites and extract sales categories from ecommerce websites using Serper API.

## Files
- `find_sales_categories.py` — Main script
- `README.md` — This file

## Setup
1. Get a free Serper API key from https://serper.dev/
2. Set environment variable:
```bash
export SERPER_API_KEY="your_serper_api_key_here"
```
3. Install dependencies:
```bash
uv sync
```

## Run
```bash
uv run task_examples/find_sales_categories/find_sales_categories.py
```

## Example Output
```
==================================================
Analyzing: Amazon
==================================================
Finding website for Amazon...
Found website: https://www.amazon.com/
Scraping website content...
Scraped 5257 characters
Found categories: Accessories, Beauty, Books, Clothing, Decor, Electronics, Fashion, Fitness, Games, Health, Home, Jewelry, Kids, Kitchen, Makeup, Men, Outdoor, Pets, Shoes, Skincare, Toys, Women
Website: https://www.amazon.com/
Categories: Accessories, Beauty, Books, Clothing, Decor, Electronics, Fashion, Fitness, Games, Health, Home, Jewelry, Kids, Kitchen, Makeup, Men, Outdoor, Pets, Shoes, Skincare, Toys, Women
```

# Find Company Website (Upsonic Agent Example)

This example shows how to build **Upsonic LLM agents** that can:

1. **Find** the official website of a company using the Serper API.  
2. **Validate** whether a given website belongs to that company.

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

## 🔎 Find a Company Website

Run the finder agent with a company name:

```bash
uv run python task_examples/find_company_website/find_company_website.py --company "Amazon Inc"
```

**Example output:**

```json
{
  "company": "Amazon Inc",
  "website": "https://www.amazon.com/",
  "validated": true,
  "score": 0.9,
  "reason": "Brand in domain"
}
```

## Validate a Company Website

Run the validator agent with a company name and a URL:

```bash
uv run python task_examples/find_company_website/validate_company_website.py --company "Amazon Inc" --url "https://www.amazon.com/"
```

**Example output:**

```json
{
  "company": "Amazon Inc",
  "website": "https://www.amazon.com/",
  "validated": true,
  "score": 0.9,
  "reason": "Brand in domain"
}
```

## File Structure

```bash
task_examples/find_company_website/
├── find_company_website.py      # Agent: find websites
├── validate_company_website.py  # Agent: validate websites
├── serper_client.py             # Serper API client
├── html_utils.py                # HTML fetch + signals
└── README.md

# Root directory
.env.example                     # Example env file for API keys (in root)
```

## Notes

- **Finder**: takes a company name, searches with Serper, validates candidates, and returns the best match.
- **Validator**: checks if a given URL belongs to a company.
- Both use Upsonic agents. 

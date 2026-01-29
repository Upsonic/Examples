# Find Company Website (Upsonic Agent Demo)

This example demonstrates how to build an Upsonic LLM Agent that autonomously finds and validates a company's official website using reasoning and lightweight search tools.

The agent:

- Searches for potential websites using the Serper API.
- Reasons through results to identify the most credible domain.
- Validates the site based on brand–domain matching and context.
- Returns a structured, explainable JSON output.

## Setup

### Install dependencies

```bash
uv sync
```

### Set your Serper API key

Copy the example environment file and edit it:

```bash
cp .env.example .env
```

Then open `.env` and replace the placeholder with your real API key:

```ini
SERPER_API_KEY=your_api_key_here
```

You can get a free key at https://serper.dev.

## Run the Finder Agent

Run the reasoning-based agent to find a company's official website:

```bash
uv run task_examples/find_company_website/find_company_website.py --company "OpenAI"
```

**Example Output:**

```json
{
  "company": "OpenAI",
  "website": "https://openai.com/",
  "validated": true,
  "reasoning": "The domain 'openai.com' directly matches the company name 'OpenAI', indicating a strong likelihood that it is the official website.",
  "confidence": 0.95
}
```

## How It Works

- **Tool Layer** – A single function (`get_company_candidates`) queries Serper for candidate URLs.
- **Agent Layer** – The Upsonic agent performs reasoning, filtering out irrelevant sites and selecting the most official one.
- **Schema Layer** – Results are returned in a structured `WebsiteResponse` format (company, website, reasoning, confidence).

This structure demonstrates how Upsonic agents can mix retrieval, reasoning, and structured outputs in one clean workflow.

## File Structure

```
task_examples/find_company_website/
├── find_company_website.py       # Legacy finder (modular version)
└── README.md                     # This file

# Root directory
.env.example                      # Example environment config
```

## Notes

- The demo emphasizes agent reasoning, not manual rule-based filtering.
- You can easily extend the agent by adding tools (e.g., WHOIS checks, HTML analyzers).
- Ideal for showing how LLMs can autonomously use tools and justify their decisions.

# GPT-OSS Safety Agent Example with OpenRouter Provider

A simple example demonstrating OpenAI's `gpt-oss-safeguard-20b` model via OpenRouter provider with **PIIBlockPolicy** for detecting and blocking personally identifiable information.

## Prerequisites

Set your OpenRouter API key:
```bash
export OPENROUTER_API_KEY="your-api-key"
export OPENAI_API_KEY="your-api-key"
```

## Installation

Install dependencies from `upsonic_configs.json`:
```bash
upsonic install
```

### Managing Dependencies

Add a new package:
```bash
upsonic add <package> <section>
# Examples:
upsonic add requests api
upsonic add pandas==2.0.0 api
```

Remove a package:
```bash
upsonic remove <package> <section>
# Examples:
upsonic remove requests api
```

**Sections:** `api`, `streamlit`, `development`

## Run Options

### Option 1: Direct Script
```bash
uv run main.py
```
Runs built-in test cases (safe query + PII query).

### Option 2: FastAPI Server
```bash
upsonic run
```
Starts server at `http://localhost:8000` with Swagger docs at `/docs`.

**Example API call:**
```bash
curl -X POST http://localhost:8000/call \
  -H "Content-Type: application/json" \
  -d '{"user_query": "My email is john@example.com, can you help me with my account?"}'
```

## How It Works

- **Safe queries** → Normal AI response
- **Queries with PII (emails, phone numbers, etc.)** → Blocked with helpful feedback suggesting how to rephrase

## Key Files

| File | Purpose |
|------|---------|
| `main.py` | Agent with safety policy |
| `upsonic_configs.json` | Dependencies & API schema |

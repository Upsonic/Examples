# AI Governance Lexicon Agent

An educational AI agent built with the **Upsonic AI Agent Framework**. This example demonstrates how to use `Agent` with web search tools to research AI governance terms and provide structured educational content including detailed explanations and frequently asked questions.

## Features

- 🔍 **Automated Research**: Uses DuckDuckGo search to find authoritative definitions and context about AI governance terms
- 📚 **Educational Content**: Explains complex AI governance concepts in a detail-oriented but accessible way
- 🧠 **Structured Knowledge**: Returns a defined schema containing `brief_explanation` and a list of `faqs`
- 🛠️ **Tool Integration**: Demonstrates how to seamlessly integrate search tools into an Upsonic Agent
- 🏗️ **Modular Design**: Clean separation of concerns with specialized agent configuration, schemas, and tools

## Prerequisites

- Python 3.10+
- OpenAI API key

## Installation

1. **Navigate to this directory**:
   ```bash
   cd examples/ai_lexicon
   ```

2. **Install dependencies**:
   ```bash
   # Install all dependencies (API)
   upsonic install
   
   # Or install specific sections:
   upsonic install api          # API dependencies only (default)
   upsonic install development  # Development dependencies only
   ```

3. **Set up environment variables**:
   ```bash
   export OPENAI_API_KEY="your-api-key"
   ```

## Usage

### Run the API Server

To run the agent as a FastAPI server:

```bash
upsonic run
```

The API will be available at `http://localhost:8000` with automatic OpenAPI documentation at `http://localhost:8000/docs`.

OR

You can run the agent directly:

```bash
python3 main.py
```

**Example API Call:**
```bash
curl -X POST http://localhost:8000/call \
  -H "Content-Type: application/json" \
  -d '{
    "inputs": {
        "term": "Gap analysis for AI governance"
    }
  }'
```

## Project Structure

```
ai_lexicon/
├── main.py                    # Entry point with main() and amain() functions
├── upsonic_configs.json       # Upsonic configuration and dependencies
├── agent.py                   # Agent configuration and system prompts
├── tools.py                   # Search tool configuration
├── schemas.py                 # Pydantic output schemas
└── README.md                  # This file
```

## How It Works

1. **Agent Configuration**: The system initializes an `Agent` with a specialized system prompt designed for the role of an "AI Governance Lexicon Expert".

2. **Research**: When a term is provided, the agent uses the configured `duckduckgo_search_tool` to gather current, authoritative information from the web.

3. **Synthesis & Structuring**: The agent processes the research findings and synthesizes them into a clear explanation and relevant FAQs.

4. **Structured Output**: The response is enforced to match the `LexiconEntry` Pydantic model defined in `schemas.py`, ensuring consistent and machine-readable output.

## Example Queries

- "Gap analysis for AI governance"
- "Model interpretability techniques"
- "EU AI Act compliance requirements"
- "AI safety frameworks"

## Input Parameters

- `term` (required): The AI governance term to research and explain (e.g., "Gap analysis for AI governance")
- `model` (optional): Model identifier (default: "openai/gpt-4o")
- `max_search_results` (optional): Maximum number of search results to use for research (default: 10)

## Output

Returns a dictionary containing:
- `term`: The AI governance term being explained
- `brief_explanation`: A detailed but concise explanation of the term
- `faqs`: A list of objects containing:
  - `question`: A common question about the term
  - `answer`: A comprehensive answer to the question

The report is returned as a JSON-serializable dictionary with all findings structured according to the `LexiconEntry` schema.

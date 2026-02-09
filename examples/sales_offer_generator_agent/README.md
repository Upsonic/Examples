# Sales Offer Generator Agent

A Sales Offer Generator Agent built with the **Upsonic AI Agent Framework**. This example demonstrates how to use `DeepAgent` to analyze customer needs, search the internet for real products, develop pricing strategies, and generate personalized sales offers.

## Features

- 🌐 **Real-Time Market Research**: Uses DuckDuckGo to fetch live product data and prices
- 💰 **Strategic Pricing Analysis**: Analyzes competitor pricing to suggest competitive offers
- ✍️ **Personalized Copywriting**: Generates professional, persuasive sales emails tailored to customer needs
- 🤖 **DeepAgent Orchestration**: Automatically plans and coordinates sub-agents to fulfill complex goals
- 🏗️ **Modular Design**: Clean separation of concerns with specialized agents and tools

## Prerequisites

- Python 3.10+
- OpenAI API key

## Installation

1. **Navigate to this directory**:
   ```bash
   cd examples/sales_offer_generator_agent
   ```

2. **Install dependencies**:
   ```bash
   # Install all dependencies (API and development)
   upsonic install all
   
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
uv run main.py
```

**Example API Call:**
```bash
curl -X POST http://localhost:8000/call \
  -H "Content-Type: application/json" \
  -d '{"user_query": "I need a gaming laptop under $2000"}'
```

## Project Structure

```
sales_offer_generator_agent/
├── main.py                    # API agent workflow (FastAPI endpoint)
├── upsonic_configs.json       # Upsonic configuration and dependencies
├── agents.py                  # Agent Factory: Defines Researcher, Strategist, and Writer agents
├── tools.py                   # Tools: SearchTools using 'ddgs' for real-time data
├── .env.example               # Example enviroment file
└── README.md                  # Quick start guide
```

## How It Works

1.  **SearchTools**: A custom Toolkit using `ddgs` that allows agents to search the internet for product specifications and current prices.

2.  **SalesAgents**: A factory class that produces three specialized agents:
    *   **Product Researcher**: Finds real products matching criteria.
    *   **Pricing Strategist**: Analyzes market data to determine pricing.
    *   **Offer Writer**: Crafts the final message.

3.  **DeepAgent**: The core orchestrator. Instead of manually chaining tasks, `DeepAgent` takes a high-level goal ("Generate a sales offer...") and automatically:
    *   Creates a execution plan.
    *   Delegates tasks to the right specialists.
    *   Passes context (research results, strategies) between them.
    *   Delivers the final output.

## Example Queries

- "I need a high-performance laptop for video editing (4K workflows) and 3D rendering. Budget is around $3,000."
- "Find me a budget-friendly smartphone under $500 with a good camera."
- "Looking for ergonomic office chairs with lumbar support."

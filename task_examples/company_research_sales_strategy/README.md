# Company Research & Sales Strategy Agent

A comprehensive Company Research and Sales Strategy Agent built with the **Upsonic AI Agent Framework**. This example demonstrates how to use `DeepAgent` with specialized subagents to conduct deep company research, analyze industry trends, perform financial analysis, and develop tailored sales strategies.

## Features

- 🔍 **Comprehensive Company Research**: Deep analysis of target companies including business models, products, markets, and competitive positioning
- 📊 **Industry Analysis**: Market trends, competitive landscape, emerging technologies, and regulatory environment analysis
- 💹 **Financial Analysis**: Stock performance, fundamentals, analyst recommendations, and market sentiment using YFinance
- 🎯 **Sales Strategy Development**: Tailored sales strategies with target segments, value propositions, pricing, and messaging
- 🤖 **DeepAgent Orchestration**: Automatically plans and coordinates specialized sub-agents to fulfill complex research goals
- 🧠 **Persistent Memory**: SQLite-based memory for session persistence and conversation history
- 🏗️ **Modular Design**: Clean separation of concerns with specialized agents, schemas, and utilities

## Prerequisites

- Python 3.10+
- OpenAI API key
- (Optional) Tavily API key for enhanced search capabilities

## Installation

1. **Navigate to this directory**:
   ```bash
   cd examples/company_research_sales_strategy
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
   export TAVILY_API_KEY="your-tavily-key"  # Optional, falls back to DuckDuckGo
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
  -d '{
    "company_name": "Microsoft",
    "industry": "Artificial Intelligence",
    "company_symbol": null
  }'
```

## Project Structure

```
company_research_sales_strategy/
├── main.py                    # Entry point with async main() function
├── upsonic_configs.json       # Upsonic configuration and dependencies
├── orchestrator.py             # DeepAgent orchestrator creation
├── subagents.py               # Specialized subagent factory functions
├── schemas.py                 # Pydantic output schemas
├── task_builder.py           # Task description builder
└── README.md                  # This file
```

## How It Works

1. **Orchestrator Agent**: A `DeepAgent` that coordinates the entire research and strategy development process using planning tools and subagent delegation.

2. **Specialized Subagents**: Four domain experts that handle specific research areas:
   - **Company Researcher**: Gathers comprehensive company information using web search
   - **Industry Analyst**: Analyzes industry trends and market dynamics
   - **Financial Analyst**: Performs financial analysis using YFinance tools
   - **Sales Strategist**: Develops tailored sales strategies based on research findings

3. **DeepAgent Coordination**: Instead of manually chaining tasks, `DeepAgent` automatically:
   - Creates execution plans using the planning tool
   - Delegates tasks to appropriate specialists
   - Passes context between subagents
   - Synthesizes findings into comprehensive reports

4. **Memory Persistence**: Uses SQLite database to store session history, summaries, and research findings for continuity across runs.

## Example Queries

- Research "Tesla" in the "Electric Vehicles" industry with stock symbol "TSLA"
- Analyze "Microsoft" and develop a sales strategy for the "Cloud Computing" industry
- Research "Anthropic" in the "AI Safety" industry without financial data

## Input Parameters

- `company_name` (required): Name of the target company
- `company_symbol` (optional): Stock symbol for financial analysis (e.g., "AAPL", "TSLA")
- `industry` (optional): Industry name for focused analysis
- `enable_memory` (optional): Whether to enable memory persistence (default: true)
- `storage_path` (optional): Path for SQLite storage (default: "company_research.db")
- `model` (optional): Model identifier (default: "openai/gpt-4o")

## Output

Returns a dictionary containing:
- `company_name`: The researched company name
- `comprehensive_report`: A structured dictionary containing:
  - Company research findings
  - Industry analysis
  - Financial analysis (if symbol provided)
  - Tailored sales strategy
  - Executive summary with key insights and recommendations
- `research_completed`: Boolean indicating successful completion

The comprehensive report is returned as a JSON-serializable dictionary with all research findings structured according to the `ComprehensiveReportOutput` schema.


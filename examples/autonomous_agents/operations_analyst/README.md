# Operations Analyst Agent

An operations analysis agent built with the **Upsonic AI Agent Framework**. This example demonstrates how to use `AutonomousAgent` with a workspace to read raw shipment data, compute delivery KPIs, write a structured report, and generate charts with matplotlib in a two-task pipeline.

## Features

- **AutonomousAgent with Workspace**: Agent reads and writes files within a sandboxed workspace directory
- **Two-Task Pipeline**: Task 1 analyzes data and writes a report, Task 2 reads the report and produces visualizations
- **Self-Directed Analysis**: The agent decides which KPIs matter based on the data it finds
- **Code Execution**: Uses `run_python` to run matplotlib code directly without writing .py files
- **Persistent Memory**: Logs decisions and findings to `workspace/memory/` for continuity across runs

## Prerequisites

- Python 3.10+
- Anthropic API key

## Installation

1. **Navigate to this directory**:
   ```bash
   cd examples/autonomous_agents/operations_analyst
   ```

2. **Install dependencies**:
   ```bash
   uv sync
   ```

3. **Set up environment variables**:
   ```bash
   export ANTHROPIC_API_KEY="your-api-key"
   ```

## Usage

```bash
uv run examples/autonomous_agents/operations_analyst/main.py
```

The agent will:
1. Read the shipment CSV (80 rows of delivery records)
2. Compute KPIs like on-time rate, carrier performance, route delays, cost efficiency
3. Write `workspace/KPI_REPORT.md` with tables, breakdowns, and commentary
4. Generate one chart per metric and save them to `workspace/charts/`

## Project Structure

```
operations_analyst/
├── main.py                         # Two-task pipeline
├── README.md                       # This file
└── workspace/
    ├── AGENTS.md                   # Agent behavior config
    ├── SOUL.md                     # Agent identity
    └── shipment_data.csv           # Sample shipment data (80 rows)
```

After running, the workspace will also contain:

```
workspace/
├── KPI_REPORT.md                   # Generated report with tables and commentary
├── charts/                         # Generated PNG charts (one per metric)
│   ├── ontime_performance.png
│   ├── carrier_comparison.png
│   └── ...
└── memory/                         # Agent's session log
    └── YYYY-MM-DD.md
```

## How It Works

1. **Workspace setup**: The agent loads its identity from `workspace/SOUL.md` and behavior from `workspace/AGENTS.md`. These files tell it who it is and how to operate.

2. **Task 1 (Analyst)**: The agent reads the raw CSV, explores the data, and decides which metrics are worth surfacing. It writes everything into a markdown report with a summary table, per-carrier breakdown, and its own analysis.

3. **Task 2 (Visualizer)**: The agent reads back the report it just wrote, then uses `run_python` to execute matplotlib code directly. Each chart gets saved as a PNG to `workspace/charts/`.

4. **Memory**: The agent logs what it did in `workspace/memory/` so it has context if you run it again.

## Sample Data

The included `shipment_data.csv` contains 80 shipment records with fields like origin/destination city, carrier, planned vs actual delivery date, shipping cost, and status. Swap it with your own data to analyze different operations.

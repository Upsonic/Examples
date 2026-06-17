# Loan Covenant Monitoring Agent

A multi-agent compliance monitoring system built with the **Upsonic AI Agent Framework**. This example demonstrates how to use `Team` in coordinate mode with specialized `Agent` instances and custom financial calculation tools to automate end-to-end loan covenant compliance analysis.

## Features

- 🏦 **Automated Covenant Extraction**: Parses loan agreements to identify all financial covenant definitions, thresholds, and constraint types
- 📊 **Financial Ratio Calculation**: Uses six custom calculation tools to compute leverage, interest coverage, current ratio, DSCR, and tangible net worth
- ⚠️ **Compliance Assessment**: Evaluates each covenant as compliant, near-breach, or breached with headroom percentages
- 🛡️ **Risk Scoring**: Produces an overall risk score (0-100) with actionable remediation recommendations
- 🏗️ **Modular Design**: Clean separation of concerns with specialized agents, schemas, tools, and team configuration
- 🧠 **Structured Output**: Returns a comprehensive `CovenantMonitoringReport` Pydantic model with full audit trail

## Prerequisites

- Python 3.10+
- Anthropic API key
- OpenAI API key

## Installation

1. **Navigate to this directory**:
   ```bash
   cd examples/loan_covenant_monitoring
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
   export ANTHROPIC_API_KEY="your-api-key"
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
  -d '{
    "inputs": {
        "company_name": "GlobalTech Manufacturing Inc.",
        "reporting_period": "Q4 2025",
        "loan_agreement_path": "data/loan_agreement.txt",
        "financial_data_path": "data/financial_data.json"
    }
  }'
```

## Project Structure

```
loan_covenant_monitoring/
├── main.py                    # Entry point with async main() function
├── team.py                    # Team assembly (coordinate mode + leader)
├── agents.py                  # 3 specialist agent factory functions
├── schemas.py                 # Pydantic output schemas
├── tools.py                   # Custom financial calculation tools
├── task_builder.py            # Task description builder
├── upsonic_configs.json       # Upsonic configuration and dependencies
├── data/
│   ├── loan_agreement.txt     # Synthetic loan agreement (5 covenants)
│   └── financial_data.json    # Synthetic Q4 2025 financials
└── README.md                  # This file
```

## How It Works

1. **Team Assembly**: A `Team` in coordinate mode is created with a leader agent that orchestrates three specialist agents: Covenant Extractor, Financial Calculator, and Risk Assessor.

2. **Covenant Extraction**: The Covenant Extractor agent parses the loan agreement document to identify every financial covenant, its threshold, formula, constraint type, and testing frequency.

3. **Financial Calculation**: The Financial Calculator agent uses custom tools (`calculate_leverage_ratio`, `calculate_interest_coverage_ratio`, etc.) to compute all required ratios from raw financial data.

4. **Compliance Evaluation**: The Risk Assessor agent uses the `evaluate_covenant_compliance` tool to determine each covenant's status (compliant, near-breach, or breached) and computes an overall risk score.

5. **Structured Output**: The final response is enforced to match the `CovenantMonitoringReport` Pydantic model, ensuring consistent and machine-readable output with full audit trail.

## Example Queries

- Monitor Q4 2025 covenant compliance for GlobalTech Manufacturing Inc.
- Evaluate leverage ratio trends approaching covenant limits
- Assess debt service capacity under current cash flow conditions
- Identify breached covenants and recommend remediation strategies

## Input Parameters

- `company_name` (required): Name of the borrower company (e.g., "GlobalTech Manufacturing Inc.")
- `reporting_period` (required): Period being monitored (e.g., "Q4 2025")
- `loan_agreement_path` (required): Path to the loan agreement text file
- `financial_data_path` (required): Path to the financial data JSON file
- `focus_areas` (optional): List of priority focus areas for the analysis
- `enable_memory` (optional): Whether to enable in-memory session persistence (default: true)
- `model` (optional): Model identifier (default: "anthropic/claude-sonnet-4-5")

## Output

Returns a dictionary containing:
- `company_name`: The borrower company name
- `reporting_period`: The period that was monitored
- `report`: Full `CovenantMonitoringReport` object containing:
  - `covenants_extracted`: All covenant definitions from the agreement
  - `calculated_ratios`: Computed ratios with audit trail (formula, components)
  - `compliance_results`: Per-covenant status with headroom percentages
  - `risk_assessment`: Overall score (0-100), risk level, key concerns, and recommended actions
  - `executive_summary`: Narrative summary of findings
  - `next_steps`: Actionable remediation steps
- `monitoring_completed`: Whether the process completed successfully

The report is returned as a JSON-serializable dictionary with all findings structured according to the `CovenantMonitoringReport` schema.

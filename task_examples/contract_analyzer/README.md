# Contract Analyzer Agent

A Contract Analyzer Agent built with the **Upsonic AI Agent Framework**. This example demonstrates how to analyze legal contracts, extract key information, identify potential issues, and provide insights for legal and business decision-making.

## Features

- 📄 **Contract Upload**: Support for PDF, DOCX, and TXT files
- 🔍 **Automatic Extraction**: Parties, dates, financial terms, obligations
- ⚠️ **Risk Detection**: Identify potentially problematic clauses
- 📚 **Legal Knowledge Base**: RAG-enabled search over contract templates and legal references
- 💬 **Interactive Chat**: Ask questions about your contract
- 💾 **Session Memory**: Maintains context across conversations

## Prerequisites

- Python 3.10+
- OpenAI API key

## Installation

1. **Clone or navigate to this directory**:
   ```bash
   cd examples/contract_analyzer
   ```

2. **Install dependencies**:
   ```bash
   # Install all dependencies (API, Streamlit, and development)
   upsonic install all
   
   # Or install specific sections:
   upsonic install api          # API dependencies only (default)
   upsonic install streamlit    # Streamlit dependencies only
   upsonic install development  # Development dependencies only
   ```

   ```

3. **Set up environment variables**:
   ```bash
   cp .env.example .env
   # Edit .env and add your OPENAI_API_KEY
   ```

## Usage

### Run the Streamlit App

```bash
streamlit run streamlit_app.py
```

The app will open in your browser at `http://localhost:8501`.

### Run the API Server

To run the agent as a FastAPI server:

```bash
upsonic run
```

The API will be available at `http://localhost:8000` with automatic OpenAPI documentation at `http://localhost:8000/docs`.


## Project Structure

```
contract_analyzer/
├── main.py                      # API agent workflow (FastAPI endpoint)
├── streamlit_app.py             # Streamlit UI application
├── upsonic_configs.json         # Upsonic configuration and dependencies
├── .env.example                 # Environment template
├── contract_analyzer/
│   ├── __init__.py
│   ├── agent.py                 # Main agent setup
│   ├── config.py                # Configuration
│   ├── tools/
│   │   ├── __init__.py
│   │   └── analysis_toolkit.py  # Contract analysis tools
│   └── knowledge/
│       ├── __init__.py
│       └── legal_kb.py          # Legal knowledge base
└── data/
    └── legal_templates/
        └── contract_clauses.txt # Legal reference document
```

## How It Works

1. **ContractAnalyzerToolKit**: A collection of specialized tools for extracting structured information from contracts (parties, dates, financial terms, obligations, risks).

2. **Legal KnowledgeBase**: A RAG-enabled knowledge base containing contract clause definitions and legal references. The agent decides when to search this knowledge to augment its analysis.

3. **Memory**: Session-based memory maintains conversation context, allowing for follow-up questions about previously analyzed contracts.

## Example Queries

- "What are the key dates in this contract?"
- "Who are the parties involved and what are their obligations?"
- "Are there any potentially risky clauses I should be aware of?"
- "What is the termination policy?"
- "Summarize the financial terms"

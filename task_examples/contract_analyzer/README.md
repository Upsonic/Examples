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
   pip install -r requirements.txt
   ```

3. **Set up environment variables**:
   ```bash
   cp .env.example .env
   # Edit .env and add your OPENAI_API_KEY
   ```

## Usage

### Run the Streamlit App

```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`.

### Programmatic Usage

```python
from contract_analyzer.agent import create_contract_analyzer_agent
from upsonic import Task

# Create the agent
agent = create_contract_analyzer_agent()

# Analyze a contract
contract_text = """
SERVICE AGREEMENT
This Agreement is entered into between ABC Corp ("Provider") 
and XYZ Inc ("Client") effective January 1, 2024...
"""

task = Task(
    description=f"Analyze this contract and provide a comprehensive summary:\n\n{contract_text}"
)

result = agent.do(task)
print(result)
```

## Project Structure

```
contract_analyzer/
├── app.py                       # Streamlit application
├── requirements.txt             # Dependencies
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

## License

This example is part of the Upsonic framework and follows the same license.

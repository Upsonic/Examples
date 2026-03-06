# Upsonic Examples

A curated collection of examples for building with **[Upsonic](https://github.com/Upsonic/Upsonic)**, an open-source agent development framework. Browse by topic to find patterns relevant to what you're building.

---

## Setup

```bash
# Install dependencies
uv sync

# Copy and fill in your API keys
cp .env.example .env
```

---

## Examples by Category

### Getting Started

Simple, single-agent examples — the best place to start if you're new to Upsonic.

| Example | Description | Key Concepts |
|---------|-------------|--------------|
| [extract_people](examples/getting_started/extract_people/) | Extract all people mentioned in a text with structured details (role, affiliation, sentiment) | Agent, Task, Pydantic output |
| [classify_emails](examples/getting_started/classify_emails/) | Classify fintech operation emails into routing categories | Agent, classification, structured output |

---

### Document Processing

Examples that work with files — images, PDFs, and documents using OCR and RAG.

| Example | Description | Key Concepts |
|---------|-------------|--------------|
| [document_analyzer](examples/document_processing/document_analyzer/) | Extract company name from a Turkish tax certificate image | Vision/OCR, image context |
| [contract_analyzer](examples/document_processing/contract_analyzer/) | Analyze legal contracts: extract parties, financial terms, risks, and answer questions | RAG, session memory, Streamlit UI, FastAPI |

---

### Web Search & Scraping

Agents that use web search tools to find and extract information from the internet.

| Example | Description | Key Concepts |
|---------|-------------|--------------|
| [find_company_website](examples/web_search_and_scraping/find_company_website/) | Find a company's official website using Serper API with LLM reasoning | Tool use, Serper API, confidence scoring |
| [find_sales_categories](examples/web_search_and_scraping/find_sales_categories/) | Discover a company's top-level ecommerce categories from their website | Web scraping, BeautifulSoup, batch processing |
| [find_example_product](examples/web_search_and_scraping/find_example_product/) | Autonomously navigate an ecommerce site and extract a product with structured data | Autonomous navigation, multi-step tool use |
| [find_agreement_links](examples/web_search_and_scraping/find_agreement_links/) | Find and verify privacy policy, terms, and cookie pages on any website | Autonomous exploration, link verification |

> `find_sales_categories` and `find_example_product` import from `find_company_website` — run them from the repo root.

---

### Knowledge & Research

Agents that research topics using web search and return structured educational or business content.

| Example | Description | Key Concepts |
|---------|-------------|--------------|
| [ai_lexicon](examples/knowledge_and_research/ai_lexicon/) | Look up AI governance terms and generate definitions + FAQs with DuckDuckGo search | DuckDuckGo tool, structured research, FastAPI |

---

### Multi-Agent

Orchestration patterns: DeepAgent, sequential pipelines, and specialized subagent teams.

| Example | Description | Key Concepts |
|---------|-------------|--------------|
| [git_changelog_writer](examples/multi_agent/git_changelog_writer/) | Turn raw git log output into a developer-focused Twitter post using two sequential agents | Sequential team mode, context handover |
| [company_research_sales_strategy](examples/multi_agent/company_research_sales_strategy/) | Full company research with industry analysis, financial data, and tailored sales strategy | DeepAgent, 4 subagents, SQLite memory |
| [landing_page_generation](examples/multi_agent/landing_page_generation/) | Generate a landing page image by coordinating content, design, and SEO specialists | DeepAgent, image generation, subagent delegation |
| [sales_offer_generator_agent](examples/multi_agent/sales_offer_generator_agent/) | Research products, analyze competitor pricing, and generate a personalized sales offer | DeepAgent, DuckDuckGo, market research |
| [agent_as_tool](examples/multi_agent/agent_as_tool/) | Coordinator agent delegates to specialist agents (research, strategy, content) passed directly as tools | Agent-as-tool pattern, hierarchical agents, model mixing |

---

### Autonomous Agents

Long-running agents with persistent memory, workspace context, and external interfaces.

| Example | Description | Key Concepts |
|---------|-------------|--------------|
| [devops_telegram_bot](examples/autonomous_agents/devops_telegram_bot/) | A DevOps assistant connected to Telegram that remembers context across conversations | AutonomousAgent, TelegramInterface, workspace memory |
| [expense_tracker_bot](examples/autonomous_agents/expense_tracker_bot/) | Chat-based Telegram bot that reads receipt photos via OCR, logs expenses to CSV, and generates monthly summaries | AutonomousAgent, TelegramInterface, OCR, ngrok, workspace memory |

---

### Safety & Policies

Examples demonstrating Upsonic's Safety Engine for content filtering and policy enforcement.

| Example | Description | Key Concepts |
|---------|-------------|--------------|
| [crypto_block_policy](examples/safety_and_policies/crypto_block_policy/) | Block cryptocurrency-related content using a prebuilt policy | Safety Engine, CryptoBlockPolicy, content moderation |
| [gpt_oss_safety_agent](examples/safety_and_policies/gpt_oss_safety_agent/) | Detect and block PII in agent inputs and outputs | PIIBlockPolicy, OpenRouter, safety enforcement |

---

### Alternative Models

Use Upsonic with models beyond OpenAI — local, open-source, and enterprise providers.

| Example | Description | Key Concepts |
|---------|-------------|--------------|
| [ollama_agent](examples/alternative_models/ollama_agent/) | Run agents locally with Ollama and llama3.2 — no cloud APIs required | OllamaModel, local inference, privacy-first |
| [nvidia_agent](examples/alternative_models/nvidia_agent/) | Use NVIDIA NIM API to access Llama, Mistral, and other enterprise models | NvidiaModel, NVIDIA NIM |
| [groq_code_review_agent](examples/alternative_models/groq_code_review_agent/) | Ultra-fast code review with security, performance, and best-practice analysis via Groq | GroqModel, code analysis, DuckDuckGo, FastAPI |

---

### Interactive

Agents with streaming responses and conversational interfaces.

| Example | Description | Key Concepts |
|---------|-------------|--------------|
| [moltbook_agent](examples/interactive/moltbook_agent/) | Interactive chat with streaming text, tool call tracking, and event-based responses | Chat, streaming, event handling |

---

## Project Structure

```
examples/
├── getting_started/          # Simple 1-agent examples — start here
│   ├── extract_people/
│   └── classify_emails/
├── document_processing/      # OCR, PDF analysis, RAG
│   ├── document_analyzer/
│   └── contract_analyzer/
├── web_search_and_scraping/  # Web tools and scraping
│   ├── find_company_website/
│   ├── find_sales_categories/
│   ├── find_example_product/
│   └── find_agreement_links/
├── knowledge_and_research/   # Research agents with web search
│   └── ai_lexicon/
├── multi_agent/              # Multi-agent orchestration patterns
│   ├── git_changelog_writer/
│   ├── company_research_sales_strategy/
│   ├── landing_page_generation/
│   ├── sales_offer_generator_agent/
│   └── agent_as_tool/
├── autonomous_agents/        # Long-running agents with memory & interfaces
│   ├── devops_telegram_bot/
│   └── expense_tracker_bot/
├── safety_and_policies/      # Safety Engine and content filtering
│   ├── crypto_block_policy/
│   └── gpt_oss_safety_agent/
├── alternative_models/       # Non-OpenAI model providers
│   ├── ollama_agent/
│   ├── nvidia_agent/
│   └── groq_code_review_agent/
└── interactive/              # Streaming and chat interfaces
    └── moltbook_agent/
```

---

## API Keys Reference

| Key | Used By |
|-----|---------|
| `OPENAI_API_KEY` | Most examples (default model provider) |
| `SERPER_API_KEY` | `find_company_website`, `find_sales_categories`, `find_example_product` |
| `GROQ_API_KEY` | `groq_code_review_agent` |
| `NVIDIA_API_KEY` | `nvidia_agent` (get from [build.nvidia.com](https://build.nvidia.com)) |
| `OPENROUTER_API_KEY` | `gpt_oss_safety_agent` |
| `ANTHROPIC_API_KEY` | `expense_tracker_bot` |
| `TELEGRAM_BOT_TOKEN` | `devops_telegram_bot`, `expense_tracker_bot` |
| *(none)* | `ollama_agent`, `crypto_block_policy` |

---

## Contributing

Each example lives in its own directory with a `README.md` and standalone scripts. To add a new example, create a folder under the most fitting category and include a clear `README.md` explaining what it does and how to run it.

---

Built with [Upsonic](https://github.com/Upsonic/Upsonic) — open-source agent development framework.

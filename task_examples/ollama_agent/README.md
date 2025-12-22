# Ollama Agent

An Ollama Agent built with the **Upsonic AI Agent Framework**. This example demonstrates how to create and use an Upsonic Agent that leverages local LLMs via Ollama, specifically using the `llama3.2` model. This allows for private, local execution of AI tasks.

## Features

- 🦙 **Local LLM Support**: Uses `OllamaModel` to connect to locally running Ollama instances
- 🏠 **Privacy-First**: All processing happens locally on your machine
- 🚀 **Simple Integration**: Easy setup with Upsonic's `Agent` and `Task` classes
- ⚡ **Synchronous & Asynchronous**: Supports both direct script execution and running as an API server

## Prerequisites

- Python 3.10+
- [Ollama](https://ollama.com/) installed and running
- `llama3.2` model pulled (`ollama pull llama3.2`)

## Installation

1. **Navigate to this directory**:
   ```bash
   cd examples/ollama_agent
   ```

2. **Install dependencies**:
   ```bash
   # Install API dependencies (default)
   upsonic install api
   ```

3. **Prepare Ollama**:
   Ensure Ollama is running and you have the model:
   ```bash
   ollama pull llama3.2
   ```

## Usage

### Run Directly

You can run the agent directly as a Python script to see it in action:

```bash
python3 main.py
```

### Run the API Server

To run the agent as a FastAPI server:

```bash
upsonic run
```

The API will be available at `http://localhost:8000` with automatic OpenAPI documentation at `http://localhost:8000/docs`.

**Example API Call:**
```bash
curl -X POST http://localhost:8000/call \
  -H "Content-Type: application/json" \
  -d '{"user_query": "Explain quantum computing in one sentence."}'
```

## Project Structure

```
ollama_agent/
├── main.py                    # Agent entry point (Script + API)
├── upsonic_configs.json       # Upsonic configuration and dependencies
└── README.md                  # Quick start guide
```

## How It Works

1.  **OllamaModel**: The `OllamaModel` class connects to your local Ollama instance (defaulting to `http://localhost:11434`). It allows you to specify which local model to use (e.g., `llama3.2`).

2.  **Agent**: The standard `Agent` class is initialized with this `OllamaModel`. This tells the agent to use your local LLM for reasoning and generation instead of cloud APIs like OpenAI.

3.  **Task**: Defines the work to be done. In this example, it's a simple text generation task provided by the user.

## Example Queries

- "Write a python function to calculate fibonacci numbers."
- "Summarize the history of the internet."
- "What are the benefits of local LLMs?"

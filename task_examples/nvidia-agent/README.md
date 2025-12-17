# NVIDIA Agent Example

This example demonstrates how to create and use an Agent with NVIDIA models using the Upsonic framework.

## Overview

This example includes:
- **NvidiaModel**: Uses NVIDIA NIM API to access various AI models
- **Agent**: Upsonic Agent configured with NVIDIA model
- **Task**: Simple task execution with user queries
- **FastAPI Server**: Run as a server using `upsonic run` command
- **Direct Execution**: Run directly with `python main.py`

## Setup

### 1. Install Dependencies

Install the required dependencies using the Upsonic CLI:

```bash
upsonic install all # Installs all dependencies in the upsonic_configs.json

# OR

upsonic install <dependency group>
```


Alternatively, you can install specific sections:
- `upsonic install api` - Install API dependencies only
- `upsonic install all` - Install all dependencies (api, streamlit, development)
- `upsonic install` - Install only "api" group as default

### 2. Set Up Environment Variables

1. Copy `env.example` to `.env`:
   ```bash
   cp env.example .env
   ```

2. Edit `.env` and add your NVIDIA API key:
   ```
   NVIDIA_API_KEY=your_actual_api_key_here
   ```

3. **Get your NVIDIA API key**:
   - Visit https://build.nvidia.com/
   - Sign up or log in to your NVIDIA account
   - Navigate to API Keys section
   - Create a new API key
   - Copy the key to your `.env` file

## Running the Example

### Option 1: Run as FastAPI Server (Recommended)

Run the agent as a FastAPI server using the Upsonic CLI:

```bash
upsonic run
```

This will:
- Start a FastAPI server on `http://0.0.0.0:8000`
- Create an API endpoint at `/call` that accepts POST requests
- Generate OpenAPI documentation at `/docs`
- Use the `async main(inputs)` function from `main.py`

**API Usage:**
```bash
# Using curl
curl -X POST "http://localhost:8000/call" \
  -H "Content-Type: application/json" \
  -d '{"user_query": "What is artificial intelligence?"}'

# Or visit http://localhost:8000/docs for interactive API documentation
```

### Option 2: Direct Execution

Run the example directly:

```bash
python main.py
```

## Configuration

### Environment Variables

The example uses the following environment variables:

- **NVIDIA_API_KEY** (required): Your NVIDIA API key. Alternatively, you can use `NGC_API_KEY`.
- **NVIDIA_BASE_URL** (optional): Custom base URL for NVIDIA NIM endpoint. Defaults to `https://integrate.api.nvidia.com/v1`.

### upsonic_configs.json

The `upsonic_configs.json` file controls:

- **agent_name**: Name of the agent ("NVIDIA Agent")
- **description**: Agent description
- **entrypoints.api_file**: Main Python file (`main.py`)
- **input_schema**: Defines the input parameters (currently `user_query`)
- **output_schema**: Defines the output structure (currently `bot_response`)
- **dependencies**: Lists all required packages for different environments

### Model Selection

You can change the model in `main.py` by modifying the `model_name` parameter in the `NvidiaModel` constructor. Available models include:

- `meta/llama-3.1-nemotron-70b-instruct:1.0` (default)
- `openai/gpt-oss-20b:1.0`
- `mistral/mistral-large:2.0`
- And many more available through NVIDIA NIM

Check the [NVIDIA NIM documentation](https://build.nvidia.com/) for the full list of available models.

## Code Structure

```
nvidia-agent/
├── main.py                    # Main agent file with async main(inputs) function for FastAPI server
├── upsonic_configs.json       # Configuration file defining agent metadata, input/output schemas, and dependencies
├── env.example                # Example environment variables file (copy to .env and add your API key)
└── README.md                  # This documentation file
```

## Upsonic CLI Commands

- **`upsonic init`**: Initialize a new agent project
- **`upsonic install [section]`**: Install dependencies from `upsonic_configs.json`
- **`upsonic run [--host HOST] [--port PORT]`**: Run the agent as a FastAPI server
- **`upsonic add <library> <section>`**: Add a dependency to the config
- **`upsonic remove <library> <section>`**: Remove a dependency from the config

## Troubleshooting

1. **Missing API Key**: Make sure `NVIDIA_API_KEY` is set in your `.env` file
2. **Dependencies Not Installed**: Run `upsonic install` to install required packages
3. **Port Already in Use**: Use `upsonic run --port 8001` to use a different port
4. **Model Not Found**: Check that the model name is correct and available in NVIDIA NIM

## Additional Resources

- [Upsonic Documentation](https://github.com/upsonic/upsonic)
- [NVIDIA NIM Documentation](https://build.nvidia.com/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)

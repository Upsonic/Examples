# Landing Page Generation Agent

A comprehensive Landing Page Generation Agent built with the **Upsonic AI Agent Framework**. This example demonstrates how to use `DeepAgent` with specialized subagents to generate landing page images by coordinating content creation, design recommendations, and SEO optimization, then creating the final visual.

## Features

- 🖼️ **Image Generation**: Generates actual landing page images (PNG format, 1536x1024)
- ✍️ **Content Creation**: Expert copywriting for headlines, value propositions, CTAs, and feature highlights
- 🎨 **Design Recommendations**: Color schemes, typography, layout structures, and visual element suggestions
- 🔍 **SEO Optimization**: Meta tags, keywords, header structure, and technical SEO elements
- 🤖 **DeepAgent Orchestration**: Automatically plans and coordinates specialized sub-agents to fulfill complex generation goals
- 🧠 **Persistent Memory**: SQLite-based memory for session persistence and conversation history
- 🏗️ **Modular Design**: Clean separation of concerns with specialized agents, schemas, and utilities

## Prerequisites

- Python 3.10+
- OpenAI API key

## Installation

1. **Navigate to this directory**:
   ```bash
   cd examples/landing_page_generation
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
uv run main.py
```

**Example API Call:**
```bash
curl -X POST http://localhost:8000/call \
  -H "Content-Type: application/json" \
  -d '{
    "product_name": "AI Writing Assistant",
    "target_audience": "Content creators and marketers",
    "primary_goal": "sign up for free trial",
    "key_features": ["AI-powered content", "Multiple templates", "Real-time collaboration"],
    "brand_tone": "friendly and professional"
  }'
```

## Project Structure

```
landing_page_generation/
├── main.py                    # Entry point with async main() function
├── upsonic_configs.json       # Upsonic configuration and dependencies
├── orchestrator.py             # DeepAgent orchestrator creation
├── subagents.py               # Specialized subagent factory functions
├── schemas.py                 # Pydantic output schemas
├── task_builder.py           # Task description builder
└── README.md                  # This file
```

## How It Works

1. **Orchestrator Agent**: A `DeepAgent` that coordinates the entire landing page generation process using planning tools and subagent delegation.

2. **Specialized Subagents**: Three domain experts that handle specific generation areas:
   - **Content Writer**: Creates compelling copy, headlines, CTAs, and messaging
   - **Designer**: Provides design recommendations for colors, typography, layout, and visuals
   - **SEO Specialist**: Optimizes for search engines with meta tags, keywords, and structure

3. **DeepAgent Coordination**: Instead of manually chaining tasks, `DeepAgent` automatically:
   - Creates execution plans using the planning tool
   - Delegates tasks to appropriate specialists
   - Passes context between subagents
   - Synthesizes all specifications into a detailed image generation prompt
   - Generates the final landing page image

4. **Image Generation**: Uses OpenAI's image generation capabilities to create high-quality landing page visuals based on all gathered specifications.

5. **Memory Persistence**: Uses SQLite database to store session history, summaries, and generation results for continuity across runs.

## Example Queries

- Generate a landing page image for "AI Writing Assistant" targeting "content creators" with goal "sign up"
- Create a landing page image for "E-commerce Platform" targeting "small business owners" with goal "start free trial"
- Generate a landing page image for "Fitness App" targeting "health-conscious individuals" with goal "download app"

## Input Parameters

- `product_name` (required): Name of the product or service
- `target_audience` (required): Description of the target audience
- `primary_goal` (required): Primary conversion goal (e.g., "sign up", "purchase", "download")
- `key_features` (optional): List of key features to highlight
- `brand_tone` (optional): Brand tone for the landing page (default: "professional")
- `enable_memory` (optional): Whether to enable memory persistence (default: true)
- `storage_path` (optional): Path for SQLite storage (default: "landing_page_generation.db")
- `model` (optional): Model identifier (default: "openai-responses/gpt-4o")
- `output_folder` (optional): Folder path for saving generated image (default: "landing_page_images")

## Output

Returns a dictionary containing:
- `product_name`: The product name for which the landing page was generated
- `image_path`: Full path to the generated landing page image file (PNG format)
- `generation_completed`: Boolean indicating successful completion

The generated image incorporates all specifications from content, design, and SEO subagents into a cohesive visual landing page.

# Agent as Tool

A hierarchical multi-agent example built with the **Upsonic AI Agent Framework**. This example demonstrates how to use specialized agents as tools for a coordinator agent, so each specialist handles what it's good at while the coordinator orchestrates the workflow.

## Features

- **Agent-as-Tool Pattern**: Pass agents directly into another agent's `tools` list for automatic delegation
- **Specialist Agents**: Research, strategy, and content agents with focused system prompts and different models
- **Model Mixing**: Use GPT-4o for strategy-heavy work, GPT-4o-mini for content, optimizing cost per task
- **Four Patterns**: Simple delegation, multi-agent workflow, sequential consultation, and nested agents
- **Side-by-Side Comparison**: `simple_comparison.py` runs single-agent vs agent-as-tool back to back

## Prerequisites

- Python 3.10+
- OpenAI API key

## Installation

1. **Navigate to this directory**:
   ```bash
   cd examples/multi_agent/agent_as_tool
   ```

2. **Install dependencies**:
   ```bash
   uv sync
   ```

3. **Set up environment variables**:
   ```bash
   export OPENAI_API_KEY="your-api-key"
   ```

## Usage

Full hierarchical demo with 4 patterns (simple delegation, multi-agent workflow, sequential consultation, nested agents):

```bash
uv run examples/multi_agent/agent_as_tool/hierarchical_agents_example.py
```

Side-by-side comparison of single agent vs agent-as-tool:

```bash
uv run examples/multi_agent/agent_as_tool/simple_comparison.py
```

You can also run just one approach:

```bash
uv run examples/multi_agent/agent_as_tool/simple_comparison.py --single
uv run examples/multi_agent/agent_as_tool/simple_comparison.py --hierarchical
```

## Project Structure

```
agent_as_tool/
├── hierarchical_agents_example.py   # Full demo with 4 patterns
├── simple_comparison.py             # Single agent vs agent-as-tool comparison
└── README.md                        # This file
```

## How It Works

1. **Define specialists**: Create agents with focused system prompts, roles, and goals. Pick the right model per agent (e.g. GPT-4o for strategy, GPT-4o-mini for content).

2. **Wire them as tools**: Pass specialist agents into the coordinator's `tools` list. Upsonic handles the rest.

3. **Run a task**: The coordinator receives a high-level task, decides which specialists to call, and synthesizes their outputs.

```python
coordinator = Agent(
    name="Campaign Director",
    model="openai/gpt-4o",
    tools=[research_agent, strategy_agent, content_agent]
)

result = coordinator.do(task)
```

## Patterns Covered

| Pattern | Description |
|---------|-------------|
| Simple Delegation | Coordinator uses one specialist as a tool |
| Multi-Agent Workflow | Coordinator orchestrates 3 specialists in one task |
| Sequential Consultation | Pass output from one specialist into the next |
| Nested Agents | A team lead agent is itself a tool for a higher-level coordinator |

# Git Changelog Writer

A multi-agent pipeline built with the **Upsonic AI Agent Framework**. This example demonstrates how to use `Team` with `mode="sequential"` to turn raw `git log` output into a ready-to-post Twitter/X update — two agents pass context automatically, no glue code required.

## Features

- **Sequential Team**: Two agents run in sequence with automatic context handover (`mode="sequential"`)
- **Tech Lead Agent**: Filters noise commits (`chore`, `docs`) and extracts user-facing changes from `feat` and `fix` entries
- **Growth Hacker Agent**: Converts the technical summary into a developer-native Twitter/X post (max 280 characters)
- **No Glue Code**: Output from Agent A flows into Agent B automatically — no variable passing or string parsing

## Prerequisites

- Python 3.10+
- OpenAI API key

## Installation

1. **Navigate to this directory**:
   ```bash
   cd examples/multi_agent/git_changelog_writer
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

```bash
uv run main.py
```

## Project Structure

```
git_changelog_writer/
├── main.py        # Sequential Team pipeline
└── README.md      # This file
```

## How It Works

1. **Input**: A changelog or `git log --oneline` string is passed to the first task. The example ships with mock data — swap it for real `git log` output in production.

2. **Agent A (Tech Lead)**: Reads the commits, ignores housekeeping tags (`chore`, `docs`), and produces a clean technical summary of user-facing `feat` and `fix` entries.

3. **Context Handover**: Upsonic's `mode="sequential"` automatically injects Agent A's output into Agent B's task context. No manual wiring needed.

4. **Agent B (Growth Hacker)**: Applies strict tone and formatting rules to write a single Twitter/X post (max 280 characters) that reads like an engineer sharing something useful, not a marketing announcement.

5. **Output**: `tasks[-1].response` contains the final tweet.

## Example Output

**Agent A (Tech Lead)** summarizes:

```
Summary of User-Facing Changes:

1. New Feature: Telegram Interface
   - What Changed: Full Telegram bot interface for agents via webhook.
   - Why Users Care: Agents can now be used over Telegram chat.

2. Bug Fix: LLM Usage Tracking
   - What Changed: Fixed tracking for direct LLM call metrics.
   - Why Users Care: Accurate usage data in dashboards.
```

**Agent B (Growth Hacker)** turns it into a tweet:

```
Upsonic v0.72.0 is out.

New Telegram interface so your agents can run over chat.
CLI now starts interfaces directly — no programmatic setup.

- Telegram bot interface (webhook, messages, media)
- CLI + interface compatibility
- LLM usage tracking fix

Changelog: [link]
```

## Notes

- **No glue code**: `mode="sequential"` handles all context passing between agents.
- **Tone-tuned**: Agent B's instructions use specific constraints ("no hashtags", "no 'we're thrilled'") rather than vague guidelines.
- **Extendable**: Add more agents to the list (e.g., Editor, Translator) — context still flows automatically.
- **Cost**: ~$0.01 per run (both agents combined).

# Git Changelog Writer

This example demonstrates how to use **Upsonic's Sequential Team mode** to turn raw `git log` output into a ready-to-post Twitter/X update — using two AI agents that pass context automatically.

## Overview

The pipeline has two agents:

1. **Tech Lead** — Reads raw commit messages, filters out noise (`chore`, `docs`), and produces a clean technical summary of user-facing changes.
2. **Growth Hacker** — Takes that summary and writes a developer-native Twitter/X post. No hashtags, no corporate tone, no emoji spam.

The key idea: `mode="sequential"` handles the context handover between agents. You don't pass variables or parse strings — the output of Agent A flows into Agent B automatically.

---

## Setup

### 1. Install dependencies

```bash
uv sync
```

### 2. Configure OpenAI API Key

Set your OpenAI API key as an environment variable:

```bash
export OPENAI_API_KEY="your_openai_api_key_here"
```

Or create a `.env` file in the project root:

```bash
echo "OPENAI_API_KEY=your_openai_api_key_here" > .env
```

---

## Run the Example

```bash
uv run examples/multi_agent/git_changelog_writer/main.py
```

### Example Output

**Agent A (Tech Lead)** filters and summarizes:

```
Summary of User-Facing Changes:

1. New Feature: Dark Mode Support
   - What Changed: The user interface now offers dark mode support.
   - Why Users Care: More comfortable for extended usage and low-light environments.

2. New Feature: Smart Caching Layer
   - What Changed: A smart caching layer was introduced to optimize performance.
   - Why Users Care: Dashboard load times are 3x faster.

3. Bug Fix: Database Connection Timeout
   - What Changed: Resolved a timeout issue under heavy load.
   - Why Users Care: Improved reliability during peak usage.

4. Bug Fix: Real-Time Notifications
   - What Changed: Fixed a race condition affecting notifications.
   - Why Users Care: Notifications are now delivered accurately and timely.
```

**Agent B (Growth Hacker)** turns it into a tweet:

```
Dark mode now available across our UI. 🌙

UI enhancements + performance upgrades with these latest updates.

- 🌙 Dark Mode support
- 🚀 Dashboard 3x speed boost with smart caching
- 🔧 Database timeout fix for heavy loads
- 🛠️ Real-time notifications now more reliable

Changelog: [link]
```

---

## How It Works

1. **Input**: A string of `git log --oneline` output (mock data in the script, swap for real git later).
2. **Agent A**: Analyzes commits, ignores housekeeping (`chore`/`docs`), extracts user-facing value from `feat` and `fix` entries.
3. **Context Handover**: Upsonic's Sequential Team automatically passes Agent A's output into Agent B's context.
4. **Agent B**: Applies tone and formatting rules to produce a single, post-ready tweet.
5. **Output**: `tasks[-1].response` gives you the final tweet directly.

---

## File Structure

```bash
examples/multi_agent/git_changelog_writer/
├── main.py        # Sequential Team pipeline
└── README.md      # This file
```

---

## Notes

- **No glue code**: `mode="sequential"` handles all context passing between agents.
- **Tone-tuned**: Agent B's instructions use specific constraints ("no hashtags", "no 'we're thrilled'") rather than vague guidelines like "be professional."
- **Cost**: ~$0.01 per run (both agents combined).
- **Extendable**: Add more agents to the list (e.g., Editor, Translator) — the context still flows automatically.

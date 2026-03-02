# Expense Tracker Bot

An expense tracking Telegram bot built with the **Upsonic AI Agent Framework**. This example demonstrates how to use `AutonomousAgent` with `TelegramInterface`, workspace-driven behavior, and a single custom tool (OCR) to read receipt photos and track expenses autonomously.

## Features

- **Telegram Integration**: Full bidirectional chat interface via Telegram Bot API with `InterfaceMode.CHAT`
- **Workspace-Driven Behavior**: Agent behavior defined in `AGENTS.md` and `SOUL.md`, not hardcoded in the script
- **OCR-Powered Extraction**: Uses Upsonic's built-in `EasyOCREngine` as the only custom tool — everything else the agent handles through workspace filesystem
- **Autonomous CSV Management**: The agent creates, reads, writes, and deduplicates `expenses.csv` on its own based on instructions in `AGENTS.md`
- **Persistent Memory**: Logs daily activity to `workspace/memory/` for continuity across sessions

## Prerequisites

- Python 3.10+
- Anthropic API key
- Telegram bot token (via BotFather)
- ngrok or similar tunneling tool for webhook delivery

## Installation

1. **Navigate to this directory**:
   ```bash
   cd examples/autonomous_agents/expense_tracker_bot
   ```

2. **Install dependencies**:
   ```bash
   uv venv && source .venv/bin/activate
   uv pip install -r requirements.txt
   ```

3. **Create a Telegram bot**:
   - Open Telegram, search **@BotFather**, send `/newbot`
   - Follow the prompts and copy the bot token

4. **Start ngrok**:
   ```bash
   ngrok http 8000
   ```
   Copy the `https://xxxx.ngrok-free.app` URL.

5. **Set up environment variables**:
   ```bash
   export ANTHROPIC_API_KEY="your-api-key"
   export TELEGRAM_BOT_TOKEN="your-bot-token"
   export TELEGRAM_WEBHOOK_URL="https://xxxx.ngrok-free.app"
   ```

## Usage

```bash
uv run examples/autonomous_agents/expense_tracker_bot/main.py
```

The server starts on `http://0.0.0.0:8000` and registers the Telegram webhook automatically.

**Example messages to send your bot:**

| Message | What happens |
|---------|-------------|
| Photo of a receipt | OCR extracts text, agent parses and saves to `expenses.csv` |
| "summary" or "this month" | Agent reads CSV and returns category breakdown |
| `/reset` | Clears conversation context |

## Project Structure

```
expense_tracker_bot/
├── main.py              # Bot server with AutonomousAgent + TelegramInterface
├── tools.py             # OCR extraction tool (the only custom tool)
├── README.md            # This file
└── workspace/
    ├── AGENTS.md        # Agent behavior: receipt workflow, CSV format, rules
    ├── SOUL.md          # Agent identity
    ├── expenses.csv     # Created by agent at runtime
    └── memory/          # Daily session logs
```

## How It Works

1. **Agent loads workspace**: On startup, the agent reads `AGENTS.md` and `SOUL.md` from the workspace to understand its role, workflow, and data format. No behavior is hardcoded in the script.

2. **Photo received**: When a user sends a receipt photo, the agent calls `ocr_extract_text` (its only custom tool), which uses EasyOCR to read the text.

3. **Parsing & saving**: The agent parses the OCR output following the rules in `AGENTS.md` (date format conversion, amount normalization, category assignment), checks for duplicates by reading `expenses.csv`, and appends the new record — all through workspace filesystem access.

4. **Summaries**: When asked for a summary, the agent reads `expenses.csv`, groups by category, and computes totals. No dedicated summary tool needed.

5. **Memory**: The agent logs daily activity to `workspace/memory/` so it retains context across sessions.

## Notes

- Only one custom tool (`ocr_extract_text`) is needed — everything else the agent handles through workspace filesystem
- OCR language is set to Turkish (`tr`) by default. Change the `languages` parameter in `tools.py` for other languages
- The CSV format is defined in `AGENTS.md`, not in code. Change the schema there and the agent adapts

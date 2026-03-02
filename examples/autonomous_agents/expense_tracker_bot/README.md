# Expense Tracker Bot

An expense tracking Telegram bot built with the **Upsonic AI Agent Framework**. This example demonstrates how to use `AutonomousAgent` with `TelegramInterface` and custom tools to read receipt photos via OCR, extract structured data, and save expenses to a CSV file.

## Features

- **Telegram Integration**: Full bidirectional chat interface via Telegram Bot API with `InterfaceMode.CHAT`
- **OCR-Powered Extraction**: Uses Upsonic's built-in `EasyOCREngine` to read text from receipt photos
- **Custom Tools**: Three tools (`ocr_extract_text`, `save_expense`, `get_monthly_summary`) handle the full workflow
- **Pydantic Validation**: All expense records are validated through a Pydantic model before saving
- **Duplicate Detection**: Same date + amount + merchant triggers a duplicate warning
- **Monthly Summaries**: Category breakdown with percentages and totals on demand

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
   uv sync
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
| Photo of a receipt | OCR extracts text, parses amount/date/merchant, saves to CSV |
| "summary" or "this month" | Returns monthly expense breakdown by category |
| `/reset` | Clears conversation context |

## Project Structure

```
expense_tracker_bot/
├── main.py              # Bot server with AutonomousAgent + TelegramInterface
├── tools.py             # OCR extraction, expense saving, monthly summary tools
├── models.py            # Pydantic model for expense validation
├── README.md            # This file
├── data/                # Created at runtime
│   └── expenses.csv     # All saved expenses
└── workspace/           # Agent workspace (empty, filesystem/shell disabled)
```

## How It Works

1. **Photo received**: The bot detects the incoming image and calls `ocr_extract_text`, which uses EasyOCR to read the text from the receipt.

2. **Parsing**: The agent extracts date, amount, merchant name, and category from the OCR output. It handles format conversion (e.g. `14.02.2026` to `2026-02-14`, `415,20` to `415.20`).

3. **Validation & save**: The `save_expense` tool validates through a Pydantic model, checks for duplicates, appends to `data/expenses.csv`, and returns a monthly running total.

4. **Summaries**: `get_monthly_summary` reads the CSV and returns a category breakdown with percentages.

## Notes

- The agent has `enable_filesystem=False` and `enable_shell=False` since it only needs its custom tools
- OCR language is set to Turkish (`tr`) by default. Change the `languages` parameter in `tools.py` for other languages
- Expenses are stored in a flat CSV file under `data/`. No database required

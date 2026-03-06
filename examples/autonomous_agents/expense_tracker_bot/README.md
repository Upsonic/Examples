# Expense Tracker Bot

An expense tracking agent built with the **Upsonic AI Agent Framework**. This example demonstrates how to use `AutonomousAgent` with the Telegram interface to create a chat-based bot that extracts data from receipt photos using OCR, logs expenses to a CSV, and generates monthly summaries — all from your phone.

## Features

- **Telegram Integration**: Full bidirectional chat interface via Telegram Bot API
- **Autonomous Agent**: Powered by Upsonic's `AutonomousAgent` with workspace file access
- **Receipt OCR**: Extracts merchant, amount, date, and category from receipt photos using EasyOCR
- **Expense Logging**: Appends parsed expenses to `expenses.csv` with duplicate detection
- **Monthly Summaries**: Groups spending by category with totals and percentages on request
- **Chat Mode**: Maintains conversation context across messages using `InterfaceMode.CHAT`
- **Ngrok Tunneling**: Exposes the local server to the internet for Telegram webhook delivery
- **Custom Identity**: Agent personality and behavior defined via `AGENTS.md` and `SOUL.md` in the workspace

## Prerequisites

- Python 3.10+
- Anthropic API key
- Telegram bot token (via BotFather)
- ngrok account and authtoken

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
   - Open Telegram → search **@BotFather** → send `/newbot`
   - Follow the prompts and copy the bot token
   - Search **@userinfobot** → send any message → copy your user ID

4. **Start ngrok**:
   ```bash
   ngrok config add-authtoken YOUR_NGROK_TOKEN
   ngrok http 8000
   ```
   Copy the `https://xxxx.ngrok-free.app` URL.

5. **Set up environment variables**:
   ```bash
   cp .env.example .env
   ```
   Edit `.env` with your values:
   ```
   TELEGRAM_BOT_TOKEN=your-bot-token
   TELEGRAM_WEBHOOK_URL=https://xxxx.ngrok-free.app
   ANTHROPIC_API_KEY=your-api-key
   ```

## Usage

Run the bot server:

```bash
uv run main.py
```

The server starts on `http://0.0.0.0:8000` and registers the Telegram webhook automatically.

**Example messages to send your bot:**

| Message | What happens |
|---|---|
| *(send a receipt photo)* | Agent runs OCR, parses fields, saves to `expenses.csv` |
| `Summary` | Agent reads `expenses.csv`, returns this month's breakdown by category |
| `How much did I spend on groceries in February?` | Agent filters CSV and returns the total |
| `Show me my last 5 expenses` | Agent reads and formats recent entries |
| `Report for March` | Agent generates a full monthly report with percentages |

Send `/reset` to clear conversation context.

## Project Structure

```
expense_tracker_bot/
├── main.py                         # Bot server and agent setup
├── tools.py                        # OCR tool using EasyOCR
├── requirements.txt                # Python dependencies
├── .env                            # API keys (you fill this in)
├── .env.example                    # Template for .env
│
└── workspace/                      # Agent's sandboxed home
    ├── AGENTS.md                   # Agent behavior and receipt workflow
    ├── SOUL.md                     # Agent identity
    ├── USER.md                     # Who the user is
    ├── BOOTSTRAP.md                # First-run initialization guide
    ├── expenses.csv                # Expense records (created on first receipt)
    └── memory/                     # Agent's daily memory logs
```

## How It Works

1. **Bot Server**: `main.py` starts a FastAPI server that handles incoming Telegram webhook events.

2. **AutonomousAgent**: The agent loads its behavior from `workspace/AGENTS.md`, its identity from `workspace/SOUL.md`, and accumulated memory from `workspace/memory/`.

3. **Receipt Processing**: When a photo arrives, the agent calls `ocr_extract_text` to extract text via EasyOCR, then parses date, amount, merchant, and category from the result before appending to `expenses.csv`.

4. **Telegram Interface**: `TelegramInterface` in `CHAT` mode wraps the agent, maintaining conversation context across messages for a natural back-and-forth experience.

5. **Webhook Delivery**: ngrok tunnels requests from Telegram's servers to your local bot server, enabling development without a public IP.

## Security Notes

- The agent is sandboxed to the `workspace/` directory — file operations outside it are blocked.
- Set `TELEGRAM_USER_ID` in `.env` to restrict the bot to your account only.
- Expense data stays local — nothing is sent to external services beyond the LLM call.

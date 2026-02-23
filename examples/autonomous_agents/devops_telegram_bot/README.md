# DevOps Telegram Bot

A DevOps automation agent built with the **Upsonic AI Agent Framework**. This example demonstrates how to use `AutonomousAgent` with the Telegram interface to create a chat-based sysadmin bot that can read logs, check disk usage, create backups, and run shell commands — all from your phone.

## Features

- **Telegram Integration**: Full bidirectional chat interface via Telegram Bot API
- **Autonomous Agent**: Powered by Upsonic's `AutonomousAgent` with filesystem and shell access
- **Workspace Sandboxing**: Agent is restricted to a dedicated `workspace/` directory for safe operation
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
   cd examples/autonomous_agents/devops_telegram_bot
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
uv run bot.py
```

The server starts on `http://0.0.0.0:8000` and registers the Telegram webhook automatically.

**Example messages to send your bot:**

| Message | What happens |
|---|---|
| `Check disk usage` | Agent runs `df -h`, returns formatted result |
| `Find all log files larger than 50KB` | Agent searches workspace, lists matching files |
| `Create a backup of the app directory` | Agent tars `app/` into `backups/`, confirms |
| `Read the last 20 lines of error.log and tell me what's wrong` | Agent reads and analyzes log content |
| `List all running processes using port 8000` | Agent runs shell command, returns results |
| `Show me the app config` | Agent reads `config.yaml`, explains it |

Send `/reset` to clear conversation context.

## Project Structure

```
devops_telegram_bot/
├── bot.py                          # Main bot server
├── .env                            # API keys (you fill this in)
├── .env.example                    # Template for .env
├── requirements.txt                # Python dependencies
│
└── workspace/                      # Agent's sandboxed home
    ├── AGENTS.md                   # Agent personality and behavior
    ├── SOUL.md                     # Agent identity
    ├── USER.md                     # Who the user is
    ├── memory/                     # Agent's daily memory logs
    │
    ├── logs/                       # Sample logs for demo
    │   ├── error.log               # Application error log
    │   ├── access.log              # Nginx-style access log
    │   └── app-debug.log           # Debug log
    │
    ├── app/                        # Sample app directory for backup demo
    │   ├── main.py
    │   ├── config.yaml
    │   └── utils/
    │       └── helpers.py
    │
    └── backups/                    # Where backups get stored
```

## How It Works

1. **Bot Server**: `bot.py` starts a FastAPI server that handles incoming Telegram webhook events.

2. **AutonomousAgent**: The agent loads its personality from `workspace/AGENTS.md`, its identity from `workspace/SOUL.md`, and any accumulated memory from `workspace/memory/`.

3. **Telegram Interface**: `TelegramInterface` in `CHAT` mode wraps the agent, maintaining conversation context across messages for a natural back-and-forth experience.

4. **Tool Execution**: The agent has access to filesystem tools (read, list, write files within the workspace) and shell execution capabilities to run system commands.

5. **Webhook Delivery**: ngrok tunnels requests from Telegram's servers to your local bot server, enabling development without a public IP.

## Security Notes

- The agent is sandboxed to the `workspace/` directory — file operations outside it are blocked.
- Set `TELEGRAM_USER_ID` in `.env` to restrict the bot to your account only.
- The agent uses `trash` over `rm` by default (defined in `AGENTS.md`).

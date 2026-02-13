# 🛠️ DevOps Agent — Telegram-Controlled Sysadmin Bot

> "I built a bot that manages my server from Telegram — and it only took 50 lines of Python."

A Telegram bot powered by Upsonic's `AutonomousAgent` that can read logs, check disk usage,
create backups, and run shell commands — all from your phone.

## Architecture

```
You (Telegram) → Telegram API → ngrok tunnel → FastAPI (port 8000) → Upsonic AutonomousAgent → workspace/
```

## Stack

| Tool     | Role                                      |
|----------|-------------------------------------------|
| Upsonic  | AutonomousAgent with filesystem + shell   |
| Telegram | Chat interface (via BotFather)            |
| ngrok    | Expose localhost to the internet          |

---

## 🗂️ Project Structure

```
devops_telegram_bot/
├── bot.py                          # Main bot server (~50 lines)
├── .env                            # API keys (you fill this in)
├── .env.example                    # Template for .env
├── requirements.txt                # Python dependencies
├── setup.sh                        # One-command setup script
│
└── workspace/                      # Agent's sandboxed home
    ├── AGENTS.md                   # Agent personality & behavior
    ├── SOUL.md                     # Agent identity
    ├── USER.md                     # Who the user is
    ├── memory/                     # Agent's daily memory logs
    │
    ├── logs/                       # Fake logs for demo
    │   ├── error.log               # Application error log
    │   ├── access.log              # Nginx-style access log
    │   └── app-debug.log           # Debug log (large file)
    │
    ├── app/                        # Fake app directory for backup demo
    │   ├── main.py
    │   ├── config.yaml
    │   └── utils/
    │       └── helpers.py
    │
    └── backups/                    # Where backups get stored
```

---

## 🚀 Setup Roadmap

### Step 1: Create the Telegram Bot (3 min)

1. Open Telegram → search **@BotFather** → send `/newbot`
2. Pick a name: `DevOps Agent`
3. Pick a username: `your_devops_agent_bot`
4. **Copy the bot token**
5. Search **@userinfobot** → send any message → **copy your user ID**

### Step 2: Start ngrok (2 min)

```bash
# Install ngrok: https://ngrok.com/download
ngrok config add-authtoken YOUR_NGROK_TOKEN
ngrok http 8000
```

Copy the `https://xxxx.ngrok-free.app` URL.

### Step 3: Configure environment (1 min)

```bash
cp .env.example .env
# Edit .env with your actual values:
#   TELEGRAM_BOT_TOKEN=...
#   TELEGRAM_WEBHOOK_URL=https://xxxx.ngrok-free.app
#   OPENAI_API_KEY=...
```

### Step 4: Install & Run (2 min)

```bash
# Option A: with uv (recommended)
uv venv && source .venv/bin/activate
uv pip install -r requirements.txt
uv run bot.py

# Option B: with pip
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python bot.py
```

### Step 5: Demo It 🎬

Open Telegram and send these messages to your bot:

| Message                                          | What happens                                    |
|--------------------------------------------------|-------------------------------------------------|
| `Check disk usage`                               | Agent runs `df -h`, returns formatted result    |
| `Find all log files larger than 50KB`            | Agent searches workspace, lists matching files  |
| `Create a backup of the app directory`           | Agent tars `app/` into `backups/`, confirms     |
| `Read the last 20 lines of error.log and tell me what's wrong` | Agent reads + analyzes log content |
| `List all running processes using port 8000`     | Agent runs shell command, returns results       |
| `Show me the app config`                         | Agent reads `config.yaml`, explains it          |

---

## 🔒 Security Notes

- The agent is **sandboxed** to the `workspace/` directory
- File operations outside workspace are **blocked**
- Use `TELEGRAM_USER_ID` to lock the bot to your account only
- The agent uses `trash` over `rm` by default (defined in AGENTS.md)

import os
from dotenv import load_dotenv
from upsonic import AutonomousAgent
from upsonic.interfaces import InterfaceManager, TelegramInterface, InterfaceMode

load_dotenv()

# Create an autonomous agent with DevOps workspace
# It auto-loads AGENTS.md, SOUL.md, and memory from the workspace
agent = AutonomousAgent(
    model="anthropic/claude-sonnet-4-5",
    workspace=os.path.join(os.path.dirname(__file__), "workspace"),
)


# Wire it up to Telegram in CHAT mode (remembers conversation context)
telegram = TelegramInterface(
    agent=agent,
    bot_token=os.getenv("TELEGRAM_BOT_TOKEN"),
    webhook_url=os.getenv("TELEGRAM_WEBHOOK_URL"),
    mode=InterfaceMode.CHAT,
    reset_command="/reset",
    parse_mode="Markdown"
)

# Serve it
manager = InterfaceManager(interfaces=[telegram])
manager.serve(host="0.0.0.0", port=8000)

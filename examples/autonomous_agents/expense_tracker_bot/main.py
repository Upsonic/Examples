"""
Expense Tracker Telegram Bot

An AutonomousAgent connected to Telegram that extracts text from receipt
photos using OCR and tracks expenses in the workspace. The agent's behavior
is defined in workspace/AGENTS.md — it knows how to parse receipts, manage
the CSV, and generate summaries on its own.
"""

import os
from dotenv import load_dotenv
from upsonic import AutonomousAgent
from upsonic.interfaces import InterfaceManager, TelegramInterface, InterfaceMode

from tools import ocr_extract_text

load_dotenv()

agent = AutonomousAgent(
    model="anthropic/claude-sonnet-4-5",
    tools=[ocr_extract_text],
    workspace=os.path.join(os.path.dirname(__file__), "workspace"),
)

telegram = TelegramInterface(
    agent=agent,
    bot_token=os.getenv("TELEGRAM_BOT_TOKEN"),
    webhook_url=os.getenv("TELEGRAM_WEBHOOK_URL"),
    mode=InterfaceMode.CHAT,
    reset_command="/reset",
    parse_mode="Markdown",
)

manager = InterfaceManager(interfaces=[telegram])
manager.serve(host="0.0.0.0", port=8000)

"""
Expense Tracker Telegram Bot

An AutonomousAgent connected to Telegram that extracts text from receipt
photos using OCR, parses the data, and saves expenses to a CSV file.
Send a photo of a receipt and the bot handles the rest.
"""

import os
from dotenv import load_dotenv
from upsonic import AutonomousAgent
from upsonic.interfaces import InterfaceManager, TelegramInterface, InterfaceMode

from tools import ocr_extract_text, save_expense, get_monthly_summary

load_dotenv()

agent = AutonomousAgent(
    model="anthropic/claude-sonnet-4-5",
    tools=[ocr_extract_text, save_expense, get_monthly_summary],
    system_prompt="""You are an expense tracking bot. Your job: extract text from receipt/invoice photos via OCR and save to CSV.

WORKFLOW: When user sends an image, execute these steps IN ORDER:

STEP 1: Call ocr_extract_text (no parameters needed, auto-detects image)

STEP 2: Parse OCR text and extract:
  - date: Invoice date in YYYY-MM-DD (convert 14.02.2026 → 2026-02-14)
  - amount: Total as float (convert 415,20 → 415.20)
  - merchant: Store/vendor/bank name
  - category: Pick ONE from: Market, Restoran, Ulasim, Saglik, Fatura, Giyim, Teknoloji, Banka, Diger
  - ocr_confidence: Average confidence score from OCR output (0.0 to 1.0, e.g. 85% → 0.85)

STEP 3: Call save_expense with extracted data including ocr_confidence (no user_id needed, single shared CSV)

STEP 4: Reply with brief confirmation in Turkish

For summary requests ("summary", "report", "this month"), call get_monthly_summary.

CRITICAL RULES:
- ALWAYS call ocr_extract_text when you see an image - never describe/interpret images yourself
- NEVER reply before calling save_expense
- Date format MUST be YYYY-MM-DD
- Amount MUST be numeric (no TL symbol)
- Respond in English
- Keep replies short and concise""",
    workspace=os.path.join(os.path.dirname(__file__), "workspace"),
    enable_filesystem=False,
    enable_shell=False,
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

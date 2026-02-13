#!/bin/bash
# DevOps Agent — Quick Setup Script
# Run this once to get everything ready

set -e

echo "🛠️  DevOps Agent Setup"
echo "====================="

# Check prerequisites
command -v python3 >/dev/null 2>&1 || { echo "❌ Python 3 is required. Install it first."; exit 1; }
command -v ngrok >/dev/null 2>&1 || { echo "⚠️  ngrok not found. Install from https://ngrok.com/download"; }

# Create .env if it doesn't exist
if [ ! -f .env ]; then
    cp .env.example .env
    echo "📝 Created .env from template — edit it with your actual keys:"
    echo "   - TELEGRAM_BOT_TOKEN (from @BotFather)"
    echo "   - TELEGRAM_WEBHOOK_URL (from ngrok)"
    echo "   - OPENAI_API_KEY"
    echo ""
    echo "   Run: nano .env"
else
    echo "✅ .env already exists"
fi

# Install dependencies
echo ""
echo "📦 Installing dependencies..."
if command -v uv >/dev/null 2>&1; then
    uv venv 2>/dev/null || true
    uv pip install -r requirements.txt
else
    python3 -m venv .venv 2>/dev/null || true
    source .venv/bin/activate
    pip install -r requirements.txt
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "  1. Edit .env with your keys"
echo "  2. Start ngrok:  ngrok http 8000"
echo "  3. Update TELEGRAM_WEBHOOK_URL in .env with ngrok URL"
echo "  4. Run the bot:  uv run bot.py  (or python bot.py)"
echo ""
echo "Then open Telegram and start chatting with your bot! 🚀"

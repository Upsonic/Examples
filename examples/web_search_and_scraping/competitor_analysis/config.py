"""
Configuration hub for the Competitor Analysis Agent.

╔══════════════════════════════════════════════════════════════════╗
║  CUSTOMIZE THIS FILE to analyze YOUR competitors.               ║
║  Just update the URLs, industry, and focus areas below.         ║
╚══════════════════════════════════════════════════════════════════╝
"""

# ── Competitors to Analyze ───────────────────────────────────────
# Add the homepage URLs of the competitors you want to research.
# Each competitor is researched in its own agent call, so adding more
# competitors won't blow up context — it just takes proportionally longer.

COMPETITOR_URLS = [
    "https://langchain.com",
    "https://crewai.com",
    "https://docs.llamaindex.ai",
]

# ── Industry / Market Segment ────────────────────────────────────
# Helps the agent focus its analysis on the right context.

INDUSTRY = "AI Agent Frameworks"

# ── Analysis Focus Areas ─────────────────────────────────────────
# What aspects should the agent prioritize when analyzing competitors?
# These are passed to the agent's task description.

FOCUS_AREAS = [
    "Core features and capabilities",
    "Pricing model and tiers",
    "Target audience and positioning",
    "Developer experience and ease of use",
    "Integrations and ecosystem",
]

# ── Model Configuration ──────────────────────────────────────────
# Choose any model supported by Upsonic (OpenAI, Anthropic, etc.)

MODEL = "claude-sonnet-4-6"

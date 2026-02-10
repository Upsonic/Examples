"""
I Stopped Writing Changelogs. Here's What Writes Them Now.

Two agents, one pipeline: feed in `git log --oneline`, get back
a ready-to-post tweet. Agent A reads the commits and pulls out
what matters. Agent B turns that into something you'd actually post.

The context flows from A → B automatically.
No variable passing. No glue code. Just `mode="sequential"`.
"""

from upsonic import Agent, Task, Team

# ── Mock Input ───────────────────────────────────────────────────────────
# Simulate `git log --oneline -n 5` — swap this for real git log later.
RAW_COMMITS = """
a1b2c3d feat: added dark mode support across the entire UI
b2c3d4e feat: introduced smart caching layer — 3x faster dashboard loads
c3d4e5f Merge pull request #42 from team/perf-improvements
d4e5f6a fix: database connection timeout on heavy load
e5f6a7b fix: resolved race condition in real-time notifications
"""

# ── Agent A — The Tech Lead ──────────────────────────────────────────────
tech_lead = Agent(
    model="openai/gpt-5-mini",
    name="Tech Lead",
    role="Technical Summarizer",
    goal="Distill raw commit messages into a clear, developer-friendly summary that highlights user-facing value.",
    instructions=(
        "You will receive a batch of raw git commit messages. "
        "Ignore anything tagged 'chore' or 'docs' — those are housekeeping. "
        "Focus on 'feat' and 'fix' entries. For each one, explain: "
        "(1) what changed, and (2) why an end-user should care. "
        "Be concise but technical enough for a developer audience."
    ),
)

# ── Agent B — The Growth Hacker ──────────────────────────────────────────
growth_hacker = Agent(
    model="openai/gpt-4o",
    name="Growth Hacker",
    role="Developer Social Media Writer",
    goal="Turn technical summaries into dev-native Twitter/X posts that feel like a smart engineer sharing something useful, not a marketing department announcing it.",
    instructions=(
        "You will receive a technical summary produced by the previous agent. "
        "Write a SINGLE Twitter/X post (NOT a thread). Follow these rules strictly:\n\n"

        "TONE:\n"
        "- Write like a developer talking to other developers. Direct, no fluff.\n"
        "- Confident but understated. Never hype or exaggerate.\n"
        "- NEVER use phrases like 'Exciting news!', 'We're thrilled', 'Game-changer', "
        "'Just dropped', or any corporate marketing language.\n"
        "- Short punchy sentences. Let line breaks do the work.\n\n"

        "STRUCTURE (follow this layout):\n"
        "- Line 1: A calm, confident hook (one sentence). Can end with a single emoji like a rocket.\n"
        "- Blank line.\n"
        "- 2-3 short lines of context explaining what shipped and why it matters.\n"
        "- Blank line.\n"
        "- A bullet list of the key changes. Use - or emoji bullets (one emoji per line, e.g. a rocket, wrench, zap). "
        "Keep each bullet to one short line.\n"
        "- Blank line.\n"
        "- CTA: 'Link in the comments' or 'Changelog: [link]'\n\n"

        "EMOJI RULES:\n"
        "- Use emojis SPARINGLY and only with PURPOSE.\n"
        "- OK: single emoji at end of hook line, or one emoji per bullet as a visual marker.\n"
        "- NEVER: emoji chains, mid-sentence emojis, or more than one emoji in a row.\n"
        "- When in doubt, skip the emoji.\n\n"

        "ABSOLUTE DON'TS:\n"
        "- No hashtags (no #ProductUpdates, #TechNews, etc.).\n"
        "- No numbered thread format (no 1/3, 2/3, 3/3).\n"
        "- No 'we're excited/thrilled/proud' language.\n"
        "- Do NOT invent features. Only use what the technical summary provides.\n\n"

        "REFERENCE EXAMPLES (match this energy):\n\n"

        "Example A:\n"
        "We wrote a Medium post about agent standardization.\n\n"
        "Teams waste weeks starting agent projects, adding safety layers, "
        "and maintaining & deploying everything.\n\n"
        "Upsonic fixes this: same structure, same API, shared safety.\n\n"
        "Read how. Link in the comments.\n\n"

        "Example B:\n"
        "Upsonic v0.71.0 is live!\n"
        "We shipped these in this version:\n"
        "- Culture System & CultureManager\n"
        "- Simulation System (+built-in scenarios)\n"
        "- Smoke Test Makefile\n"
        "- Open-source friendly README\n"
        "- Direct LLM call metrics bug fix\n"
        "Link in the comments\n"
    ),
)

# ── The Sequential Team ─────────────────────────────────────────────────
team = Team(
    agents=[tech_lead, growth_hacker],
    mode="sequential",
)

# ── Tasks ────────────────────────────────────────────────────────────────
tasks = [
    Task(
        description=(
            f"Analyze the following raw git commit messages and produce "
            f"a concise technical summary of the meaningful, user-facing changes.\n\n"
            f"Raw commits:\n{RAW_COMMITS}"
        ),
        agent=tech_lead
    ),
    Task(
        description=(
            "Using the technical summary from the previous step, "
            "create a Twitter/X thread (3 tweets)"
            "that announce this week's product updates."
        ),
        agent=growth_hacker
    ),
]

team.print_do(tasks)

print(tasks[-1].response)
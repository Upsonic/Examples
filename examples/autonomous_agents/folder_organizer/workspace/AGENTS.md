# AGENTS.md - Your Workspace

This folder is home. Treat it that way.

Before doing anything else, read `memory/YYYY-MM-DD.md` (today + yesterday) for recent context. **If in MAIN SESSION** (direct chat with your human): Also read `MEMORY.md`. Don't ask permission. Just do it.


## Skills

Skills live in `skills/`. Each skill has its own folder with a `SKILL.md`. Read the relevant one before starting a task — skills can be combined.

**Available skills:**

- **folder_organization** — Semantically reorganizes a messy folder (e.g. Downloads) into a clean, navigable hierarchy. Use this whenever the user asks to classify, sort, clean up, or reorganize files and folders.

Structure:
```
skills/
└── <skill_name>/
    └── SKILL.md   ← how to use the skill
```



## Memory

You wake up fresh each session. These files are your continuity. Capture what matters — decisions, context, things to remember. Skip the secrets unless asked.

- **Daily notes:** `memory/YYYY-MM-DD.md` — raw session logs (create `memory/` if needed)
- **Long-term:** `MEMORY.md` — curated memories, like human long-term memory. **MAIN SESSION ONLY** — contains personal context that shouldn't leak to strangers (Discord, group chats, shared sessions)
- **Write it down** — mental notes don't survive restarts. Files do. When someone says "remember this" → write to file. When you learn a lesson → update AGENTS.md or the relevant skill. When you make a mistake → document it so future-you doesn't repeat it.
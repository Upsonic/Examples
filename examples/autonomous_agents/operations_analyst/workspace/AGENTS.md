---
summary: "Operations Analyst — delivery performance analysis and KPI visualization"
read_when:
  - Every session start
---

# AGENTS.md - Operations Analyst Workspace

This folder is home. Your data, reports, and charts live here.

## Every Session

Before doing anything else:

1. Read `SOUL.md` — this is who you are
2. Read `memory/YYYY-MM-DD.md` (today + yesterday) for recent context

Don't ask permission. Just do it.

## Memory

You wake up fresh each session. These files are your continuity:

- **Daily notes:** `memory/YYYY-MM-DD.md` (create `memory/` if needed) — log what you computed, what you found, what you wrote
- Use memory to pass context between tasks — if Task 1 wrote `KPI_REPORT.md`, Task 2 should know that

Capture decisions and findings. Skip noise.

## This Workspace Runs Two Tasks

You are called twice in sequence by the same agent runner:

**Task 1 — Analyst:**
- Read `shipment_data.csv`
- Decide which KPIs matter for delivery operations
- Compute them from the raw data
- Write `KPI_REPORT.md` — summary table, carrier breakdown, route analysis, commentary

**Task 2 — Visualizer:**
- Read `KPI_REPORT.md` and `shipment_data.csv`
- Use `run_python` to execute `matplotlib` code tailored to the KPIs in the report
- Use a white background with dark text for readability
- Save charts as PNGs to `charts/`
- Run the code directly — no need to write a `.py` file first

## Workspace Contents

| File / Dir | Owner | Purpose |
|---|---|---|
| `shipment_data.csv` | Source | Raw shipment records — never delete |
| `SOUL.md` | Config | Who you are |
| `KPI_REPORT.md` | Task 1 output | KPI tables + commentary |
| `visualize_kpis.py` | Task 2 output | Generated visualization script (optional) |
| `charts/` | Task 2 output | PNG charts |
| `memory/` | Agent | Session continuity |

## Rules

- Never delete `shipment_data.csv`, `SOUL.md`, or `AGENTS.md`
- Don't exfiltrate data. Ever.
- `trash` > `rm` (recoverable beats gone forever)
- When in doubt, ask.

## Tools

Write your own. Task 2's job is to produce `visualize_kpis.py` — that script is the tool, and you write it from scratch based on what Task 1 found.

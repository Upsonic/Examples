---
summary: "Expense Tracker — receipt OCR, expense logging, and monthly summaries"
read_when:
  - Every session start
---

# AGENTS.md - Expense Tracker Workspace

This folder is home. Your expense data and memory live here.

## Every Session

Before doing anything else:

1. Read `SOUL.md` — this is who you are
2. Read `memory/YYYY-MM-DD.md` (today + yesterday) for recent context

Don't ask permission. Just do it.

## Memory

You wake up fresh each session. These files are your continuity:

- **Daily notes:** `memory/YYYY-MM-DD.md` (create `memory/` if needed) — log what you processed, any issues, daily totals
- Use memory to track patterns — flag if a merchant shows up unusually often or amounts spike

Capture decisions and findings. Skip noise.

## Receipt Workflow

When a user sends a photo:

1. **OCR**: You MUST call the `ocr_extract_text` tool. Do NOT use any other method to read images. Do NOT try to interpret, describe, or analyze the image yourself. The `ocr_extract_text` tool is the ONLY way to read text from photos.
2. **Parse**: Extract from the OCR tool output:
   - `date` — invoice date in YYYY-MM-DD (convert `14.02.2026` → `2026-02-14`)
   - `amount` — total as a number (convert `415,20` → `415.20`, strip currency symbols)
   - `merchant` — store, vendor, or bank name
   - `category` — pick ONE: Groceries, Restaurant, Transportation, Health, Bills, Clothing, Technology, Banking, Other
   - `ocr_confidence` — average confidence from OCR output (e.g. 85% → `0.85`)
3. **Duplicate check**: Read `expenses.csv`, check if same date + amount + merchant already exists. If so, warn the user instead of saving
4. **Save**: Append a new row to `expenses.csv`
5. **Confirm**: Reply with what was saved and the monthly running total

## expenses.csv Format

The CSV lives at `expenses.csv` in this workspace. Create it with headers on first use.

```
date,amount,merchant,category,description,ocr_confidence,created_at
2026-02-14,415.20,Migros,Groceries,,0.92,2026-02-14T18:30:00
```

| Column | Type | Description |
|---|---|---|
| `date` | string | Invoice date (YYYY-MM-DD) |
| `amount` | float | Total amount |
| `merchant` | string | Store/vendor name |
| `category` | string | One of the categories above |
| `description` | string | Optional note |
| `ocr_confidence` | float | 0.0 to 1.0 |
| `created_at` | string | ISO timestamp when saved |

## Summary Requests

When the user asks for a summary ("summary", "report", "this month"):

1. Read `expenses.csv`
2. Filter by the requested month (default: current month)
3. Group by category, compute totals and percentages
4. Reply with a clean breakdown and grand total

## Workspace Contents

| File / Dir | Owner | Purpose |
|---|---|---|
| `expenses.csv` | Agent | All expense records — append only |
| `SOUL.md` | Config | Who you are |
| `AGENTS.md` | Config | This file — your behavior |
| `memory/` | Agent | Session continuity |

## Rules

- **For ANY image: call `ocr_extract_text` tool. No exceptions. No alternatives.**
- Never delete `expenses.csv`, `SOUL.md`, or `AGENTS.md`
- Date format is always YYYY-MM-DD
- Amounts are always numeric (no currency symbols in CSV)
- Keep replies short and concise
- Respond in English

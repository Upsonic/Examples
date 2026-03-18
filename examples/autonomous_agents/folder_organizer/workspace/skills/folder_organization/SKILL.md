# Skill: Folder Organization

Semantically reorganize a messy folder (e.g. Downloads) into a clean, navigable structure.

---

## Task

**Goal:** Survey all files and subfolders, infer their purpose from name/type/context, then move them into a meaningful folder hierarchy — without deleting anything.

### Steps

1. **Survey** — run `tree -L 3 <target_dir>` (or equivalent) to get a full picture of what exists.
2. **Classify** — group files by semantic category. Use file names, extensions, and folder hints together. Common categories:
   - `photos/` — JPG, JPEG, PNG, HEIC personal photos
   - `videos/` — MP4, MOV raw footage and personal recordings
   - `videos/edited/` — files with `_edited` suffix or clearly post-processed
   - `audio/` — WAV, AIFF, MP3 music and sound files
   - `documents/` — PDF, DOCX, TXT general documents
   - `documents/official/` — student records, invoices, IDs, agendas
   - `design/` — SVG, logo PNGs, brand assets
   - `code/` — Python scripts, HTML, JS, config files
   - `code/<project-name>/` — when scripts clearly belong to a project (e.g. queue API scripts)
   - `archives/` — ZIP, RAR, DMG installers
   - `projects/<name>/` — self-contained project folders (e.g. `randomaf Project`, `devops-bot-telegram`)
3. **Plan** — before moving anything, output a proposed structure as a tree. Wait for confirmation if in an interactive session; proceed autonomously otherwise.
4. **Move** — execute moves. Preserve existing subfolders that are already well-named (e.g. `Instructions-how-to-work-with-queue/` → `code/queue-api/`).
5. **Log** — write a `REORGANIZATION_LOG.md` in the target directory listing every move made: `original path → new path`.

### Rules

- **Never delete files.** Only move.
- Duplicates (e.g. `YDXJ0387.JPG` and `YDXJ0387 (1).JPG`) go into the same folder; do not resolve them.
- Keep related files together — if several scripts share a project context, group them under one subfolder.
- Prefer semantic names over technical ones: `documents/official/` not `pdfs/`.
- When uncertain about a file's category, default to the most generic fitting bucket (e.g. `documents/`).

---

## Example Output Structure

```
Downloads/
├── photos/
│   ├── YDXJ0387.JPG
│   └── IMG_4665.JPEG
├── videos/
│   ├── raw/
│   │   ├── YDXJ0406.MP4
│   │   └── part_1.MP4
│   └── edited/
│       ├── part_3_edited.mov
│       └── jump_edited.mov
├── audio/
│   ├── MiniminiminiZalim.wav
│   └── Tronish Aviara.aiff
├── documents/
│   ├── official/
│   │   ├── öğrenci_belgesi.pdf
│   │   └── İrem_Öztimur_Document (1).pdf
│   └── Enhancing Memory in Alzheimer's and Dementia Using.docx
├── design/
│   ├── logo.svg
│   └── Logo Design for PromptSpace.png
├── code/
│   └── queue-api/
│       ├── push_call_into_queue.py
│       └── remove_call_in_queue.py
├── archives/
│   ├── prompt-library-app.zip
│   └── API updated.rar
├── projects/
│   └── randomaf Project/
└── REORGANIZATION_LOG.md
```

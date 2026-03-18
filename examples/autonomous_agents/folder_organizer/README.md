# Folder Organizer

An autonomous agent that semantically reorganizes any messy folder into a clean, navigable structure — using only a one-line task and a skill file.

Drop your files into `workspace/unorganized_folder/`, run the agent, and get a logically grouped hierarchy back. No hardcoded sorting rules — the agent reads the `folder_organization` skill and reasons about what goes where based on file names, types, and context. A good use case is your Downloads folder, which tends to accumulate a mix of photos, code, documents, and archives over time.

## Features

- **Semantic Classification**: Groups files by purpose, not just extension — photos, videos, audio, documents, code, design assets, and archives each get their own place
- **Skill-Driven Behavior**: Agent behavior is defined in `workspace/skills/folder_organization/SKILL.md` — change the skill, change the behavior
- **Reorganization Log**: Writes `REORGANIZATION_LOG.md` inside the folder with every original → new path move
- **Non-Destructive**: Never deletes files, only moves them

## Prerequisites

- Python 3.10+
- Anthropic API key

## Installation

1. **Navigate to this directory**:
   ```bash
   cd examples/autonomous_agents/folder_organizer
   ```

2. **Install dependencies**:
   ```bash
   uv venv && source .venv/bin/activate
   uv pip install -r requirements.txt
   ```

3. **Set up environment variables**:
   ```bash
   cp .env.example .env
   ```
   Edit `.env`:
   ```
   ANTHROPIC_API_KEY=your-api-key
   ```

## Usage

1. Drop your files into `workspace/unorganized_folder/`
2. Run the agent:
   ```bash
   uv run main.py
   ```

The agent surveys the folder, classifies each file semantically, moves them into a structured hierarchy, and writes a log.

## Project Structure

```
folder_organizer/
├── main.py                              # Agent setup and task
├── requirements.txt                     # Python dependencies
├── .env.example                         # Template for .env
│
└── workspace/                           # Agent's sandboxed home
    ├── AGENTS.md                        # Agent behavior and skill index
    ├── unorganized_folder/              # Drop your messy files here
    │   └── REORGANIZATION_LOG.md        # Created after the agent runs
    └── skills/
        └── folder_organization/
            └── SKILL.md                 # How the agent categorizes files
```

## How It Works

1. **Task**: `main.py` gives the agent a single instruction — `"Organize the unorganized_folder."`.

2. **Skill Lookup**: The agent reads `AGENTS.md`, finds the `folder_organization` skill, and loads `SKILL.md`.

3. **Survey**: The agent runs `tree` on the target folder to map all files and subfolders.

4. **Classify**: It groups files semantically — by name, extension, and context — into categories like `photos/`, `videos/edited/`, `code/<project>/`, `documents/official/`, etc.

5. **Move & Log**: Files are moved into the new structure. A `REORGANIZATION_LOG.md` records every move made.

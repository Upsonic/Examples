"""
Folder Organizer — Autonomous Agent Example

Semantically reorganizes any messy folder into a clean, navigable structure.
Drop files into workspace/unorganized_folder/ and run this script.
The agent reads the folder_organization skill and classifies everything by purpose.
"""

import os
from dotenv import load_dotenv
from upsonic import AutonomousAgent, Task

load_dotenv()

agent = AutonomousAgent(
    model="anthropic/claude-sonnet-4-6",
    workspace=os.path.join(os.path.dirname(__file__), "workspace"),
)

classification_task = Task("Organize the unorganized_folder.")


if __name__ == "__main__":
    agent.print_do(classification_task)


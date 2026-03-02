"""
Operations Analysis with Upsonic AutonomousAgent (two-task pipeline)

Task 1 (Analyst):    reads shipment_data.csv, decides KPIs, writes KPI_REPORT.md
Task 2 (Visualizer): reads KPI_REPORT.md, runs matplotlib code via run_python, produces charts

One agent. Two tasks. Fully autonomous.
"""

import os
from upsonic import AutonomousAgent, Task

WORKSPACE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "workspace")

print(f"Workspace: {WORKSPACE}")

agent = AutonomousAgent(
    model="anthropic/claude-sonnet-4-5",
    workspace=WORKSPACE,
)

analyst_task = Task(
    "Read shipment_data.csv. Identify the KPIs that matter most for delivery operations — "
    "on-time rate, carrier performance, route delays, cost efficiency. Compute each from the raw data. "
    "Write KPI_REPORT.md with a summary table, per-carrier breakdown, and a "
    "## Agent Commentary section with your analysis and recommendations."
)

visualizer_task = Task(
    "Read KPI_REPORT.md and shipment_data.csv. Based on the KPIs in the report, use run_python "
    "to execute matplotlib code that creates one chart per key metric. "
    "Use a white background with dark text for readability. Save all charts as PNGs to the charts/ directory. "
    "Do not write a .py file — run the code directly."
)

if __name__ == "__main__":
    print("\n-- Task 1: Analyst ----------------------------------------")
    agent.print_do(analyst_task)

    print("\n-- Task 2: Visualizer -------------------------------------")
    agent.print_do(visualizer_task)

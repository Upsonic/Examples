"""
Task description builder for loan covenant monitoring.

Constructs the instruction-only task description. Actual data
(loan agreement, financial data) is provided via Task.context.
"""

from __future__ import annotations

from typing import Optional, List


def build_covenant_monitoring_task(
    company_name: str,
    reporting_period: str,
    focus_areas: Optional[List[str]] = None,
) -> str:
    """Build the instruction task description for the covenant monitoring team.

    Args:
        company_name: Name of the borrower company.
        reporting_period: Period under analysis (e.g. "Q4 2025").
        focus_areas: Optional list of priority areas to emphasize.

    Returns:
        Formatted task description string containing only instructions.
    """
    focus_text: str = ""
    if focus_areas:
        focus_list: str = "\n".join([f"   - {area}" for area in focus_areas])
        focus_text = f"\n\nPRIORITY FOCUS AREAS:\n{focus_list}"

    task_description: str = (
        f"Perform comprehensive covenant compliance monitoring for {company_name} "
        f"for the reporting period {reporting_period}.\n\n"
        f"You have been provided the full loan agreement document and financial data "
        f"as context. Use them to complete the following deliverables:\n\n"
        f"REQUIRED DELIVERABLES:\n"
        f"1. Extract all financial covenants from the loan agreement, including "
        f"names, formulas, thresholds applicable to {reporting_period}, constraint types "
        f"(maximum or minimum), and testing frequencies\n"
        f"2. Calculate all required financial ratios using the financial data and the "
        f"calculation tools (do NOT compute manually)\n"
        f"3. Evaluate compliance status for each covenant (compliant, near_breach, or "
        f"breached) using the compliance evaluation tool\n"
        f"4. Produce an overall risk assessment with a numerical risk score (0-100) "
        f"and risk level\n"
        f"5. Write a concise executive summary highlighting any breaches or near-breaches "
        f"and their business implications\n"
        f"6. Provide specific, actionable next steps for remediation where needed, "
        f"referencing cure provisions from the agreement if applicable"
        f"{focus_text}"
    )

    return task_description

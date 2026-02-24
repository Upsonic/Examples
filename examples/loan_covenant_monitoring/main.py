"""
Main entry point for Loan Covenant Monitoring Agent.

This module provides the async entry point "main" that coordinates
the comprehensive loan covenant monitoring process.
"""

from __future__ import annotations

import asyncio
import json
from pathlib import Path
from typing import Dict, Any, Optional, List

from upsonic import Task

try:
    from .team import create_covenant_monitoring_team
    from .task_builder import build_covenant_monitoring_task
    from .schemas import CovenantMonitoringReport
except ImportError:
    from team import create_covenant_monitoring_team
    from task_builder import build_covenant_monitoring_task
    from schemas import CovenantMonitoringReport


async def main(inputs: Dict[str, Any]) -> Dict[str, Any]:
    """
    Main async function for loan covenant monitoring.

    Args:
        inputs: Dictionary containing:
            - company_name: Name of the borrower company (required)
            - reporting_period: Period being monitored, e.g. "Q4 2025" (required)
            - loan_agreement_path: Path to loan agreement text file (required)
            - financial_data_path: Path to financial data JSON file (required)
            - focus_areas: Optional list of priority focus areas
            - enable_memory: Whether to enable memory persistence (default: True)
            - model: Optional model identifier (default: "anthropic/claude-sonnet-4-5")
            - print: If True, do() prints; if False, print_do() does not. Respects UPSONIC_AGENT_PRINT env.

    Returns:
        Dictionary containing the covenant monitoring report and metadata.
    """
    company_name: str = inputs.get("company_name", "")
    if not company_name:
        raise ValueError("company_name is required in inputs")

    reporting_period: str = inputs.get("reporting_period", "")
    if not reporting_period:
        raise ValueError("reporting_period is required in inputs")

    loan_agreement_path: str = inputs.get("loan_agreement_path", "")
    if not loan_agreement_path:
        raise ValueError("loan_agreement_path is required in inputs")

    financial_data_path: str = inputs.get("financial_data_path", "")
    if not financial_data_path:
        raise ValueError("financial_data_path is required in inputs")

    focus_areas: Optional[List[str]] = inputs.get("focus_areas")
    enable_memory: bool = inputs.get("enable_memory", True)
    model: str = inputs.get("model", "anthropic/claude-sonnet-4-5")
    print_flag: Optional[bool] = inputs.get("print")

    team = create_covenant_monitoring_team(
        model=model,
        enable_memory=enable_memory,
        print=print_flag,
    )

    task_description: str = build_covenant_monitoring_task(
        company_name=company_name,
        reporting_period=reporting_period,
        focus_areas=focus_areas,
    )

    task: Task = Task(
        task_description,
        context=[loan_agreement_path, financial_data_path],
    )

    result = await team.do_async(task)

    if isinstance(result, CovenantMonitoringReport):
        report_dict: Dict[str, Any] = result.model_dump()
    else:
        report_dict = {"raw_output": str(result)}

    return {
        "company_name": company_name,
        "reporting_period": reporting_period,
        "report": report_dict,
        "monitoring_completed": True,
    }


if __name__ == "__main__":
    import sys

    script_dir: Path = Path(__file__).parent

    test_inputs: Dict[str, Any] = {
        "company_name": "GlobalTech Manufacturing Inc.",
        "reporting_period": "Q4 2025",
        "loan_agreement_path": str(script_dir / "data" / "loan_agreement.txt"),
        "financial_data_path": str(script_dir / "data" / "financial_data.json"),
        "focus_areas": [
            "Leverage ratio trending toward covenant limit",
            "Debt service capacity under current cash flow",
        ],
        "enable_memory": False,
        "model": "anthropic/claude-sonnet-4-5",
        "print": True,
    }

    if len(sys.argv) > 1:
        try:
            with open(sys.argv[1], "r") as f:
                test_inputs = json.load(f)
        except Exception as e:
            print(f"Error loading JSON file: {e}")
            print("Using default test inputs")

    try:
        result = asyncio.run(main(test_inputs))

        print("\n" + "=" * 80)
        print("Loan Covenant Monitoring Report - Completed")
        print("=" * 80)
        print(f"\nCompany: {result['company_name']}")
        print(f"Period:  {result['reporting_period']}")
        print(f"Status:  {'Completed' if result.get('monitoring_completed') else 'Failed'}")

        report: Dict[str, Any] = result.get("report", {})

        if "executive_summary" in report:
            print(f"\n--- Executive Summary ---\n{report['executive_summary']}")

        if "risk_assessment" in report:
            risk: Dict[str, Any] = report["risk_assessment"]
            print("\n--- Risk Assessment ---")
            print(f"  Risk Score : {risk.get('overall_risk_score', 'N/A')} / 100")
            print(f"  Risk Level : {risk.get('risk_level', 'N/A')}")
            print(
                f"  Breached: {risk.get('breached_count', 0)} | "
                f"Near Breach: {risk.get('near_breach_count', 0)} | "
                f"Compliant: {risk.get('compliant_count', 0)}"
            )

        if "compliance_results" in report:
            print("\n--- Covenant Compliance Details ---")
            print("-" * 60)
            status_symbols: Dict[str, str] = {
                "compliant": "[OK]",
                "near_breach": "[!!]",
                "breached": "[XX]",
            }
            for covenant in report["compliance_results"]:
                symbol: str = status_symbols.get(covenant.get("status", ""), "[??]")
                print(
                    f"  {symbol} {covenant.get('covenant_name', 'Unknown')}: "
                    f"{covenant.get('actual_value', 'N/A')} vs "
                    f"{covenant.get('threshold', 'N/A')} "
                    f"(headroom: {covenant.get('headroom_percentage', 'N/A')}%)"
                )

        if "next_steps" in report:
            print("\n--- Recommended Next Steps ---")
            for i, step in enumerate(report["next_steps"], 1):
                print(f"  {i}. {step}")

        print("\n" + "=" * 80)
        print("\nFull report (JSON):")
        print(json.dumps(report, indent=2, default=str))

    except Exception as e:
        print(f"\nError during execution: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

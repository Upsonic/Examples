"""
Specialized agent creation functions for covenant monitoring.

Each function creates an Agent with a specific domain expertise:
- Covenant extraction from legal documents
- Financial ratio calculation using custom tools
- Compliance assessment and risk evaluation
"""

from __future__ import annotations

from typing import List, Callable

from upsonic import Agent

try:
    from .tools import (
        calculate_leverage_ratio,
        calculate_interest_coverage_ratio,
        calculate_current_ratio,
        calculate_debt_service_coverage_ratio,
        calculate_tangible_net_worth,
        evaluate_covenant_compliance,
    )
except ImportError:
    from tools import (
        calculate_leverage_ratio,
        calculate_interest_coverage_ratio,
        calculate_current_ratio,
        calculate_debt_service_coverage_ratio,
        calculate_tangible_net_worth,
        evaluate_covenant_compliance,
    )


def create_covenant_extractor_agent(model: str = "openai/gpt-4o-mini") -> Agent:
    """Create a specialist agent for extracting covenant definitions from loan agreements.

    Args:
        model: Model identifier for the agent.

    Returns:
        Configured Agent for covenant extraction.
    """
    return Agent(
        model=model,
        name="Covenant Extractor",
        role="Legal Document Analyst specializing in commercial loan agreements",
        goal=(
            "Extract and structure every financial covenant definition from the loan "
            "agreement, including precise thresholds, formulas, constraint types, and "
            "testing frequencies"
        ),
        system_prompt=(
            "You are a specialist in analyzing commercial loan agreements and credit "
            "facility documentation. Your task is to:\n"
            "- Identify every financial covenant in the provided agreement text\n"
            "- Extract the exact numerical threshold for the applicable period\n"
            "- Determine the formula specified for each covenant\n"
            "- Classify each as 'maximum' (must not exceed) or 'minimum' (must not fall below)\n"
            "- Note the testing frequency (quarterly TTM, point-in-time, etc.)\n\n"
            "CRITICAL: Only extract values explicitly stated in the document. Never infer "
            "or estimate thresholds. Use the exact step-down schedule applicable to the "
            "reporting period being analyzed."
        ),
        education="JD in Corporate Law, CFA Charterholder",
        work_experience="15 years in leveraged finance documentation and loan agreement analysis",
        tool_call_limit=5,
    )


def create_financial_calculator_agent(model: str = "openai/gpt-4o-mini") -> Agent:
    """Create a specialist agent for computing financial ratios using calculation tools.

    Args:
        model: Model identifier for the agent.

    Returns:
        Configured Agent with financial calculation tools.
    """
    financial_tools: List[Callable[..., dict]] = [
        calculate_leverage_ratio,
        calculate_interest_coverage_ratio,
        calculate_current_ratio,
        calculate_debt_service_coverage_ratio,
        calculate_tangible_net_worth,
    ]

    return Agent(
        model=model,
        name="Financial Calculator",
        role="Quantitative Financial Analyst",
        goal=(
            "Calculate all required financial ratios and metrics from raw financial "
            "data using the provided calculation tools, producing an audit-ready trail"
        ),
        system_prompt=(
            "You are a quantitative analyst responsible for computing financial ratios "
            "needed for covenant compliance testing.\n\n"
            "RULES:\n"
            "1. ALWAYS use the provided calculation tools. NEVER compute ratios manually.\n"
            "2. Use exact figures from the financial data. Do not round or adjust inputs.\n"
            "3. For each ratio, identify the correct input values from the financial data "
            "and call the corresponding tool.\n"
            "4. Report all results with their component values for audit trail.\n\n"
            "Available tools:\n"
            "- calculate_leverage_ratio(total_debt, ebitda)\n"
            "- calculate_interest_coverage_ratio(ebit, interest_expense)\n"
            "- calculate_current_ratio(current_assets, current_liabilities)\n"
            "- calculate_debt_service_coverage_ratio(net_operating_income, total_debt_service)\n"
            "- calculate_tangible_net_worth(total_assets, total_liabilities, intangible_assets)"
        ),
        education="MS in Financial Engineering, FRM Certification",
        work_experience="10 years in credit risk analytics and financial modeling",
        tools=financial_tools,
        tool_call_limit=15,
    )


def create_risk_assessor_agent(model: str = "openai/gpt-4o-mini") -> Agent:
    """Create a specialist agent for evaluating covenant compliance and risk.

    Args:
        model: Model identifier for the agent.

    Returns:
        Configured Agent with the compliance evaluation tool.
    """
    compliance_tools: List[Callable[..., dict]] = [evaluate_covenant_compliance]

    return Agent(
        model=model,
        name="Risk Assessor",
        role="Credit Risk Officer",
        goal=(
            "Evaluate covenant compliance status for each covenant using the evaluation "
            "tool, calculate overall risk score, and provide actionable recommendations"
        ),
        system_prompt=(
            "You are a senior credit risk officer evaluating loan covenant compliance.\n\n"
            "PROCESS:\n"
            "1. For each covenant, call evaluate_covenant_compliance with:\n"
            "   - covenant_name: the covenant's name\n"
            "   - actual_value: the calculated ratio/metric value\n"
            "   - threshold: the covenant threshold from the agreement\n"
            "   - constraint_type: 'maximum' or 'minimum'\n"
            "2. Analyze headroom percentage for each to assess comfort level\n"
            "3. Compute overall risk score using this methodology:\n"
            "   - Start at 0 (no risk)\n"
            "   - Add 30 points per breached covenant\n"
            "   - Add 15 points per near-breach covenant\n"
            "   - Risk levels: 0-20=Low, 21-40=Moderate, 41-70=High, 71-100=Critical\n"
            "4. Provide specific, actionable recommendations for any covenant that is "
            "near breach or breached, considering both immediate remediation and "
            "structural solutions\n\n"
            "Consider cure provisions and grace periods when formulating recommendations."
        ),
        education="MBA in Finance, PRM Certification",
        work_experience="12 years in commercial banking credit risk and portfolio monitoring",
        tools=compliance_tools,
        tool_call_limit=15,
    )

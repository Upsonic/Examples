"""
Custom financial calculation tools for covenant monitoring.

Provides standalone calculation and compliance evaluation functions
used by the financial calculator and risk assessor agents.
"""

from __future__ import annotations

from typing import Dict, Any


def calculate_leverage_ratio(total_debt: float, ebitda: float) -> Dict[str, Any]:
    """Calculate the Leverage Ratio (Total Debt / EBITDA).

    Args:
        total_debt: Total outstanding funded debt in dollars.
        ebitda: Earnings Before Interest, Taxes, Depreciation, and Amortization in dollars.

    Returns:
        Dictionary with ratio value, formula used, and input components.
    """
    if ebitda <= 0:
        return {
            "ratio_name": "Leverage Ratio",
            "value": float("inf"),
            "formula": "Total Funded Debt / EBITDA",
            "components": {"total_debt": total_debt, "ebitda": ebitda},
            "warning": "EBITDA is zero or negative; ratio is undefined",
        }

    ratio: float = round(total_debt / ebitda, 4)
    return {
        "ratio_name": "Leverage Ratio",
        "value": ratio,
        "formula": "Total Funded Debt / EBITDA",
        "components": {"total_debt": total_debt, "ebitda": ebitda},
    }


def calculate_interest_coverage_ratio(ebit: float, interest_expense: float) -> Dict[str, Any]:
    """Calculate the Interest Coverage Ratio (EBIT / Interest Expense).

    Args:
        ebit: Earnings Before Interest and Taxes in dollars.
        interest_expense: Total interest expense in dollars.

    Returns:
        Dictionary with ratio value, formula used, and input components.
    """
    if interest_expense <= 0:
        return {
            "ratio_name": "Interest Coverage Ratio",
            "value": float("inf"),
            "formula": "EBIT / Interest Expense",
            "components": {"ebit": ebit, "interest_expense": interest_expense},
            "warning": "Interest expense is zero or negative; ratio is undefined",
        }

    ratio: float = round(ebit / interest_expense, 4)
    return {
        "ratio_name": "Interest Coverage Ratio",
        "value": ratio,
        "formula": "EBIT / Interest Expense",
        "components": {"ebit": ebit, "interest_expense": interest_expense},
    }


def calculate_current_ratio(current_assets: float, current_liabilities: float) -> Dict[str, Any]:
    """Calculate the Current Ratio (Current Assets / Current Liabilities).

    Args:
        current_assets: Total current assets in dollars.
        current_liabilities: Total current liabilities in dollars.

    Returns:
        Dictionary with ratio value, formula used, and input components.
    """
    if current_liabilities <= 0:
        return {
            "ratio_name": "Current Ratio",
            "value": float("inf"),
            "formula": "Current Assets / Current Liabilities",
            "components": {"current_assets": current_assets, "current_liabilities": current_liabilities},
            "warning": "Current liabilities is zero or negative; ratio is undefined",
        }

    ratio: float = round(current_assets / current_liabilities, 4)
    return {
        "ratio_name": "Current Ratio",
        "value": ratio,
        "formula": "Current Assets / Current Liabilities",
        "components": {"current_assets": current_assets, "current_liabilities": current_liabilities},
    }


def calculate_debt_service_coverage_ratio(
    net_operating_income: float,
    total_debt_service: float,
) -> Dict[str, Any]:
    """Calculate the Debt Service Coverage Ratio (Net Operating Income / Total Debt Service).

    Args:
        net_operating_income: EBITDA minus unfunded capex minus cash taxes paid, in dollars.
        total_debt_service: Sum of scheduled principal payments and interest payments, in dollars.

    Returns:
        Dictionary with ratio value, formula used, and input components.
    """
    if total_debt_service <= 0:
        return {
            "ratio_name": "Debt Service Coverage Ratio",
            "value": float("inf"),
            "formula": "Net Operating Income / Total Debt Service",
            "components": {
                "net_operating_income": net_operating_income,
                "total_debt_service": total_debt_service,
            },
            "warning": "Total debt service is zero or negative; ratio is undefined",
        }

    ratio: float = round(net_operating_income / total_debt_service, 4)
    return {
        "ratio_name": "Debt Service Coverage Ratio",
        "value": ratio,
        "formula": "Net Operating Income / Total Debt Service",
        "components": {
            "net_operating_income": net_operating_income,
            "total_debt_service": total_debt_service,
        },
    }


def calculate_tangible_net_worth(
    total_assets: float,
    total_liabilities: float,
    intangible_assets: float,
) -> Dict[str, Any]:
    """Calculate Tangible Net Worth (Total Assets - Total Liabilities - Intangible Assets).

    Args:
        total_assets: Total assets in dollars.
        total_liabilities: Total liabilities in dollars.
        intangible_assets: Intangible assets including goodwill, patents, trademarks, in dollars.

    Returns:
        Dictionary with calculated value, formula used, and input components.
    """
    tangible_net_worth: float = round(total_assets - total_liabilities - intangible_assets, 2)
    return {
        "metric_name": "Tangible Net Worth",
        "value": tangible_net_worth,
        "formula": "Total Assets - Total Liabilities - Intangible Assets",
        "components": {
            "total_assets": total_assets,
            "total_liabilities": total_liabilities,
            "intangible_assets": intangible_assets,
        },
    }


def evaluate_covenant_compliance(
    covenant_name: str,
    actual_value: float,
    threshold: float,
    constraint_type: str,
) -> Dict[str, Any]:
    """Evaluate whether a financial covenant is compliant, near breach, or breached.

    Uses a 10 percent buffer zone to determine near-breach status.

    Args:
        covenant_name: Name of the covenant being evaluated.
        actual_value: The actual calculated ratio or metric value.
        threshold: The covenant threshold from the loan agreement.
        constraint_type: Either 'maximum' (value must be at or below threshold) or 'minimum' (value must be at or above threshold).

    Returns:
        Dictionary with compliance status, headroom percentage, and assessment details.
    """
    near_breach_buffer: float = 0.10

    if constraint_type.lower() not in ("maximum", "minimum"):
        return {
            "covenant_name": covenant_name,
            "error": f"Invalid constraint_type '{constraint_type}'. Must be 'maximum' or 'minimum'.",
        }

    if constraint_type.lower() == "maximum":
        if actual_value > threshold:
            status: str = "breached"
            headroom_pct: float = round(-((actual_value - threshold) / threshold) * 100, 2)
        elif actual_value > threshold * (1 - near_breach_buffer):
            status = "near_breach"
            headroom_pct = round(((threshold - actual_value) / threshold) * 100, 2)
        else:
            status = "compliant"
            headroom_pct = round(((threshold - actual_value) / threshold) * 100, 2)
    else:
        if actual_value < threshold:
            status = "breached"
            headroom_pct = round(-((threshold - actual_value) / threshold) * 100, 2)
        elif actual_value < threshold * (1 + near_breach_buffer):
            status = "near_breach"
            headroom_pct = round(((actual_value - threshold) / threshold) * 100, 2)
        else:
            status = "compliant"
            headroom_pct = round(((actual_value - threshold) / threshold) * 100, 2)

    return {
        "covenant_name": covenant_name,
        "actual_value": actual_value,
        "threshold": threshold,
        "constraint_type": constraint_type,
        "status": status,
        "headroom_percentage": headroom_pct,
    }

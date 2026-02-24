"""
Output schemas for loan covenant monitoring agent.

Defines structured Pydantic models for type-safe outputs from the
covenant monitoring pipeline.
"""

from __future__ import annotations

from typing import List
from pydantic import BaseModel, Field


class CovenantDefinition(BaseModel):
    """A single financial covenant extracted from a loan agreement."""
    name: str
    description: str
    formula: str
    threshold: float
    constraint_type: str = Field(description="Either 'maximum' or 'minimum'")
    testing_frequency: str


class FinancialRatio(BaseModel):
    """A calculated financial ratio with audit trail."""
    name: str
    value: float
    formula_used: str
    components: dict[str, float]


class CovenantComplianceResult(BaseModel):
    """Compliance evaluation result for a single covenant."""
    covenant_name: str
    threshold: float
    actual_value: float
    status: str = Field(description="One of: 'compliant', 'near_breach', 'breached'")
    headroom_percentage: float = Field(description="Positive = buffer remaining, negative = extent of breach")
    explanation: str


class RiskAssessment(BaseModel):
    """Overall portfolio risk assessment across all covenants."""
    overall_risk_score: float = Field(ge=0.0, le=100.0)
    risk_level: str = Field(description="One of: 'low', 'moderate', 'high', 'critical'")
    total_covenants: int
    compliant_count: int
    near_breach_count: int
    breached_count: int
    key_concerns: List[str]
    recommended_actions: List[str]


class CovenantMonitoringReport(BaseModel):
    """Final comprehensive covenant monitoring report."""
    company_name: str
    reporting_period: str
    report_date: str
    covenants_extracted: List[CovenantDefinition]
    calculated_ratios: List[FinancialRatio]
    compliance_results: List[CovenantComplianceResult]
    risk_assessment: RiskAssessment
    executive_summary: str
    detailed_findings: str
    next_steps: List[str]

"""
Output schemas for company research and sales strategy agent.

Defines structured Pydantic models for type-safe outputs from different
analysis components.
"""

from __future__ import annotations

from typing import List, Optional
from pydantic import BaseModel


class CompanyResearchOutput(BaseModel):
    """Structured output for company research."""
    company_name: str
    company_description: str
    industry: str
    key_products_services: List[str]
    target_markets: List[str]
    competitive_advantages: List[str]
    recent_news_highlights: List[str]
    website: Optional[str] = None
    headquarters: Optional[str] = None
    employee_count: Optional[str] = None


class IndustryAnalysisOutput(BaseModel):
    """Structured output for industry analysis."""
    industry_name: str
    market_size: str
    growth_trends: List[str]
    key_players: List[str]
    emerging_technologies: List[str]
    regulatory_environment: str
    market_opportunities: List[str]
    market_threats: List[str]


class FinancialAnalysisOutput(BaseModel):
    """Structured output for financial analysis."""
    company_symbol: Optional[str] = None
    current_price: Optional[str] = None
    market_cap: Optional[str] = None
    pe_ratio: Optional[str] = None
    revenue_trend: str
    profitability_status: str
    financial_strengths: List[str]
    financial_concerns: List[str]
    analyst_sentiment: Optional[str] = None


class SalesStrategyOutput(BaseModel):
    """Structured output for sales strategy."""
    target_segments: List[str]
    value_propositions: List[str]
    sales_channels: List[str]
    pricing_strategy: str
    competitive_positioning: str
    key_messaging: List[str]
    sales_process_recommendations: List[str]
    success_metrics: List[str]


class ComprehensiveReportOutput(BaseModel):
    """Final comprehensive report combining all analyses."""
    company_research: CompanyResearchOutput
    industry_analysis: IndustryAnalysisOutput
    financial_analysis: FinancialAnalysisOutput
    sales_strategy: SalesStrategyOutput
    executive_summary: str
    key_insights: List[str]
    recommended_next_steps: List[str]


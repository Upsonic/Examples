"""
Pydantic schemas for structured competitive analysis output.

Customize these models to change what data the agent extracts.
Add or remove fields based on what matters for YOUR competitive landscape.
"""

from typing import List, Optional
from pydantic import BaseModel, Field


class CompetitorProfile(BaseModel):
    """Profile of a single competitor extracted from their website."""

    name: str = Field(description="Company or product name")
    website: str = Field(description="Primary website URL")
    tagline: str = Field(description="Main tagline or value proposition from the website")
    description: str = Field(
        description="Brief description of what they do (2-3 sentences)"
    )
    key_features: List[str] = Field(
        description="List of main features or capabilities (up to 8)"
    )
    pricing_model: str = Field(
        description=(
            "Pricing model summary (e.g. 'Freemium with Pro at $20/mo', "
            "'Enterprise only - contact sales', 'Open source with paid cloud')"
        )
    )
    pricing_tiers: Optional[List[str]] = Field(
        default=None,
        description="List of pricing tiers if available (e.g. 'Free', 'Pro $20/mo', 'Enterprise custom')",
    )
    target_audience: str = Field(
        description="Who is this product for? (e.g. 'SMB developers', 'Enterprise DevOps teams')"
    )
    differentiators: List[str] = Field(
        description="What makes them stand out? Key selling points (up to 5)"
    )


class CompetitiveAnalysisReport(BaseModel):
    """Full competitive analysis report comparing multiple competitors."""

    industry: str = Field(description="The industry or market segment being analyzed")
    analysis_summary: str = Field(
        description="Executive summary of the competitive landscape (3-5 sentences)"
    )
    competitors: List[CompetitorProfile] = Field(
        description="Detailed profiles for each competitor analyzed"
    )
    feature_comparison: str = Field(
        description=(
            "Markdown table comparing key features across all competitors. "
            "Rows = features, Columns = competitors, Cells = ✅/❌/partial"
        )
    )
    pricing_comparison: str = Field(
        description=(
            "Markdown table comparing pricing across all competitors. "
            "Include tiers, starting prices, and free tier availability"
        )
    )
    key_insights: List[str] = Field(
        description=(
            "Strategic insights and observations about the competitive landscape (5-8 bullet points)"
        )
    )
    opportunities: List[str] = Field(
        description="Gaps or opportunities identified in the market (3-5 bullet points)"
    )

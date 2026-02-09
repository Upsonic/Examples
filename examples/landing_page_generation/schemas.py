"""
Output schemas for landing page generation agent.

Defines structured Pydantic models for type-safe outputs from different
landing page generation components.
"""

from __future__ import annotations

from typing import List, Optional
from pydantic import BaseModel


class ContentOutput(BaseModel):
    """Structured output for landing page content."""
    headline: str
    subheadline: str
    value_proposition: str
    key_benefits: List[str]
    call_to_action_primary: str
    call_to_action_secondary: Optional[str] = None
    feature_highlights: List[str]
    social_proof: Optional[str] = None
    footer_text: Optional[str] = None


class DesignOutput(BaseModel):
    """Structured output for landing page design recommendations."""
    color_scheme: str
    primary_color: str
    secondary_color: str
    typography_style: str
    layout_structure: str
    visual_elements: List[str]
    spacing_recommendations: str
    mobile_responsiveness: str


class SEOOutput(BaseModel):
    """Structured output for SEO optimization."""
    meta_title: str
    meta_description: str
    focus_keywords: List[str]
    header_structure: List[str]
    alt_text_suggestions: List[str]
    url_structure: str
    schema_markup: Optional[str] = None


class LandingPageOutput(BaseModel):
    """Final comprehensive landing page specification."""
    content: ContentOutput
    design: DesignOutput
    seo: SEOOutput
    implementation_notes: str
    priority_features: List[str]

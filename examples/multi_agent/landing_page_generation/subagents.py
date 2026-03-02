"""
Specialized subagent creation functions.

Each function creates a specialized agent for a specific domain:
- Content writing
- Design recommendations
- SEO optimization
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from upsonic import Agent

if TYPE_CHECKING:
    pass


def create_content_writer_subagent(model: str = "openai/gpt-4o-mini") -> Agent:
    """Create specialized subagent for landing page content creation.
    
    Args:
        model: Model identifier for the subagent
        
    Returns:
        Configured Agent instance for content writing
    """
    return Agent(
        model=model,
        name="content-writer",
        role="Landing Page Content Specialist",
        goal="Create compelling, conversion-focused copy for landing pages including headlines, value propositions, CTAs, and feature highlights",
        system_prompt="""You are an expert copywriter specializing in high-converting landing pages. Your role is to create 
        compelling, clear, and persuasive copy that drives action. Focus on:
        - Attention-grabbing headlines that communicate value immediately
        - Clear value propositions that differentiate the offering
        - Benefit-focused content that addresses customer pain points
        - Strong, action-oriented call-to-action buttons
        - Social proof and trust-building elements
        - Concise, scannable content that works on mobile devices
        
        Write copy that is specific, benefit-driven, and speaks directly to the target audience. Keep it concise and 
        conversion-focused.""",
        tool_call_limit=10,
    )


def create_designer_subagent(model: str = "openai/gpt-4o-mini") -> Agent:
    """Create specialized subagent for landing page design recommendations.
    
    Args:
        model: Model identifier for the subagent
        
    Returns:
        Configured Agent instance for design recommendations
    """
    return Agent(
        model=model,
        name="designer",
        role="Landing Page Design Specialist",
        goal="Provide design recommendations for landing pages including color schemes, typography, layout, and visual elements",
        system_prompt="""You are a UI/UX designer specializing in high-converting landing pages. Your role is to recommend 
        design elements that enhance user experience and conversion rates. Focus on:
        - Color schemes that align with brand and psychology
        - Typography that improves readability and hierarchy
        - Layout structures that guide user attention
        - Visual elements that support the message
        - Spacing and whitespace for clarity
        - Mobile-first responsive design principles
        
        Provide practical, implementable design recommendations that balance aesthetics with conversion optimization.""",
        tool_call_limit=10,
    )


def create_seo_specialist_subagent(model: str = "openai/gpt-4o-mini") -> Agent:
    """Create specialized subagent for SEO optimization.
    
    Args:
        model: Model identifier for the subagent
        
    Returns:
        Configured Agent instance for SEO optimization
    """
    return Agent(
        model=model,
        name="seo-specialist",
        role="SEO Optimization Specialist",
        goal="Optimize landing pages for search engines with proper meta tags, keywords, structure, and technical SEO elements",
        system_prompt="""You are an SEO expert specializing in landing page optimization. Your role is to ensure landing pages 
        are discoverable and rank well in search engines. Focus on:
        - Compelling meta titles and descriptions
        - Strategic keyword placement and density
        - Proper header hierarchy (H1, H2, H3)
        - Alt text for images
        - Clean URL structures
        - Schema markup for rich snippets
        - Mobile-friendly optimization
        
        Balance SEO requirements with user experience and conversion goals. Avoid keyword stuffing.""",
        tool_call_limit=10,
    )

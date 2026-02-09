"""
Task description builder for landing page generation.

Constructs comprehensive task descriptions based on input parameters.
"""

from __future__ import annotations

from typing import Optional


def build_landing_page_task(
    product_name: str,
    target_audience: str,
    primary_goal: str,
    key_features: Optional[list[str]] = None,
    brand_tone: Optional[str] = None,
) -> str:
    """Build comprehensive task description for landing page generation.
    
    Args:
        product_name: Name of the product or service
        target_audience: Description of the target audience
        primary_goal: Primary conversion goal (e.g., "sign up", "purchase", "download")
        key_features: Optional list of key features to highlight
        brand_tone: Optional brand tone (e.g., "professional", "friendly", "bold")
        
    Returns:
        Comprehensive task description string
    """
    features_text = ""
    if key_features:
        features_list = "\n".join([f"       - {feature}" for feature in key_features])
        features_text = f"\n    Key features to highlight:\n{features_list}"
    
    tone_text = f"\n    Brand tone: {brand_tone}" if brand_tone else ""
    
    task_description = f"""Generate a landing page image for {product_name} targeting {target_audience} with the goal of {primary_goal}.
    
    Coordinate with specialized subagents to gather content, design, and SEO specifications, then create a detailed visual description 
    and generate the final landing page image. The image should incorporate all gathered specifications including headlines, 
    value propositions, color schemes, layout structure, and visual elements.{features_text}{tone_text}"""
    
    return task_description

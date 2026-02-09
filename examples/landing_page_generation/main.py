"""
Main entry point for Landing Page Generation Agent.

This module provides the entry point that coordinates
the comprehensive landing page generation process.
"""

from __future__ import annotations

from typing import Dict, Any

from upsonic import Task
from upsonic.utils.image import save_image_to_folder, create_images_folder
try:
    from .orchestrator import create_orchestrator_agent
    from .task_builder import build_landing_page_task
except ImportError:
    from orchestrator import create_orchestrator_agent
    from task_builder import build_landing_page_task


async def main(inputs: Dict[str, Any]) -> Dict[str, Any]:
    """
    Main function for landing page generation.
    
    Args:
        inputs: Dictionary containing:
            - product_name: Name of the product or service (required)
            - target_audience: Description of target audience (required)
            - primary_goal: Primary conversion goal (required)
            - key_features: Optional list of key features to highlight
            - brand_tone: Optional brand tone (default: "professional")
            - enable_memory: Whether to enable memory persistence (default: True)
            - storage_path: Optional path for SQLite storage (default: "landing_page_generation.db")
            - model: Optional model identifier (default: "openai/gpt-4o")
    
    Returns:
        Dictionary containing comprehensive landing page specification
    """
    product_name = inputs.get("product_name")
    if not product_name:
        raise ValueError("product_name is required in inputs")
    
    target_audience = inputs.get("target_audience")
    if not target_audience:
        raise ValueError("target_audience is required in inputs")
    
    primary_goal = inputs.get("primary_goal")
    if not primary_goal:
        raise ValueError("primary_goal is required in inputs")
    
    key_features = inputs.get("key_features")
    brand_tone = inputs.get("brand_tone", "professional")
    enable_memory = inputs.get("enable_memory", True)
    storage_path = inputs.get("storage_path")
    model = inputs.get("model", "openai-responses/gpt-4o")
    output_folder = inputs.get("output_folder", "landing_page_images")
    
    orchestrator = create_orchestrator_agent(
        model=model,
        storage_path=storage_path,
        enable_memory=enable_memory,
    )
    
    task_description = build_landing_page_task(
        product_name=product_name,
        target_audience=target_audience,
        primary_goal=primary_goal,
        key_features=key_features,
        brand_tone=brand_tone,
    )
    
    task = Task(task_description)
    
    result = await orchestrator.do_async(task)
    
    if not isinstance(result, bytes):
        raise ValueError(f"Expected image bytes, got {type(result)}")
    
    create_images_folder(output_folder)
    safe_product_name = "".join(c for c in product_name if c.isalnum() or c in (' ', '-', '_')).strip().replace(' ', '_')
    image_path = save_image_to_folder(
        image_data=result,
        folder_path=output_folder,
        filename=f"{safe_product_name}_landing_page.png",
        is_base64=False
    )
    
    return {
        "product_name": product_name,
        "image_path": image_path,
        "generation_completed": True,
    }


if __name__ == "__main__":
    import asyncio
    import json
    import sys
    
    test_inputs = {
        "product_name": "AI Writing Assistant",
        "target_audience": "Content creators and marketers who need to produce high-quality content quickly",
        "primary_goal": "sign up for free trial",
        "key_features": [
            "AI-powered content generation",
            "Multiple writing templates",
            "Real-time collaboration",
            "SEO optimization suggestions"
        ],
        "brand_tone": "friendly and professional",
        "enable_memory": False,
        "storage_path": None,
        "model": "openai-responses/gpt-4o",
        "output_folder": "landing_page_images",
    }
    
    if len(sys.argv) > 1:
        try:
            with open(sys.argv[1], "r") as f:
                test_inputs = json.load(f)
        except Exception as e:
            print(f"Error loading JSON file: {e}")
            print("Using default test inputs")
    
    async def run_main():
        try:
            result = await main(test_inputs)
            
            print("\n" + "=" * 80)
            print("Landing Page Generation Completed Successfully!")
            print("=" * 80)
            print(f"\nProduct: {result.get('product_name')}")
            print(f"Generation Status: {'Completed' if result.get('generation_completed') else 'Failed'}")
            print(f"\nImage saved to: {result.get('image_path', 'N/A')}")
            
        except Exception as e:
            print(f"\n❌ Error during execution: {e}")
            import traceback
            traceback.print_exc()
            sys.exit(1)
    
    asyncio.run(run_main())

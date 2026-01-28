"""
Main entry point for Company Research and Sales Strategy Agent.

This module provides the entry point that coordinate
the comprehensive research and strategy development process.
"""

from __future__ import annotations

from typing import Dict, Any

from upsonic import Task
try:
    from .orchestrator import create_orchestrator_agent
    from .task_builder import build_research_task
    from .schemas import ComprehensiveReportOutput
except ImportError:
    from orchestrator import create_orchestrator_agent
    from task_builder import build_research_task
    from schemas import ComprehensiveReportOutput


def main(inputs: Dict[str, Any]) -> Dict[str, Any]:
    """
    Main function for company research and sales strategy development.
    
    Args:
        inputs: Dictionary containing:
            - company_name: Name of the target company (required)
            - company_symbol: Optional stock symbol for financial analysis
            - industry: Optional industry name for focused analysis
            - enable_memory: Whether to enable memory persistence (default: True)
            - storage_path: Optional path for SQLite storage (default: "company_research.db")
            - model: Optional model identifier (default: "openai/gpt-4o")
    
    Returns:
        Dictionary containing comprehensive research report
    """
    company_name = inputs.get("company_name")
    if not company_name:
        raise ValueError("company_name is required in inputs")
    
    company_symbol = inputs.get("company_symbol")
    industry = inputs.get("industry")
    enable_memory = inputs.get("enable_memory", True)
    storage_path = inputs.get("storage_path")
    model = inputs.get("model", "openai/gpt-4o")
    
    orchestrator = create_orchestrator_agent(
        model=model,
        storage_path=storage_path,
        enable_memory=enable_memory,
    )
    
    task_description = build_research_task(
        company_name=company_name,
        company_symbol=company_symbol,
        industry=industry,
    )
    
    task = Task(task_description, response_format=ComprehensiveReportOutput)
    
    result = orchestrator.do(task)
    
    report_dict = result.model_dump(mode='json')
    
    return {
        "company_name": company_name,
        "comprehensive_report": report_dict,
        "research_completed": True,
    }


async def amain(inputs: Dict[str, Any]) -> Dict[str, Any]:
    """
    Async main function for company research and sales strategy development.
    
    Args:
        inputs: Dictionary containing:
            - company_name: Name of the target company (required)
            - company_symbol: Optional stock symbol for financial analysis
            - industry: Optional industry name for focused analysis
            - enable_memory: Whether to enable memory persistence (default: True)
            - storage_path: Optional path for SQLite storage (default: "company_research.db")
            - model: Optional model identifier (default: "openai/gpt-4o")
    
    Returns:
        Dictionary containing comprehensive research report
    """
    company_name = inputs.get("company_name")
    if not company_name:
        raise ValueError("company_name is required in inputs")
    
    company_symbol = inputs.get("company_symbol")
    industry = inputs.get("industry")
    enable_memory = inputs.get("enable_memory", True)
    storage_path = inputs.get("storage_path")
    model = inputs.get("model", "openai/gpt-4o")
    
    orchestrator = create_orchestrator_agent(
        model=model,
        storage_path=storage_path,
        enable_memory=enable_memory,
    )
    
    task_description = build_research_task(
        company_name=company_name,
        company_symbol=company_symbol,
        industry=industry,
    )
    
    task = Task(task_description, response_format=ComprehensiveReportOutput)
    
    result = await orchestrator.do_async(task)
    
    report_dict = result.model_dump(mode='json')
    
    return {
        "company_name": company_name,
        "comprehensive_report": report_dict,
        "research_completed": True,
    }


if __name__ == "__main__":
    import json
    import sys
    
    test_inputs = {
        "company_name": "Microsoft",
        "company_symbol": None,
        "industry": "Artificial Intelligence",
        "enable_memory": False,
        "storage_path": None,
        "model": "openai/gpt-4o-mini",
    }
    
    if len(sys.argv) > 1:
        try:
            with open(sys.argv[1], "r") as f:
                test_inputs = json.load(f)
        except Exception as e:
            print(f"Error loading JSON file: {e}")
            print("Using default test inputs")
    
    try:
        result = main(test_inputs)
        
        print("\n" + "=" * 80)
        print("Research Completed Successfully!")
        print("=" * 80)
        print(f"\nCompany: {result.get('company_name')}")
        print(f"Research Status: {'Completed' if result.get('research_completed') else 'Failed'}")
        report = result.get('comprehensive_report', {})
        if isinstance(report, dict):
            print(f"\nComprehensive Report:\n{json.dumps(report, indent=2, default=str)}")
        else:
            print(f"\nComprehensive Report:\n{report}")
        
    except Exception as e:
        print(f"\n❌ Error during execution: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


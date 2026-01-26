"""
Main entry point for AI Governance Lexicon Agent.

This module provides the entry point that coordinates the research 
and explanation generation for AI governance terms.
"""

from __future__ import annotations

from typing import Dict, Any

from upsonic import Task

try:
    from .agent import create_lexicon_agent
    from .schemas import LexiconEntry
except ImportError:
    from agent import create_lexicon_agent
    from schemas import LexiconEntry


def main(inputs: Dict[str, Any]) -> Dict[str, Any]:
    """
    Main function for AI Lexicon agent.
    
    Args:
        inputs: Dictionary containing:
            - term: The AI governance term to explain (required)
            - model: Optional model identifier (default: "openai/gpt-4o")
            - max_search_results: Optional max search results (default: 10)
    
    Returns:
        Dictionary containing the detailed explanation and FAQs
    """
    term = inputs.get("term")
    if not term:
        # Fallback for "keyword" if "term" is not provided
        term = inputs.get("keyword")
        
    if not term:
        raise ValueError("term or keyword is required in inputs")
    
    model = inputs.get("model", "openai/gpt-4o")
    max_search_results_input = inputs.get("max_search_results", 10)
    max_search_results: int = int(max_search_results_input) if max_search_results_input is not None else 10
    
    # Initialize the agent
    agent = create_lexicon_agent(
        model=model,
        max_search_results=max_search_results
    )
    
    # Define the task
    task_description = f"""
    Research and explain the AI governance term: "{term}"
    
    1. Search for current definitions, frameworks, and best practices.
    2. Provide a brief but comprehensive explanation.
    3. Generate 3-5 relevant FAQs with answers.
    """
    
    task = Task(task_description, response_format=LexiconEntry)
    
    # Execute the agent
    result = agent.do(task)
    
    # Return result as dictionary
    return result.model_dump(mode='json')


async def amain(inputs: Dict[str, Any]) -> Dict[str, Any]:
    """
    Async main function for AI Lexicon agent.
    
    Args:
        inputs: Dictionary containing:
            - term: The AI governance term to explain (required)
            - model: Optional model identifier (default: "openai/gpt-4o")
            - max_search_results: Optional max search results (default: 10)
    
    Returns:
        Dictionary containing the detailed explanation and FAQs
    """
    term = inputs.get("term")
    if not term:
        # Fallback for "keyword" if "term" is not provided
        term = inputs.get("keyword")
        
    if not term:
        raise ValueError("term or keyword is required in inputs")
    
    model = inputs.get("model", "openai/gpt-4o")
    max_search_results_input = inputs.get("max_search_results", 10)
    max_search_results: int = int(max_search_results_input) if max_search_results_input is not None else 10
    
    # Initialize the agent
    agent = create_lexicon_agent(
        model=model,
        max_search_results=max_search_results
    )
    
    # Define the task
    task_description = f"""
    Research and explain the AI governance term: "{term}"
    
    1. Search for current definitions, frameworks, and best practices.
    2. Provide a brief but comprehensive explanation.
    3. Generate 3-5 relevant FAQs with answers.
    """
    
    task = Task(task_description, response_format=LexiconEntry)
    
    # Execute the agent
    result = await agent.do_async(task)
    
    # Return result as dictionary
    return result.model_dump(mode='json')


if __name__ == "__main__":
    import json
    import sys
    
    test_inputs = {
        "term": "Gap analysis for AI governance",
        "model": "openai/gpt-4o",
    }
    
    if len(sys.argv) > 1:
        try:
            with open(sys.argv[1], "r") as f:
                file_inputs = json.load(f)
                if file_inputs:
                    test_inputs = file_inputs
        except Exception as e:
            print(f"Error loading JSON file: {e}")
            print("Using default test inputs")
    
    try:
        print(f"Researching term: {test_inputs.get('term') or test_inputs.get('keyword')}...")
        result = main(test_inputs)
        
        print("\n" + "=" * 80)
        print("LEXICON ENTRY GENERATED")
        print("=" * 80)
        
        print(f"\n{result.get('term')}:")
        print(f"\n{result.get('brief_explanation')}")
        
        print(f"\nFAQs:")
        for i, faq in enumerate(result.get('faqs', []), 1):
            print(f"\nQ{i}: {faq.get('question')}")
            print(f"A{i}: {faq.get('answer')}")
            
    except Exception as e:
        print(f"\n❌ Error during execution: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


"""
Tools for the AI Lexicon Agent.

This module provides web search tools for researching AI governance terms
and retrieving comprehensive information from the internet.
"""

from __future__ import annotations

from typing import Callable


def get_search_tool(max_results: int = 10) -> Callable:
    """
    Get the DuckDuckGo search tool for researching AI terms.
    
    Args:
        max_results: Maximum number of search results to return
        
    Returns:
        A configured search tool function
    """
    from upsonic.tools.common_tools.duckduckgo import duckduckgo_search_tool
    
    return duckduckgo_search_tool(
        duckduckgo_client=None,
        max_results=max_results
    )


def get_all_tools(max_search_results: int = 10) -> list:
    """
    Get all tools configured for the AI Lexicon agent.
    
    Args:
        max_search_results: Maximum search results per query
        
    Returns:
        List of all configured tools
    """
    return [
        get_search_tool(max_results=max_search_results),
    ]

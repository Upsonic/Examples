"""
Agent configuration for the AI Lexicon Agent.

This module creates and configures the Upsonic Agent with 
appropriate tools and system prompts for AI governance term explanations.
"""

from __future__ import annotations

from typing import Optional

from upsonic import Agent

try:
    from .tools import get_all_tools
except ImportError:
    from tools import get_all_tools


LEXICON_SYSTEM_PROMPT = """You are an AI Governance Lexicon Expert. Your role is to provide comprehensive, 
accurate, and educational explanations of AI-related governance terms and concepts.

When given an AI governance term or concept, you must:

1. RESEARCH: Use the web search tool to find current, authoritative information about the term.
   Search for definitions, frameworks, best practices, and real-world applications.

2. EXPLAIN: Provide a detailed but accessible explanation that covers:
   - Clear definition of the term
   - Why it matters in AI governance
   - Key components or aspects
   - Practical applications and examples
   - Relationship to other governance concepts

3. FAQs: Generate 3-5 frequently asked questions that someone learning about this term 
   would likely have, along with comprehensive answers.

Your explanations should be:
- Accurate and well-researched (use search tools to verify information)
- Educational and accessible to both technical and non-technical audiences
- Practical with real-world examples when possible
- Current and up-to-date with latest industry practices

Always search the internet first to ensure your explanations are based on current 
best practices and authoritative sources."""


def create_lexicon_agent(
    model: str = "openai/gpt-4o",
    max_search_results: int = 10,
) -> Agent:
    """
    Create and configure the AI Lexicon agent.
    
    Args:
        model: The LLM model identifier to use
        max_search_results: Maximum search results per query
        
    Returns:
        Configured Agent instance ready for lexicon tasks
    """
    tools = get_all_tools(max_search_results=max_search_results)
    
    agent = Agent(
        name="AI Governance Lexicon Agent",
        model=model,
        system_prompt=LEXICON_SYSTEM_PROMPT,
    )
    
    agent.add_tools(tools)
    
    return agent

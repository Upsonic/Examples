"""
Specialized subagent creation functions.

Each function creates a specialized agent for a specific domain:
- Company research
- Industry analysis
- Financial analysis
- Sales strategy development
"""

from __future__ import annotations

import os
from typing import TYPE_CHECKING

from upsonic import Agent
from upsonic.tools.common_tools.duckduckgo import duckduckgo_search_tool
from upsonic.tools.common_tools.financial_tools import YFinanceTools
from upsonic.tools.common_tools.tavily import tavily_search_tool

if TYPE_CHECKING:
    pass


def create_research_subagent(model: str = "openai/gpt-4o-mini") -> Agent:
    """Create specialized subagent for company research.
    
    Args:
        model: Model identifier for the subagent
        
    Returns:
        Configured Agent instance for company research
    """
    ddg_search = duckduckgo_search_tool(duckduckgo_client=None, max_results=10)
    
    return Agent(
        model=model,
        name="company-researcher",
        role="Company Research Specialist",
        goal="Conduct comprehensive research on target companies including business model, products, markets, and competitive positioning",
        system_prompt="""You are an expert company researcher with deep knowledge of business analysis, 
        market research, and competitive intelligence. Your role is to gather comprehensive information 
        about companies including their business model, products/services, target markets, competitive 
        advantages, and recent developments. Use web search tools extensively to find current, accurate 
        information. Structure your findings clearly and cite sources when possible.""",
        tools=[ddg_search],
        tool_call_limit=15,
    )


def create_industry_analyst_subagent(model: str = "openai/gpt-4o-mini") -> Agent:
    """Create specialized subagent for industry analysis.
    
    Args:
        model: Model identifier for the subagent
        
    Returns:
        Configured Agent instance for industry analysis
    """
    tavily_api_key = os.getenv("TAVILY_API_KEY")
    tools = []
    
    if tavily_api_key:
        tavily_search = tavily_search_tool(tavily_api_key)
        tools.append(tavily_search)
    else:
        ddg_search = duckduckgo_search_tool(duckduckgo_client=None, max_results=10)
        tools.append(ddg_search)
    
    return Agent(
        model=model,
        name="industry-analyst",
        role="Industry Analysis Specialist",
        goal="Analyze industry trends, market dynamics, competitive landscape, and emerging opportunities",
        system_prompt="""You are a senior industry analyst with expertise in market research, trend analysis, 
        and competitive intelligence. Your role is to analyze industry trends, market size, growth patterns, 
        key players, emerging technologies, regulatory environment, opportunities, and threats. Provide 
        data-driven insights and strategic perspectives on industry dynamics.""",
        tools=tools,
        tool_call_limit=15,
    )


def create_financial_analyst_subagent(model: str = "openai/gpt-4o-mini") -> Agent:
    """Create specialized subagent for financial analysis.
    
    Args:
        model: Model identifier for the subagent
        
    Returns:
        Configured Agent instance for financial analysis
    """
    financial_tools = YFinanceTools(
        stock_price=True,
        company_info=True,
        analyst_recommendations=True,
        company_news=True,
        enable_all=True,
    )
    
    return Agent(
        model=model,
        name="financial-analyst",
        role="Financial Analysis Specialist",
        goal="Perform comprehensive financial analysis including stock performance, fundamentals, and analyst sentiment",
        system_prompt="""You are a financial analyst with expertise in company valuation, financial statement 
        analysis, and market research. Your role is to analyze financial data, stock performance, company 
        fundamentals, analyst recommendations, and market sentiment. Provide clear insights on financial 
        health, growth prospects, and investment considerations.""",
        tools=financial_tools.functions(),
        tool_call_limit=10,
    )


def create_sales_strategist_subagent(model: str = "openai/gpt-4o-mini") -> Agent:
    """Create specialized subagent for sales strategy development.
    
    Args:
        model: Model identifier for the subagent
        
    Returns:
        Configured Agent instance for sales strategy development
    """
    return Agent(
        model=model,
        name="sales-strategist",
        role="Sales Strategy Specialist",
        goal="Develop comprehensive, tailored sales strategies based on company research, industry analysis, and market insights",
        system_prompt="""You are a sales strategy expert with deep knowledge of B2B and B2C sales, 
        go-to-market strategies, and revenue generation. Your role is to develop tailored sales strategies 
        that align with company capabilities, market opportunities, and competitive positioning. Create 
        actionable strategies covering target segments, value propositions, sales channels, pricing, 
        messaging, and success metrics.""",
        tool_call_limit=5,
    )


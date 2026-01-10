"""
Task description builder for company research and sales strategy.

Constructs comprehensive task descriptions based on input parameters.
"""

from __future__ import annotations

from typing import Optional


def build_research_task(
    company_name: str,
    company_symbol: Optional[str] = None,
    industry: Optional[str] = None,
) -> str:
    """Build comprehensive task description for company research and sales strategy.
    
    Args:
        company_name: Name of the target company
        company_symbol: Optional stock symbol for financial analysis
        industry: Optional industry name for focused analysis
        
    Returns:
        Comprehensive task description string
    """
    task_description = f"""Conduct comprehensive research and develop a sales strategy for {company_name}.
    
    Requirements:
    1. **Company Research**: Use the 'company-researcher' subagent to gather comprehensive information about {company_name}:
       - Business model and core products/services
       - Target markets and customer segments
       - Competitive advantages and differentiators
       - Recent news and developments
       - Company website and headquarters information
    
    2. **Industry Analysis**: Use the 'industry-analyst' subagent to analyze the industry:
       - Market size and growth trends
       - Key players and competitive landscape
       - Emerging technologies and innovations
       - Regulatory environment
       - Market opportunities and threats
       {"- Focus on the " + industry + " industry" if industry else ""}
    
    3. **Financial Analysis**: {"Use the 'financial-analyst' subagent to analyze financial data" if company_symbol else "Note: No stock symbol provided, skip detailed financial analysis"}:
       {"- Stock symbol: " + company_symbol if company_symbol else ""}
       - Current stock price and market cap
       - Financial fundamentals and ratios
       - Analyst recommendations and sentiment
       - Recent financial news
    
    4. **Sales Strategy Development**: Use the 'sales-strategist' subagent to develop a tailored sales strategy:
       - Target customer segments
       - Value propositions
       - Recommended sales channels
       - Pricing strategy recommendations
       - Competitive positioning
       - Key messaging points
       - Sales process recommendations
       - Success metrics
    
    5. **Synthesis**: Create a comprehensive executive summary with:
       - Key insights from all analyses
       - Recommended next steps
       - Strategic recommendations
    
    Use the planning tool to break down this complex task into manageable steps. Execute subagent tasks 
    in parallel when possible to maximize efficiency. Ensure all findings are well-documented and 
    actionable."""
    
    return task_description


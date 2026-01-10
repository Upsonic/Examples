"""
Orchestrator agent creation and configuration.

Creates the main DeepAgent orchestrator that coordinates all specialized
subagents for comprehensive company research and sales strategy development.
"""

from __future__ import annotations

from typing import Optional

from upsonic.agent.deepagent import DeepAgent
from upsonic.db.database import SqliteDatabase

try:
    from .subagents import (
        create_research_subagent,
        create_industry_analyst_subagent,
        create_financial_analyst_subagent,
        create_sales_strategist_subagent,
    )
except ImportError:
    from subagents import (
        create_research_subagent,
        create_industry_analyst_subagent,
        create_financial_analyst_subagent,
        create_sales_strategist_subagent,
    )


def create_orchestrator_agent(
    model: str = "openai/gpt-4o",
    storage_path: Optional[str] = None,
    enable_memory: bool = True,
) -> DeepAgent:
    """Create the main orchestrator DeepAgent with all subagents.
    
    Args:
        model: Model identifier for the orchestrator agent
        storage_path: Optional path for SQLite storage database
        enable_memory: Whether to enable memory persistence
        
    Returns:
        Configured DeepAgent instance with all subagents
    """
    db = None
    memory = None
    
    if enable_memory:
        if storage_path is None:
            storage_path = "company_research.db"
        db = SqliteDatabase(
            db_file=storage_path,
            agent_sessions_table_name="agent_sessions",
            session_id="company_research_session",
            user_id="research_user",
            full_session_memory=True,
            summary_memory=True,
            model=model,
        )
        memory = db.memory
    
    subagents = [
        create_research_subagent(),
        create_industry_analyst_subagent(),
        create_financial_analyst_subagent(),
        create_sales_strategist_subagent(),
    ]
    
    orchestrator = DeepAgent(
        model=model,
        name="Company Research & Sales Strategy Orchestrator",
        role="Senior Business Strategy Consultant",
        goal="Orchestrate comprehensive company research, industry analysis, financial evaluation, and sales strategy development",
        system_prompt="""You are a senior business strategy consultant orchestrating a comprehensive 
        research and strategy development process. Your role is to:
        
        1. Coordinate specialized subagents to conduct deep research on target companies
        2. Analyze industry trends and competitive landscape
        3. Evaluate financial performance and market position
        4. Synthesize findings into actionable sales strategies
        
        Use the planning tool (write_todos) to break down complex research tasks. Delegate specific 
        research areas to specialized subagents. Synthesize all findings into a comprehensive report 
        with actionable insights and recommendations.
        
        Always use subagents for specialized tasks:
        - Use 'company-researcher' for company-specific research
        - Use 'industry-analyst' for industry and market analysis
        - Use 'financial-analyst' for financial data and stock analysis
        - Use 'sales-strategist' for sales strategy development
        
        Coordinate parallel execution when tasks are independent to maximize efficiency.""",
        memory=memory,
        subagents=subagents,
        enable_planning=True,
        enable_filesystem=True,
        tool_call_limit=30,
        debug=False,
    )
    
    return orchestrator


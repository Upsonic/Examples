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
    
    if enable_memory:
        if storage_path is None:
            storage_path = "company_research.db"
        db = SqliteDatabase(
            db_file=storage_path,
            session_table="agent_sessions",
            session_id="company_research_session",
            user_id="research_user",
            full_session_memory=True,
            summary_memory=True,
            model=model,
        )
    
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
        research and strategy development process. Your role is to plan the research process, coordinate 
        with specialized subagents to gather all necessary information, and synthesize findings into 
        actionable sales strategies and recommendations. Coordinate parallel execution when tasks are 
        independent to maximize efficiency.""",
        db=db,
        subagents=subagents,
        enable_planning=True,
        enable_filesystem=True,
        tool_call_limit=30,
        debug=False,
    )
    
    return orchestrator


"""
Orchestrator agent creation and configuration.

Creates the main DeepAgent orchestrator that coordinates all specialized
subagents for comprehensive landing page generation.
"""

from __future__ import annotations

from typing import Optional

from upsonic.agent.deepagent import DeepAgent
from upsonic.db.database import SqliteDatabase
from upsonic.tools.builtin_tools import ImageGenerationTool

try:
    from .subagents import (
        create_content_writer_subagent,
        create_designer_subagent,
        create_seo_specialist_subagent,
    )
except ImportError:
    from subagents import (
        create_content_writer_subagent,
        create_designer_subagent,
        create_seo_specialist_subagent,
    )


def create_orchestrator_agent(
    model: str = "openai-responses/gpt-4o",
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
            storage_path = "landing_page_generation.db"
        db = SqliteDatabase(
            db_file=storage_path,
            session_table="agent_sessions",
            session_id="landing_page_session",
            user_id="landing_page_user",
            full_session_memory=True,
            summary_memory=True,
            model=model,
        )
    
    subagents = [
        create_content_writer_subagent(),
        create_designer_subagent(),
        create_seo_specialist_subagent(),
    ]
    
    orchestrator = DeepAgent(
        model=model,
        name="Landing Page Generation Orchestrator",
        role="Senior Landing Page Strategist",
        goal="Plan and orchestrate landing page image generation by coordinating subagents and generating the final visual",
        system_prompt="""You are a senior landing page strategist orchestrating a landing page image generation process. 
        Your role is to plan the generation process, coordinate with specialized subagents to gather all necessary 
        specifications, synthesize the information into a detailed visual description, and generate the final landing 
        page image. Coordinate parallel execution when tasks are independent to maximize efficiency.""",
        db=db,
        subagents=subagents,
        tools=[ImageGenerationTool(size="1536x1024", quality="high", output_format="png")],
        enable_planning=True,
        enable_filesystem=True,
        tool_call_limit=25,
        debug=False,
    )
    
    return orchestrator

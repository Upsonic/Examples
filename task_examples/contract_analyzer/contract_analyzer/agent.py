from typing import Optional, List, Any

from upsonic import Agent, Task
from upsonic.storage.memory import Memory
from upsonic.storage.providers.in_memory import InMemoryStorage

from contract_analyzer.config import ContractAnalyzerConfig, default_config
from contract_analyzer.tools import ContractAnalyzerToolKit
from contract_analyzer.knowledge import create_legal_knowledge_base


def create_contract_analyzer_agent(
    config: Optional[ContractAnalyzerConfig] = None,
    session_id: Optional[str] = None,
    include_knowledge_base: bool = True,
    additional_tools: Optional[List[Any]] = None
) -> Agent:
    """
    Create a fully configured Contract Analyzer Agent.
    
    The agent is equipped with:
    - ContractAnalyzerToolKit for contract extraction and analysis
    - Legal KnowledgeBase for reference information (as a tool)
    - Session memory for conversation continuity
    - Specialized system prompt for legal analysis
    
    Args:
        config: Configuration settings. Uses default_config if not provided.
        session_id: Session ID for memory. Auto-generated if not provided.
        include_knowledge_base: Whether to include legal KB as a tool (default True).
        additional_tools: Extra tools to add to the agent.
        
    Returns:
        A configured Agent instance ready for contract analysis.
        
    Usage:
        ```python
        agent = create_contract_analyzer_agent()
        
        result = agent.do(Task(
            description="Analyze this contract: [contract text here]"
        ))
        ```
    """
    if config is None:
        config = default_config
    
    session = config.get_session_id(session_id)
    memory = Memory(
        storage=InMemoryStorage(),
        session_id=session,
        full_session_memory=True
    )
    
    tools: List[Any] = []
    
    contract_toolkit = ContractAnalyzerToolKit()
    tools.append(contract_toolkit)
    
    if include_knowledge_base:
        kb = create_legal_knowledge_base(config)
        tools.append(kb)
    
    if additional_tools:
        tools.extend(additional_tools)
    
    agent = Agent(
        model=config.model,
        name=config.agent_name,
        role=config.agent_role,
        goal=config.agent_goal,
        system_prompt=config.system_prompt,
        memory=memory,
        tools=tools,
        debug=config.debug,
        show_tool_calls=True
    )
    
    return agent


def create_analysis_task(
    contract_text: str,
    analysis_type: str = "full",
    specific_questions: Optional[List[str]] = None
) -> Task:
    """
    Create a task for contract analysis.
    
    Args:
        contract_text: The contract text to analyze.
        analysis_type: Type of analysis:
            - "full": Complete contract analysis
            - "summary": Executive summary only
            - "risk": Risk assessment focus
            - "extraction": Data extraction only
            - "custom": Custom questions
        specific_questions: Questions for "custom" analysis type.
        
    Returns:
        A configured Task for the analysis.
    """
    if analysis_type == "full":
        description = f"""Perform a comprehensive analysis of the following contract:

<contract>
{contract_text}
</contract>

Please provide:
1. Executive summary of the contract
2. All parties involved and their roles
3. Key dates (effective, termination, renewal)
4. Financial terms and payment obligations
5. Main obligations for each party
6. Risk assessment with recommendations

If you need reference information about standard contract clauses or legal terminology, 
use the search tool to query the legal knowledge base."""

    elif analysis_type == "summary":
        description = f"""Provide an executive summary of the following contract:

<contract>
{contract_text}
</contract>

Focus on the key points a business executive would need to know for a quick review."""

    elif analysis_type == "risk":
        description = f"""Perform a risk assessment of the following contract:

<contract>
{contract_text}
</contract>

Identify:
1. High-risk clauses requiring immediate attention
2. Medium-risk items to review
3. Unusual or non-standard terms
4. Missing protective clauses
5. Recommendations for negotiation

Use the legal knowledge base to reference standard risk indicators if needed."""

    elif analysis_type == "extraction":
        description = f"""Extract structured data from the following contract:

<contract>
{contract_text}
</contract>

Extract and organize:
1. All parties (names, roles, entity types)
2. All dates mentioned
3. All financial terms and amounts
4. All obligations for each party

Present the information in a structured format."""

    elif analysis_type == "custom" and specific_questions:
        questions_formatted = "\n".join(f"- {q}" for q in specific_questions)
        description = f"""Analyze the following contract to answer these specific questions:

{questions_formatted}

<contract>
{contract_text}
</contract>

Provide detailed answers to each question."""

    else:
        description = f"""Analyze the following contract:

<contract>
{contract_text}
</contract>

Provide a helpful analysis based on the content."""

    return Task(description=description)


async def analyze_contract_async(
    contract_text: str,
    analysis_type: str = "full",
    config: Optional[ContractAnalyzerConfig] = None,
    session_id: Optional[str] = None
) -> str:
    """
    Analyze a contract asynchronously.
    
    Convenience function that creates an agent and task, runs the analysis,
    and returns the result.
    
    Args:
        contract_text: The contract text to analyze.
        analysis_type: Type of analysis ("full", "summary", "risk", "extraction").
        config: Optional configuration settings.
        session_id: Optional session ID for memory continuity.
        
    Returns:
        The analysis result as a string.
    """
    agent = create_contract_analyzer_agent(config=config, session_id=session_id)
    task = create_analysis_task(contract_text, analysis_type)
    
    result = await agent.do_async(task)
    return str(result)


def analyze_contract(
    contract_text: str,
    analysis_type: str = "full",
    config: Optional[ContractAnalyzerConfig] = None,
    session_id: Optional[str] = None
) -> str:
    """
    Analyze a contract synchronously.
    
    Convenience function that creates an agent and task, runs the analysis,
    and returns the result.
    
    Args:
        contract_text: The contract text to analyze.
        analysis_type: Type of analysis ("full", "summary", "risk", "extraction").
        config: Optional configuration settings.
        session_id: Optional session ID for memory continuity.
        
    Returns:
        The analysis result as a string.
    """
    agent = create_contract_analyzer_agent(config=config, session_id=session_id)
    task = create_analysis_task(contract_text, analysis_type)
    
    result = agent.do(task)
    return str(result)

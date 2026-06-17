"""
Team assembly and configuration for covenant monitoring.

Creates a coordinated Team with a leader agent that orchestrates
covenant extraction, financial calculation, and compliance assessment.
"""

from __future__ import annotations

from typing import Optional

from upsonic import Agent, Team
from upsonic.storage import Memory, InMemoryStorage

try:
    from .agents import (
        create_covenant_extractor_agent,
        create_financial_calculator_agent,
        create_risk_assessor_agent,
    )
    from .schemas import CovenantMonitoringReport
except ImportError:
    from agents import (
        create_covenant_extractor_agent,
        create_financial_calculator_agent,
        create_risk_assessor_agent,
    )
    from schemas import CovenantMonitoringReport


def create_covenant_monitoring_team(
    model: str = "anthropic/claude-sonnet-4-5",
    enable_memory: bool = True,
    print: Optional[bool] = None,
) -> Team:
    """Create the coordinated Team for end-to-end covenant monitoring.

    Uses coordinate mode with a leader agent that delegates to three
    specialist agents: covenant extractor, financial calculator, and
    risk assessor.

    Args:
        model: Model identifier for the leader/coordinator agent.
        enable_memory: Whether to enable in-memory session persistence.
        print: If True, do() prints; if False, print_do() does not. Respects UPSONIC_AGENT_PRINT env.

    Returns:
        Configured Team instance ready for covenant monitoring tasks.
    """
    leader: Agent = Agent(
        model=model,
        name="Covenant Monitoring Coordinator",
        role="Head of Loan Portfolio Monitoring",
        goal=(
            "Coordinate the end-to-end covenant monitoring process by delegating "
            "to specialist agents and synthesizing a comprehensive compliance report"
        ),
        system_prompt=(
            "You coordinate the loan covenant monitoring workflow.\n\n"
            "WORKFLOW:\n"
            "1. Delegate to Covenant Extractor: Have them parse the loan agreement and "
            "extract all covenant definitions with thresholds for the applicable period\n"
            "2. Delegate to Financial Calculator: Have them calculate all required ratios "
            "using the financial data and their calculation tools\n"
            "3. Delegate to Risk Assessor: Have them evaluate compliance for each covenant "
            "using the extracted thresholds and calculated ratios\n"
            "4. Synthesize all findings into the final structured report\n\n"
            "IMPORTANT:\n"
            "- Ensure each covenant definition is matched with its corresponding ratio\n"
            "- Pass the correct threshold and constraint type to the risk assessor\n"
            "- The final report must cover every covenant's compliance status\n"
            "- Include an overall risk assessment with a numerical score and risk level\n"
            "- Provide actionable next steps, especially for any breached or near-breach covenants"
        ),
    )

    memory: Optional[Memory] = None
    if enable_memory:
        memory = Memory(
            storage=InMemoryStorage(),
            session_id="covenant_monitoring_session",
            full_session_memory=True,
        )

    covenant_extractor: Agent = create_covenant_extractor_agent()
    financial_calculator: Agent = create_financial_calculator_agent()
    risk_assessor: Agent = create_risk_assessor_agent()

    team: Team = Team(
        entities=[covenant_extractor, financial_calculator, risk_assessor],
        mode="coordinate",
        leader=leader,
        response_format=CovenantMonitoringReport,
        memory=memory,
        name="Loan Covenant Monitoring Team",
        print=print,
    )

    return team

import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional


@dataclass
class ContractAnalyzerConfig:
    """Configuration for the Contract Analyzer Agent."""
    
    # Model settings
    model: str = field(default_factory=lambda: os.getenv("CONTRACT_ANALYZER_MODEL", "openai/gpt-4o"))
    
    # Debug mode
    debug: bool = field(default_factory=lambda: os.getenv("DEBUG", "false").lower() == "true")
    
    # Vector database settings
    vectordb_path: str = field(default_factory=lambda: os.getenv(
        "VECTORDB_PATH", 
        str(Path(__file__).parent.parent / "data" / "vectordb")
    ))
    collection_name: str = "legal_knowledge"
    vector_size: int = 1536  # OpenAI text-embedding-3-small dimension
    
    # Knowledge base settings
    knowledge_sources_dir: Path = field(default_factory=lambda: Path(__file__).parent.parent / "data" / "legal_templates")
    
    # Agent settings
    agent_name: str = "Contract Analyzer"
    agent_role: str = "Senior Legal Analyst"
    agent_goal: str = "Analyze contracts accurately to extract key information and identify risks"
    
    # System prompt for the agent
    system_prompt: str = """You are an expert legal contract analyst with extensive experience in reviewing 
and analyzing legal documents. Your role is to:

1. Carefully analyze contract documents provided by users
2. Extract key information such as parties, dates, financial terms, and obligations
3. Identify potential risks, unusual clauses, or areas of concern
4. Provide clear, actionable insights for business decision-makers
5. Search the legal knowledge base when you need reference information about standard contract clauses or legal terminology

When analyzing contracts:
- Be thorough but concise in your responses
- Highlight important findings clearly
- Flag any red flags or areas requiring legal review
- Use the available tools to extract structured information
- Search the knowledge base for relevant legal references when needed

Remember: You are providing analysis to help users understand contracts, but always recommend 
professional legal counsel for final decisions on legal matters."""

    # Memory settings
    session_id_prefix: str = "contract_analyzer"
    
    def get_session_id(self, user_session: Optional[str] = None) -> str:
        """Generate a session ID for memory."""
        if user_session:
            return f"{self.session_id_prefix}_{user_session}"
        return f"{self.session_id_prefix}_default"


# Default configuration instance
default_config = ContractAnalyzerConfig()

import os
from pathlib import Path
from typing import Optional

from upsonic import KnowledgeBase
from upsonic.embeddings import OpenAIEmbedding, OpenAIEmbeddingConfig
from upsonic.vectordb import ChromaProvider
from upsonic.vectordb.config import ChromaConfig, ConnectionConfig, Mode, DistanceMetric, HNSWIndexConfig

from contract_analyzer.config import ContractAnalyzerConfig, default_config


def create_legal_knowledge_base(
    config: Optional[ContractAnalyzerConfig] = None,
    additional_sources: Optional[list] = None
) -> KnowledgeBase:
    """
    Create a legal knowledge base for contract analysis.
    
    The knowledge base contains reference information about:
    - Common contract clause types and their purposes
    - Legal terminology definitions
    - Red flags and warning signs in contracts
    - Standard contract structures
    
    This can be added to the agent as a tool, allowing the agent to
    decide when to search for relevant legal references.
    
    Args:
        config: Optional configuration. Uses default_config if not provided.
        additional_sources: Additional document sources to include.
        
    Returns:
        A configured KnowledgeBase instance ready to be used as a tool.
        
    Usage:
        ```python
        kb = create_legal_knowledge_base()
        
        # Add to task as a tool
        task = Task(
            description="Analyze this contract...",
            tools=[kb]  # Agent can search when needed
        )
        ```
    """
    if config is None:
        config = default_config
    
    embedding_config = OpenAIEmbeddingConfig(
        model_name="text-embedding-3-small"
    )
    embedding_provider = OpenAIEmbedding(embedding_config)
    
    vectordb_path = Path(config.vectordb_path)
    vectordb_path.mkdir(parents=True, exist_ok=True)
    
    connection_config = ConnectionConfig(
        mode=Mode.EMBEDDED,
        db_path=str(vectordb_path)
    )
    
    chroma_config = ChromaConfig(
        connection=connection_config,
        collection_name=config.collection_name,
        vector_size=config.vector_size,
        distance_metric=DistanceMetric.COSINE,
        index=HNSWIndexConfig()
    )
    
    vectordb = ChromaProvider(config=chroma_config)
    
    sources = []
    
    legal_templates_dir = config.knowledge_sources_dir
    if legal_templates_dir.exists():
        for file_path in legal_templates_dir.glob("*.txt"):
            sources.append(str(file_path))
        for file_path in legal_templates_dir.glob("*.md"):
            sources.append(str(file_path))
    
    if additional_sources:
        sources.extend(additional_sources)
    
    if not sources:
        default_content = _get_default_legal_content()
        sources = [default_content]
    
    kb = KnowledgeBase(
        sources=sources,
        embedding_provider=embedding_provider,
        vectordb=vectordb,
        name="Legal Contract References",
        description="A comprehensive knowledge base containing legal contract terminology, "
                   "common clause types, red flags, and contract analysis best practices. "
                   "Search this when you need reference information about contract clauses, "
                   "legal terms, or standard contract provisions.",
        topics=["contract law", "legal clauses", "contract analysis", "legal terminology"]
    )
    
    return kb


def _get_default_legal_content() -> str:
    """Get default legal reference content if no files are available."""
    return """
# Legal Contract Reference Guide

## Common Contract Clauses

### 1. Indemnification Clause
An indemnification clause requires one party to compensate the other for certain damages or losses. 
Key considerations:
- Scope of indemnification (what events trigger it)
- Cap on liability
- Whether indemnification is mutual or one-sided
- Carve-outs and exceptions

### 2. Limitation of Liability
Limits the amount of damages a party can recover. Important aspects:
- Types of damages excluded (consequential, punitive)
- Cap amount (often tied to contract value)
- Carve-outs for gross negligence or willful misconduct
- RED FLAG: One-sided limitations or unlimited liability for one party

### 3. Termination Provisions
Defines how and when the contract can be ended. Consider:
- Termination for cause vs. convenience
- Notice requirements
- Cure periods for breach
- Effect of termination (survival clauses)
- RED FLAG: Termination at will with no notice period

### 4. Confidentiality/Non-Disclosure
Protects sensitive information shared between parties. Key elements:
- Definition of confidential information
- Permitted disclosures
- Duration of confidentiality obligation
- Return or destruction of information

### 5. Intellectual Property Rights
Addresses ownership and licensing of IP. Important provisions:
- Work product ownership
- Pre-existing IP
- License grants
- Assignment rights

### 6. Warranties and Representations
Statements of fact or commitments about the subject matter. Types:
- Express warranties
- Implied warranties
- Disclaimers
- Warranty period

## Red Flags in Contracts

### High Risk Items
1. **Unlimited liability** - No cap on potential damages
2. **One-sided indemnification** - Only one party bears risk
3. **Automatic renewal without notice** - Trapped in unfavorable terms
4. **Broad non-compete clauses** - Excessive restrictions
5. **Waiver of jury trial** - Giving up important rights
6. **Unfavorable governing law** - Distant or unfamiliar jurisdiction

### Medium Risk Items
1. **Short cure periods** - Limited time to fix breaches
2. **Broad definition of confidential information**
3. **Restrictive assignment clauses**
4. **Mandatory arbitration** - May limit remedies
5. **Most favored nation clauses** - Pricing commitments

### Items Requiring Attention
1. **Insurance requirements** - Ensure compliance capability
2. **Audit rights** - Consider operational impact
3. **Change of control provisions**
4. **Force majeure scope**
5. **Payment terms and late fees**

## Contract Analysis Best Practices

1. **Read the entire contract** - Don't skip sections
2. **Identify the parties** - Verify legal names and authority
3. **Understand the scope** - What exactly is being agreed to
4. **Check all dates** - Effective, termination, renewal
5. **Review financial terms** - All payments, fees, penalties
6. **Identify your obligations** - What must you do
7. **Assess risk allocation** - Who bears what risks
8. **Review termination rights** - How can you exit
9. **Check governing law** - Where disputes are resolved
10. **Seek legal counsel** - For significant contracts

## Common Legal Terms

- **Force Majeure**: Unforeseeable circumstances preventing contract fulfillment
- **Severability**: Invalid provisions don't void entire contract
- **Waiver**: Giving up a right (usually requires writing)
- **Assignment**: Transferring rights/obligations to another party
- **Novation**: Replacing a party or obligation with consent
- **Material Breach**: Significant violation justifying termination
- **Liquidated Damages**: Pre-determined penalty amount
- **Good Faith**: Acting honestly and fairly
- **Time is of the Essence**: Deadlines are strictly enforced
- **Entire Agreement**: Contract supersedes prior discussions
"""

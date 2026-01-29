from typing import Dict, Any

from contract_analyzer.agent import analyze_contract_async
from upsonic import Task


async def main(inputs: Dict[str, Any]) -> Dict[str, Any]:
    """
    Main API endpoint for contract analysis.
    
    Args:
        inputs: Dictionary containing:
            - contract_text (str, required): The contract text to analyze
            - analysis_type (str, optional): Type of analysis - "full", "summary", "risk", or "extraction". Defaults to "full"
            - session_id (str, optional): Session ID for conversation continuity
            - question (str, optional): Specific question to ask about the contract (for Q&A mode)
    
    Returns:
        Dictionary containing:
            - analysis_result (str): The analysis result
            - analysis_type (str): The type of analysis performed
    """
    contract_text = inputs.get("contract_text")
    analysis_type = inputs.get("analysis_type", "full")
    session_id = inputs.get("session_id")
    question = inputs.get("question")
    
    if not contract_text:
        return {
            "error": "contract_text is required",
            "analysis_result": None
        }
    
    try:
        if question:
            from contract_analyzer.agent import create_contract_analyzer_agent
            
            agent = create_contract_analyzer_agent(session_id=session_id)
            task = Task(
                description=f"""Based on the following contract, please answer this question:

                        Question: {question}

                        <contract>
                        {contract_text}
                        </contract>

                        Provide a helpful, accurate answer based on the contract content."""
            )
            result = await agent.do_async(task)
            return {
                "analysis_result": str(result),
                "analysis_type": "qa"
            }
        
        result = await analyze_contract_async(
            contract_text=contract_text,
            analysis_type=analysis_type,
            session_id=session_id
        )
        
        return {
            "analysis_result": result,
            "analysis_type": analysis_type
        }
        
    except Exception as e:
        return {
            "error": str(e),
            "analysis_result": None,
            "analysis_type": analysis_type
        }

if __name__ == "__main__":
    import asyncio
    asyncio.run(main({
        "contract_text": "This is a contract text",
        "analysis_type": "full",
        "session_id": "test",
        "question": "What is the contract?"
    }))
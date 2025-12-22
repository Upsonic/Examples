"""
Sales Offer Generator Agent

This example demonstrates how to create and use an Agent that research products and writes sales offers.

This file contains:
- async main(inputs): For use with `upsonic run` CLI command (FastAPI server)
"""
import asyncio
from upsonic import Task
from upsonic.agent.deepagent import DeepAgent
from agents import SalesAgents

async def main(inputs: dict) -> dict:
    """
    Async main function for FastAPI server (used by `upsonic run` command).
    
    This function is called by the Upsonic CLI when running the agent as a server.
    It receives inputs from the API request and returns a response dictionary.
    
    Args:
        inputs: Dictionary containing input parameters as defined in upsonic_configs.json
                Expected key: "user_query" (string)
    
    Returns:
        Dictionary with output schema as defined in upsonic_configs.json
        Expected key: "bot_response" (string)
    """
    
    user_query = inputs.get("user_query")
    if not user_query:
        return {"bot_response": "Please provide a user_query."}

    print("🚀 Starting Sales Offer Generator Agent (DeepAgent Mode)...\n")

    # 1. Initialize Agents Factory
    agents_factory = SalesAgents()

    # 2. Create Specialist Agents
    researcher = agents_factory.product_researcher()
    strategist = agents_factory.pricing_strategist()
    writer = agents_factory.offer_writer()

    # 3. Initialize DeepAgent with the Team
    # DeepAgent will automatically coordinate these subagents to fulfill the main task.
    deep_agent = DeepAgent(
        model="openai/gpt-4o",
        subagents=[researcher, strategist, writer]
    )

    print(f"📋 Customer Requirements:\n{user_query}\n")

    task = Task(description=f"""
    Generate a complete, personalized sales offer email for a customer with these requirements:
    "{user_query}"

    You must execute this in the following order:
    1. MARKET RESEARCH: Use the Product Researcher to find at least 3 REAL products available now that match the specs. Get prices.
    2. PRICING STRATEGY: Use the Pricing Strategist to analyze the findings and determine the best 'special offer' price.
    3. EMAIL DRAFT: Use the Creative Copywriter to write the final sales email including the selected best product and the special price.
    
    Output the final email.
    """)

    # 5. Execute
    print("🤖 DeepAgent is working...")
    result = await deep_agent.do_async(task)

    print("\n" + "="*50)
    print("Final Result:")
    print("="*50)
    print(result)
    
    return {
        "bot_response": result
    }


if __name__ == "__main__":
    # Test execution
    test_input = {
        "user_query": "I need a high-performance laptop for video editing (4K workflows) and 3D rendering. Budget is around $3,000. Prefer NVIDIA RTX 4080 or better."
    }
    asyncio.run(main(test_input))

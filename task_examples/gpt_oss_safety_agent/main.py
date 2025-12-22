"""
Openai Safety Agent Example with provider OpenRouter

This example demonstrates how to use the OpenAI's gpt-oss-safeguard-20b model
with Upsonic's safety policies (PIIBlockPolicy_LLM) to create a secure AI agent.

The agent:
- Uses OpenAI's gpt-4o for main agent responses
- Uses OpenRouter's gpt-oss-safeguard-20b (OpenAI's safety-focused model) for policy enforcement
- Applies PIIBlockPolicy_LLM to detect and block PII in user inputs
- Provides helpful feedback when policy violations occur

Requirements:
- Set OPENROUTER_API_KEY environment variable
- Set OPENAI_API_KEY environment variable (for gpt-4o)
"""

from upsonic import Task, Agent
from upsonic.safety_engine.policies.pii_policies import PIIBlockPolicy_LLM
from upsonic.safety_engine.llm.upsonic_llm import UpsonicLLMProvider


async def main(inputs):
    """
    Main function for the Safety Agent.
    
    Args:
        inputs: Dictionary containing user_query
        
    Returns:
        Dictionary containing bot_response
    """
    user_query = inputs.get("user_query")
    
    answering_task = Task(f"Answer the user question: {user_query}")
    
    # Set the LLM for the policy to use gpt-oss-safeguard-20b via OpenRouter
    policy_llm = UpsonicLLMProvider(
        agent_name="PII Policy LLM",
        model="openrouter/openai/gpt-oss-safeguard-20b"
    )
    PIIBlockPolicy_LLM.base_llm = policy_llm
    
    agent = Agent(
        model='openai/gpt-4o',
        user_policy=PIIBlockPolicy_LLM,
        user_policy_feedback=True,
        user_policy_feedback_loop=1,
        debug=True
    )
    
    result = await agent.print_do_async(answering_task)
    
    return {
        "bot_response": result
    }


if __name__ == "__main__":
    import asyncio
    
    test_inputs = [
        {"user_query": "What is machine learning?"},
        {"user_query": "My email is john@example.com, can you help me with my account?"},
    ]
    
    async def run_tests():
        for i, inputs in enumerate(test_inputs, 1):
            print(f"\n{'='*60}")
            print(f"Test {i}: {inputs['user_query'][:50]}...")
            print('='*60)
            
            try:
                _ = await main(inputs)
            except Exception as e:
                print(f"\nError: {e}")
    
    asyncio.run(run_tests())

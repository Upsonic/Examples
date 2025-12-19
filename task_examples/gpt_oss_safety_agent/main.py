"""
Openai Safety Agent Example with provider OpenRouter

This example demonstrates how to use the OpenAI's gpt-oss-safeguard-20b model
with Upsonic's safety policies (PIIBlockPolicy) to create a secure AI agent.

The agent:
- Uses OpenRouter's gpt-oss-safeguard-20b (OpenAI's safety-focused model)
- Applies PIIBlockPolicy to detect and block PII in user inputs
- Provides helpful feedback when policy violations occur

Requirements:
- Set OPENROUTER_API_KEY environment variable
"""

from upsonic import Task, Agent
from upsonic.safety_engine.policies.pii_policies import PIIBlockPolicy


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
    
    agent = Agent(
        model='openrouter/openai/gpt-oss-safeguard-20b',
        user_policy=PIIBlockPolicy,
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
                result = await main(inputs)
                print(f"\nResult: {result['bot_response']}")
            except Exception as e:
                print(f"\nError: {e}")
    
    asyncio.run(run_tests())

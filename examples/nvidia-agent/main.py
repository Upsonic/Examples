"""
NVIDIA Agent Example

This example demonstrates how to create and use an Agent with NVIDIA models.
The example shows:
1. Creating a NvidiaModel instance
2. Creating an Agent with the NvidiaModel
3. Creating a Task
4. Executing the task with the agent

This file contains:
- async main(inputs): For use with `upsonic run` CLI command (FastAPI server)
"""

from upsonic import Agent, Task
from upsonic.models.nvidia import NvidiaModel


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
    user_query = inputs.get("user_query", "Hi, how are you?")

    model = NvidiaModel(
        model_name="meta/llama-3.1-nemotron-70b-instruct:1.0"
    )

    agent = Agent(
        model=model,
        name="NVIDIA Agent"
    )
    

    answering_task = Task(
        description=f"Answer the user question: {user_query}"
    )
    
    result = await agent.print_do_async(answering_task)
    
    return {
        "bot_response": result
    }


if __name__ == "__main__":
    import asyncio
    asyncio.run(main({"user_query": "Hi, how are you?"}))
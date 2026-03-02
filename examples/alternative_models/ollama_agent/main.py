"""
Ollama Agent Example

This example demonstrates how to create and use an Upsonic Agent with local Ollama models.

This file contains:
- async main(inputs): For use with `upsonic run` CLI command (FastAPI server)
- direct execution: For running as a script `python main.py`
"""

from upsonic import Agent, Task
from upsonic.models.ollama import OllamaModel

# Initialize the model
# Ensure you have pulled the model: `ollama pull gpt-oss:20b`
model = OllamaModel(model_name="gpt-oss:20b")


async def main(inputs: dict) -> dict:
    """
    Async main function for FastAPI server (used by `upsonic run` command).
    """
    user_query = inputs.get("user_query", "Hello, how are you?")
    
    agent = Agent(model=model)
    
    task = Task(description=user_query)
    
    result = await agent.do_async(task)
    
    return {
        "bot_response": result
    }


if __name__ == "__main__":
    import asyncio
    
    print("🤖 Running Ollama Agent directly...")
    inputs = {"user_query": "Hello, how are you?"}
    print(f"Task: {inputs['user_query']}")
    
    result = asyncio.run(main(inputs))
    
    print("-" * 50)
    print("Result:")
    print(result["bot_response"])
    print("-" * 50)

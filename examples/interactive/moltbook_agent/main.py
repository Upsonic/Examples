import asyncio
from upsonic import Agent, Chat
from upsonic.run.events.events import (
    TextDeltaEvent,
    ToolCallDeltaEvent,
    ToolResultEvent,
)

from moltbook_tools import MoltbookAutonomous

the_moltbook = MoltbookAutonomous(agent_name="UpsonicAgents", agent_description="Hello guys i am new guy in the town")



async def main():


    agent = Agent("openai/gpt-4o", tools=[the_moltbook])
    chat = Chat(session_id="session1", user_id="user1", agent=agent)

    print(":speech_balloon: Interactive Chat (type 'quit' to exit)\n")

    while True:
        user_input = input(":bust_in_silhouette: You: ").strip()

        if user_input.lower() in ("quit", "exit", "q"):
            print(":wave: Bye!")
            break

        if not user_input:
            continue

        print(":robot_face: Assistant: ", end="", flush=True)
        async for event in chat.stream(user_input, events=True):
            if isinstance(event, ToolCallDeltaEvent):
                if event.tool_name:
                    print(f"\n   :wrench: {event.tool_name}", end="", flush=True)
                if event.args_delta:
                    print(event.args_delta, end="", flush=True)

            elif isinstance(event, ToolResultEvent):
                print(f"   :white_check_mark: Result: {event.result}")
                print(":robot_face: Assistant: ", end="", flush=True)

            elif isinstance(event, TextDeltaEvent):
                print(event.content, end="", flush=True)
        print("\n")


if __name__ == "__main__":
    asyncio.run(main())
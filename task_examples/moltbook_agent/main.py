import asyncio
from upsonic import Agent, Chat

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
        async for chunk in chat.stream(user_input):
            print(chunk, end="", flush=True)
        print("\n")


if __name__ == "__main__":
    asyncio.run(main())
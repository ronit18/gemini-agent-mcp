import os
import asyncio
from google.genai import types
from google.adk.agents.llm_agent import LlmAgent
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from dotenv import load_dotenv

load_dotenv()
os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")


# Simple file writing tool
def write_file_tool(content: str, filename: str) -> str:
    """Write content to a file in the current directory."""
    try:
        with open(filename, "w") as f:
            f.write(content)
        return f"Successfully wrote to {filename}"
    except Exception as e:
        return f"Error writing to {filename}: {e}"


async def async_main():
    # Create agent with simple file writing tool
    root_agent = LlmAgent(
        model="gemini-2.0-flash",
        name="file_assistant",
        instruction="Help user by writing files. Use the write_file_tool to create files.",
        tools=[write_file_tool],
    )

    session_service = InMemorySessionService()
    session = await session_service.create_session(
        state={}, app_name="simple_file_app", user_id="user_fs"
    )

    query = "write a poem on Gujarat University(GU) and save it as poem.txt"
    print(f"User Query: '{query}'")

    content = types.Content(role="user", parts=[types.Part(text=query)])

    runner = Runner(
        app_name="simple_file_app",
        agent=root_agent,
        session_service=session_service,
    )

    print("Running agent...")
    events_async = runner.run_async(
        session_id=session.id, user_id=session.user_id, new_message=content
    )

    async for event in events_async:
        print(f"Event received: {event}")

    print("Task complete.")


if __name__ == "__main__":
    try:
        asyncio.run(async_main())
    except Exception as e:
        print(f"An error occurred: {e}")

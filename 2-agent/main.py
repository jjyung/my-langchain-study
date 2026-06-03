from langchain.agents import create_agent
from langchain.tools import tool
from dotenv import load_dotenv

from langchain_core.utils.uuid import uuid7
from langgraph.checkpoint.memory import InMemorySaver

from langchain.messages import AIMessage, HumanMessage

load_dotenv()


@tool
def search(query: str) -> str:
    """Search for information."""
    return f"Results for: {query}"


system_prompt = "You are a helpful assistant. Be concise and accurate."


config = {"configurable": {"thread_id": str(uuid7())}}

agent = create_agent(
    "google_genai:gemini-3-flash-preview",
    tools=[search],
    system_prompt=system_prompt,
    name="research_assistant",
    checkpointer=InMemorySaver(),
)


def main():

    # Stream the agent's response to the first question
    for chunk in agent.stream(
        {
            "messages": [
                {
                    "role": "user",
                    "content": "What's the weather in San Francisco?",
                }
            ]
        },
        stream_mode="values",
        config=config,
    ):
        # Each chunk contains the full state at that point
        latest_message = chunk["messages"][-1]
        if latest_message.content:
            if isinstance(latest_message, HumanMessage):
                print(f"User: {latest_message.content}")
            elif isinstance(latest_message, AIMessage):
                print(f"Agent: {latest_message.content}")
        elif latest_message.tool_calls:
            print(f"Calling tools: {[tc['name'] for tc in latest_message.tool_calls]}")

    for chunk in agent.stream(
        {
            "messages": [
                {
                    "role": "user",
                    "content": "What about tomorrow?",
                }
            ]
        },
        stream_mode="values",
        config=config,
    ):
        # Each chunk contains the full state at that point
        latest_message = chunk["messages"][-1]
        if latest_message.content:
            if isinstance(latest_message, HumanMessage):
                print(f"User: {latest_message.content}")
            elif isinstance(latest_message, AIMessage):
                print(f"Agent: {latest_message.content}")
        elif latest_message.tool_calls:
            print(f"Calling tools: {[tc['name'] for tc in latest_message.tool_calls]}")


if __name__ == "__main__":
    main()

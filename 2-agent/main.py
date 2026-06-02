from dataclasses import dataclass

from langchain.agents import create_agent
from langchain.tools import tool
from dotenv import load_dotenv
from pydantic import BaseModel

from langchain_core.utils.uuid import uuid7
from langgraph.checkpoint.memory import InMemorySaver

load_dotenv()


@tool
def search(query: str) -> str:
    """Search for information."""
    return f"Results for: {query}"


system_prompt = "You are a helpful assistant. Be concise and accurate."


class Answer(BaseModel):
    summary: str
    confidence: float


config = {"configurable": {"thread_id": str(uuid7())}}

agent = create_agent(
    "google_genai:gemini-3-flash-preview",
    tools=[search],
    system_prompt=system_prompt,
    response_format=Answer,
    name="research_assistant",
    checkpointer=InMemorySaver(),
)


def main():
    result = agent.invoke(
        {
            "messages": [
                {"role": "user", "content": "What's the weather in San Francisco?"}
            ],
        },
        config=config,
    )
    print(result["structured_response"])  # Answer(summary=..., confidence=...)

    result = agent.invoke(
        {"messages": [{"role": "user", "content": "What about tomorrow?"}]},
        config=config,
    )
    print(result["structured_response"])  # Answer(summary=..., confidence=...)


if __name__ == "__main__":
    main()

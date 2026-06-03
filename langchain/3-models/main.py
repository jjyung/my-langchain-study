from dotenv import load_dotenv

from langchain.chat_models import init_chat_model
from langchain.tools import tool
from langchain_core.messages import AIMessage, AIMessageChunk, HumanMessage, ToolMessage

load_dotenv(".env")


@tool
def get_weather(location: str) -> str:
    """Get the weather at a location."""
    return f"It's sunny in {location}."


model = init_chat_model(
    "google_genai:gemini-2.5-flash-lite",
    temperature=0.7,
    timeout=30,
    max_tokens=1000,
    max_retries=6,
)

model_with_tools = model.bind_tools([get_weather])

messages = [HumanMessage("What's the weather like in Boston?")]

while True:
    full: AIMessageChunk | None = None

    for chunk in model_with_tools.stream(messages):
        full = chunk if full is None else full + chunk

        for block in chunk.content_blocks:
            if block["type"] == "reasoning" and (reasoning := block.get("reasoning")):
                print(f"Reasoning: {reasoning}")
            elif block["type"] == "text":
                print(block.get("text", ""), end="", flush=True)
            elif block["type"] == "tool_call":
                print(f"[Calling tool: {block.get('name')}]", end="", flush=True)

    if full and full.tool_calls:
        print()
        messages.append(AIMessage(content=full.content, tool_calls=full.tool_calls))
        for tc in full.tool_calls:
            result = get_weather.invoke(tc["args"])
            print(f"  → {result}")
            messages.append(ToolMessage(content=result, tool_call_id=tc["id"]))
    else:
        print()
        break

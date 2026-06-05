import subprocess

import os
from langchain.chat_models import init_chat_model
from langchain.agents import create_agent
from langchain_core.tools import tool
from dotenv import load_dotenv

load_dotenv()

MAX_OUTPUT = 5000


@tool
def write_file(path: str, content: str) -> str:
    """Write content to a file at the given path."""
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "w") as f:
        f.write(content)
    return f"Wrote {path} ({len(content)} bytes)"


@tool
def read_file(path: str) -> str:
    """Read the contents of a file."""
    with open(path) as f:
        return f.read()


@tool
def execute(command: str) -> str:
    """Execute a shell command and return its output."""
    result = subprocess.run(
        command, shell=True, capture_output=True, text=True, timeout=60
    )
    output = (result.stdout + result.stderr).strip()
    if len(output) > MAX_OUTPUT:
        output = output[:MAX_OUTPUT] + "\n... (truncated)"
    return output or "(no output)"


@tool
def ls(path: str = ".") -> str:
    """List files in a directory."""
    result = subprocess.run(
        ["ls", "-la", path], capture_output=True, text=True
    )
    return result.stdout or result.stderr


model = init_chat_model("google_genai:gemini-2.5-flash")

agent = create_agent(
    model,
    tools=[write_file, read_file, execute, ls],
    system_prompt="You are a Python coding assistant. You can write files and run shell commands.",
)

for event in agent.stream(
    {
        "messages": [
            {
                "role": "user",
                "content": "Create a small Python package and run pytest",
            }
        ]
    }
):
    for node, update in event.items():
        if isinstance(update, dict) and "messages" in update:
            for msg in update["messages"]:
                role = msg.type.upper()
                if msg.content and isinstance(msg.content, str):
                    print(f"\n[{role}]: {msg.content[:500]}")
                elif hasattr(msg, "tool_calls") and msg.tool_calls:
                    for tc in msg.tool_calls:
                        print(f"\n[{role} uses {tc['name']}]: {tc['args']}")

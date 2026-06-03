# Messages

Messages = the unit of communication between user and model — what goes in and what comes out.

## What it does

Uses `create_agent` (LangGraph) with Google Gemini (`gemini-2.5-flash-lite`) to answer weather queries:

- Binds a `get_weather` tool
- Prints the raw `content_blocks` of the final AI response
- Demonstrates the structured output format (`tool_use`, `text`, etc.)

## Setup

```bash
uv sync
```

Copy `.env.example` to `.env` and set your `GOOGLE_API_KEY`.

## Usage

```bash
uv run main.py
```

## Dependencies

- `langchain`
- `langchain-google-genai`
- `dotenv`

Managed via `uv` / `pyproject.toml`.

# Models

Model = the core LLM inference layer — no agent harness, just model + tools.

## What it does

Demonstrates streaming tool calling with Google Gemini (`gemini-2.5-flash-lite`) via `init_chat_model`:

- Initializes a model with configurable parameters (`temperature`, `timeout`, `max_tokens`)
- Binds a `get_weather` tool using `bind_tools`
- Streams the response, handling `text`, `reasoning`, and `tool_call` blocks
- Manually executes tools and feeds results back in a loop

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

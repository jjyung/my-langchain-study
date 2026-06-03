# Agents

Agent = Model + Harness — the harness delivers the right context at the right time.

## What it does

A research agent powered by Google Gemini (`gemini-3-flash-preview`) via LangGraph:

- Calls a `search` tool for information retrieval
- Returns structured output (`summary` + `confidence`) via Pydantic
- Maintains conversation history with `InMemorySaver` checkpointing
- Supports follow-up questions within the same thread

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
- `langgraph`
- `python-dotenv`

Managed via `uv` / `pyproject.toml`.

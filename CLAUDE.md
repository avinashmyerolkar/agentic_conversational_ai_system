# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Running the App

```bash
source venv/bin/activate
streamlit run frontend.py
```

Requires a `.env` file with `OPENAI_API_KEY` set (loaded via `python-dotenv`).

## Architecture

This is a Streamlit + LangGraph conversational AI app with two files:

- **`backend.py`** — Defines the LangGraph `StateGraph` with a single `chat_node` that calls `ChatOpenAI`. Compiles the graph as `chatbot` with `InMemorySaver` for conversation persistence across turns within a session.
- **`frontend.py`** — Streamlit UI. Maintains `message_history` in `st.session_state` for display, invokes `chatbot` with a fixed `thread_id` (`thread-1`), and renders the chat.

**Key design note:** LangGraph's `InMemorySaver` is the source of truth for conversation history per thread; `st.session_state['message_history']` is only a display cache for rendering previous messages on page reload.

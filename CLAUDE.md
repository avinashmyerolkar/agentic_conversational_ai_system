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

## Streaming

The app uses LangGraph's `chatbot.stream()` with `stream_mode='messages'` instead of `chatbot.invoke()`. This returns a generator of `(message_chunk, metadata)` tuples. The chunk content is fed into Streamlit's `st.write_stream()`, which renders tokens progressively as they arrive from the LLM. The fully assembled response string returned by `st.write_stream` is what gets appended to `st.session_state['message_history']`.

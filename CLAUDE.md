# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Running the App

```bash
source venv/bin/activate
streamlit run frontend.py
```

Requires a `.env` file with `OPENAI_API_KEY` set (loaded via `python-dotenv`).

## Architecture

This is a Streamlit + LangGraph conversational AI app with three files:

- **`backend.py`** — Defines the LangGraph `StateGraph` with a single `chat_node` that calls `ChatOpenAI`. Compiles the graph as `chatbot` with `InMemorySaver` for conversation persistence across turns within a session.
- **`frontend.py`** — Streamlit UI. Maintains `message_history` in `st.session_state` for display, invokes `chatbot` with a dynamic `thread_id` from `st.session_state`, and renders the chat. The sidebar provides "New Chat" and a list of past threads to resume.
- **`utility.py`** — Helper functions for session management:
  - `generate_thread_id()` — creates a unique `uuid4` thread ID
  - `reset_chat()` — generates a new thread ID and clears message history
  - `add_thread(thread_id)` — registers a thread ID in `st.session_state['chat_threads']`
  - `load_conversation_with_thread_id(thread_id)` — fetches message history from LangGraph's `InMemorySaver` via `chatbot.get_state()`

**Key design note:** LangGraph's `InMemorySaver` is the source of truth for conversation history per thread; `st.session_state['message_history']` is only a display cache. When a user resumes a past thread, messages are fetched from `InMemorySaver` and converted to the `{'role', 'content'}` display format before being written to `message_history`.

## Session Management

Each browser session starts with a fresh `uuid4` thread ID. All active thread IDs are stored in `st.session_state['chat_threads']` and displayed in the sidebar. Clicking a thread:
1. Sets `st.session_state['thread_id']` to that thread's ID (so subsequent messages continue in that thread)
2. Loads the thread's messages from LangGraph state
3. Converts them to the display format and updates `message_history`

## Streaming

The app uses LangGraph's `chatbot.stream()` with `stream_mode='messages'` instead of `chatbot.invoke()`. This returns a generator of `(message_chunk, metadata)` tuples. The chunk content is fed into Streamlit's `st.write_stream()`, which renders tokens progressively as they arrive from the LLM. The fully assembled response string returned by `st.write_stream` is what gets appended to `st.session_state['message_history']`.

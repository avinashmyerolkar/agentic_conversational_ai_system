# Conversational AI Project

A multi-turn conversational AI chatbot built with LangGraph, OpenAI, and Streamlit.

## Features

- **Persistent memory** — conversation history is retained across turns within a session using LangGraph's checkpointer
- **Chat UI** — clean Streamlit-based interface with chat bubbles and input field

## Tech Stack

| Layer | Technology |
|---|---|
| LLM | OpenAI GPT (via `langchain_openai`) |
| Orchestration | LangGraph `StateGraph` |
| UI | Streamlit |
| Memory | LangGraph `InMemorySaver` |

## Setup

**1. Clone the repo and create a virtual environment**

```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
```

**2. Install dependencies**

```bash
pip install -r requirements.txt
```

**3. Configure environment variables**

Create a `.env` file in the project root:

```
OPENAI_API_KEY=your_openai_api_key_here
```

## Running the App

```bash
streamlit run frontend.py
```

## Project Structure

```
├── backend.py        # LangGraph StateGraph definition and compiled chatbot
├── frontend.py       # Streamlit UI
├── requirements.txt
└── .env              # Not committed — add your own
```

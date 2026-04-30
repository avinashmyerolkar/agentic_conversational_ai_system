import uuid
import streamlit as st
from backend import chatbot

def generate_thread_id():
    """
    will generate new thread id using uuid
    """
    thread_id = uuid.uuid4()
    return thread_id

def reset_chat():
    """
    Docstring for reset_chat
    when user will click on new chat, we have to do 3 things
    1. create new thread id
    2. store newly created thread id in session state
    3. clean message history conversation from precious convo in session
    """
    thread_id = generate_thread_id()  
    st.session_state['thread_id'] = thread_id
    add_thread(thread_id=st.session_state['thread_id'])
    st.session_state['message_history'] = []

def add_thread(thread_id):
    """
    here we will store chat wrt to every thread id : chat_thread 
    so that user can go on respective thread and resume chat 
    """
    if thread_id not in st.session_state['chat_threads']:
        st.session_state["chat_threads"].append(thread_id)

def load_conversation_with_thread_id(thread_id):
    """
    Docstring for load_conversation_with_thread_id
    
    :param thread_id: thread id of respective conversation

    when user will click on specific thread id, conversation will get laoaded in list to render on ui
    CONFIG = {'configurable': {'thread_id': st.session_state['thread_id']}}
    """
    state = chatbot.get_state(
        config={"configurable": {"thread_id": thread_id}}
    )
    return state.values.get("messages", [])
    #return chatbot.get_state(config={'configurable': {'thread_id': thread_id}}).values['messages']
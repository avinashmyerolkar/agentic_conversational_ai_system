import streamlit as st
from langchain_core.messages import HumanMessage
from backend import chatbot

###################################### session setup ###################################

if "message_history" not in st.session_state: # st.session_state is a dictionary
    st.session_state['message_history'] = [] # adding message_history key to above dictionary


CONFIG = {'configurable': {'thread_id': 'thread-1'}} # as we have already incorporated thread id


# to render previous conversation on UI
for message in st.session_state['message_history']:
    with st.chat_message(message['role']):
        st.text(message['content'])

user_input = st.chat_input(placeholder='Type here ...') # where user can type message / input here

if user_input:  # once user has written message
    st.session_state['message_history'].append({'role':'user','content': user_input}) # appending list of conversation by user
    with st.chat_message(name='user'):  # it should be displayed in chat section under User role
        st.text(body=user_input)  # this will be render under chat message

    # sending user input to workflow    
    initial_state = {'messages':HumanMessage(content=user_input)} # convert user input to human message

    # for no stream response
    # response = chatbot.invoke(initial_state, config = CONFIG)
    # ai_message = response['messages'][-1].content  # extracting last most message from reponse
    # st.session_state['message_history'].append({'role':'assistant','content': ai_message})
    # with st.chat_message(name='assistant'):
    #     st.text(body=ai_message)

    # for streaming response 
    stream_object = chatbot.stream(initial_state, config=CONFIG,stream_mode='messages') # generator object by .stream method = message chunk + metadata
    with st.chat_message('assistant'):
        ai_message = st.write_stream(
            message_chunk.content for message_chunk, metadata in stream_object
        )  # to render streaming messages in streamlit we have st.write_stream method
    st.session_state['message_history'].append({'role':'assistant','content': ai_message}) # appending list of conversation by assistant
              

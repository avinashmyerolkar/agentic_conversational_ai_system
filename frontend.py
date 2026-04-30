import streamlit as st
from backend import chatbot
from utility import generate_thread_id
from utility import reset_chat
from utility import add_thread
from utility import load_conversation_with_thread_id
from langchain_core.messages import HumanMessage



###################################### session setup ###################################

if "message_history" not in st.session_state: # st.session_state is a dictionary
    st.session_state['message_history'] = [] # adding message_history key to above dictionary

if "thread_id" not in st.session_state:
    st.session_state['thread_id'] = generate_thread_id() # for dynamic thread id

if "chat_threads" not in st.session_state:
    st.session_state['chat_threads'] = []  # when user clieck on specific thrread convo

add_thread(thread_id=st.session_state['thread_id'])

###################################### Side bar UI ###################################
st.sidebar.title('Langraph Chatbot')

if st.sidebar.button('New Chat'):
    reset_chat()


st.sidebar.header('My Conversations')
# st.sidebar.text(st.session_state['thread_id']) # to showcase thread_id / conversation with reaspect to thread

for thread_id in st.session_state['chat_threads'][::-1]:
    #st.sidebar.text(thread_id)  # to show all threads of conversation on sidebar
    # st.sidebar.button(str(thread_id)) # to make it clickable
    if st.sidebar.button(str(thread_id)):
        st.session_state['thread_id'] = thread_id # we have to store conversation realted to same trhead id user clicked
        meassages_list = load_conversation_with_thread_id(thread_id=thread_id)

        # as the format in conversation in loaded conversation is not compatible to render on UI when user click thread id 
        temp_message = []
        for msg in meassages_list:
            if isinstance(msg, HumanMessage):
                role='user'
            else:
                role='assistant'
            temp_message.append({'role':role, 'content':msg.content})
        st.session_state['message_history'] = temp_message


###################################### Main UI ###################################
CONFIG = {'configurable': {'thread_id': st.session_state['thread_id']}} # as we have already incorporated thread id

# to render previous conversation on UI
for message in st.session_state['message_history']:
    with st.chat_message(message['role']):
        st.text(message['content'])


user_input = st.chat_input(placeholder='Type here ...') # where user can type message

if user_input:  # once user has written message
    st.session_state['message_history'].append({'role':'user','content': user_input}) # appending list of conversation by user
    with st.chat_message(name='user'):  # it should be displayed in chat section under User role
        st.text(body=user_input)  # this will be render under chat message

    # sending user input to workflow    
    initial_state = {'messages':HumanMessage(content=user_input)} # convert user input to human message

    # for no stream response
    # response = chatbot.invoke(initial_state, config=CONFIG)  # invoke main workflow we have to pass thread id too, as checkpointer we have configured
    # ai_message = response['messages'][-1].content  # extracting last most message from reponse
    # st.session_state['message_history'].append({'role':'assistant','content': ai_message}) # # appending list of conversation by assistant
    # with st.chat_message(name='assistant'):
    #     st.text(body=ai_message)

    # for streaming response 
    stream_object = chatbot.stream(initial_state, config=CONFIG,stream_mode='messages') # generator object by .stream method = message chunk + metadata
    with st.chat_message('assistant'):
        ai_message = st.write_stream(
            message_chunk.content for message_chunk, metadata in stream_object
        )  # to render streaming messages in streamlit we have st.write_stream method
    st.session_state['message_history'].append({'role':'assistant','content': ai_message}) # appending list of conversation by assistant
              


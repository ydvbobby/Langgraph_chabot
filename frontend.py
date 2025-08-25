import streamlit as st
from langgraph_backend import chatbot, retreive_all_threads
from langchain_core.messages import HumanMessage, AIMessage
import uuid


#******************************UTILITY_FUNCTIONS*********************************************************

def create_thread():
    thread_id = uuid.uuid4()
    return thread_id

def add_thread(thread_id):
    if thread_id not in st.session_state['thread_list']:
        st.session_state['thread_list'].append(thread_id)

def reset_chat():
    thread_id = create_thread()
    st.session_state['message_history'] = []
    st.session_state['thread_id'] = thread_id
    add_thread(thread_id)
    
def load_conversations(thread_id):
    conversation = chatbot.get_state(config={'configurable': {'thread_id': thread_id}}).values['messages']
    return conversation
    

#***************************************SESSION_STATE*******************************************************

if 'message_history' not in st.session_state:
    st.session_state['message_history'] = []
    

if 'thread_id' not in st.session_state:
    st.session_state['thread_id'] = create_thread()

if "thread_list" not in st.session_state:
    st.session_state['thread_list'] = retreive_all_threads()

add_thread(st.session_state['thread_id'])

#****************************************SIDEBAR***********************************************************

st.sidebar.title("AI Chatbot")

new_chat = st.sidebar.button("New Chat")
if new_chat:
    reset_chat()

st.sidebar.subheader("Conversations")

for thread_ids in st.session_state['thread_list']:
    if st.sidebar.button(f"{thread_ids}"):
        st.session_state['thread_id'] = thread_ids
        conversation = load_conversations(thread_ids)
        
        temp_msg = []
        for msg in conversation:
            if isinstance(msg, HumanMessage):
                role = "user"
            else:
                role = "AI"
            temp_msg.append({"role":role, "content":msg.content})
            st.session_state['message_history'] = temp_msg
            
        

#******************************************MAIN_UI*******************************************************

CONFIG = {'configurable': {'thread_id': st.session_state['thread_id']},
          "metadata": {'thread_id': st.session_state['thread_id']},
          "run_name":"chat_turn"}



for message in st.session_state['message_history']:
    with st.chat_message(message['role']):
        st.text(message['content'])

#{'role': 'user', 'content': 'Hi'}
#{'role': 'assistant', 'content': 'Hi=ello'}

user_input = st.chat_input('Type here')

if user_input:

    # first add the message to message_history
    st.session_state['message_history'].append({'role': 'user', 'content': user_input})
    with st.chat_message('user'):
        st.text(user_input)
        
    with st.chat_message("AI"):
        
        def ai_only_stream():
            for message, metadata in chatbot.stream( {'messages': [HumanMessage(content=user_input)]},
                            config=(CONFIG),
                            stream_mode = "messages"):
                
                if isinstance(message,AIMessage ):
                    yield message.content
                    
        ai_message = st.write_stream(ai_only_stream())
 
    
    # first add the message to message_history
    st.session_state['message_history'].append({'role': 'AI', 'content': ai_message})
    
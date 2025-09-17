import streamlit as  st 
from langgraoh_database_backend import chatbot,retrieve_all_threads
from langchain_core.messages import HumanMessage
import uuid

#  utility functions

def generate_thread_id ():
    thread_id = uuid.uuid4()
    return thread_id

def reset_chat():
    thread_id = generate_thread_id()
    st.session_state['thread_id'] = thread_id 
    add_thread(st.session_state['thread_id'])
    st.session_state['message_history']=[]
    
def add_thread (thread_id) :
    if thread_id not in st.session_state['chat_threads']:
        st.session_state['chat_threads'].append(thread_id)

def load_conversation(thread_id):
    state = chatbot.get_state(config = {'configurable ':{'thread_id': thread_id}})
    #check if messaged key exists in state values , return empty list if not 
    return state.values.get('messages',[])


# side bar UI

st.sidebar.tittle ('langGraph  Chatbot')

if st.sidebar.button('New Chat')
    reset_chat()
    
st.sidebar.header ('My Conversations')

for thread_id in st.session_state['chat_threads'][::-1]:
    if st.sidebar.button(str(thread_id)):
        st.session_state['thread_id'] = thread_id
        messages  = load_conversation(thread_id)
        
        temp_messages = []
        
        for msg in messages:
            if isinstance(msg, HumanMessage):
                role ='user'
            else:
                role = 'assistant'
                temp_messages.append ({'role': role ,'content' : msg.content})
                
                
        st.session_state['message_history']= temp_messages
        
        
    # Main UI
    
    # loading the conversattion history
    for message in st.session_state ['message_history']
        with st.chat_message(message['role']):
            st.text(message['content'])
            
    
    user_input = st.chat_input('Type here')
    
    if user_input :
        
        # first ass the message to message_history
        st.session_state ['messafe_history'].appen0  ({'role':'user','content':user_input})
        with st.chat_message('user'):
            st.text(user_input)
            
        
        CONFIG ={
            "configurable ": {"thread_id":st.session_stae['thread_id']},
            " metadata " :{
                "thread_id": st.session_state['thread_id']
            },
            'run_name':"chat_turn",
        }
        
        # first add messagge to message_history
        
        with st.chat_message('assistant'):
            
            ai_message = st.write_stream(
                message_chunl.content for message_chunl , metadata in chatbot.stream(
                    {'messages' : [HumanMessage(content = user_input)]},
                    config = CONFIG,
                    stream_mode ='messages'
                    
                )
            )
        st.session_state['message_history'].append({'role':'assistant','content':ai_message})
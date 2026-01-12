#streamlit ui 
from langchain_community.chat_message_histories import StreamlitChatMessageHistory
import streamlit as st
from db import get_conversations,create_conversation ,get_messeges , get_session,add_messege
from ai import get_chain_with_history
from auth_ui import show_auth_ui

#show auth ui 
if 'user_id' not in st.session_state:
    st.session_state.user_id = None

if st.session_state.user_id is None:
    show_auth_ui()

elif st.session_state.user_id is not None:
    #Sidebar
    st.sidebar.title('Converstaion')

    #process conversation in sidbar
    session = get_session()
    conversations = get_conversations(session,st.session_state.user_id)
    convs_titles = [conv.title for conv in conversations]
    convs_ids = [conv.id for conv in conversations]

    #display conversations
    selected_conv = st.sidebar.radio(
        "selected a conversation",
        options= ['new conversation'] + convs_titles
    )
    # update active conversation
    if selected_conv =='new conversation':
        st.session_state.active_conversation_id = None
    elif selected_conv in convs_titles:
        idx = convs_titles.index(selected_conv)
        st.session_state.active_conversation_id = convs_ids[idx]


    #load messages for active conversation
    if st.session_state.active_conversation_id is not None:
        conv_messages = get_messeges(session,st.session_state.active_conversation_id)
        idx = convs_ids.index(st.session_state.active_conversation_id)
        conv_title = convs_titles[idx]

    else:
        conv_messages = []
        conv_title = "new conversation"



    #chat ui 
    st.title(conv_title)
    msgs=StreamlitChatMessageHistory(key = 'chat_history')
    #show message for selected conversation
    #if conversation id is change update the message display
    if st.session_state.active_conversation_id != st.session_state.get('last_conversation_id'):
        st.session_state.last_conversation_id = st.session_state.active_conversation_id
        msgs.clear()
        for msg in conv_messages:
            if msg.role == 'human':
                msgs.add_user_message(msg.content)
            elif msg.role == 'ai':
                msgs.add_ai_message(msg.content)
        #if now messages 
        if not conv_messages and st.session_state.active_conversation_id is None:
            msgs.add_ai_message("Hello! How can I help you today?")


    #get chain with history 
    chain_with_history = get_chain_with_history(msgs)


    #display messages
    for msg in msgs.messages:
        st.chat_message(msg.type).write(msg.content)

    #handle user input
    if prompt_text := st.chat_input("type your message"):
        #check if conversation is active 
        if st.session_state.active_conversation_id is None:
            #create new conversation
            conv = create_conversation(session, title=prompt_text,user_id=st.session_state.user_id)
            st.session_state.active_conversation_id = conv.id
        
        #add user messages to db 
        add_messege(session, st.session_state.active_conversation_id, "human", prompt_text)

        #display user message
        st.chat_message("human").write(prompt_text)

        #get ai response
        with st.chat_message("ai"):
            response_placeholder = st.empty()
            full_response = ""
            for chunk in chain_with_history.stream(
                {"input": prompt_text},
                {"configurable":{"session_id":st.session_state.active_conversation_id}}
            ):
                full_response += chunk.content
            response_placeholder.markdown(full_response)
            
            #add ai response to db
            add_messege(session, st.session_state.active_conversation_id, "ai", full_response)

            #refresh conversation list
            st.rerun()
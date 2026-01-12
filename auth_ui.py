#show auth ui for login register 

import streamlit as st 
from auth import register_user,authenticate_user
from db import get_session

#show auth ui 
def show_auth_ui():
    session = get_session()
    
    tab1 , tab2 = st.tabs(['login','register'])
    with tab1:
        st.text_input('email',key='login_email')
        st.text_input('password',key='login_password',type='password')
        if st.button("Login"):
            email = st.session_state.login_email
            password = st.session_state.login_password
            
            if not email or not password:
                st.error("Please enter both email and password")
            else:
                st.write(f"Attempting login with email: {email}")
                user = authenticate_user(session, email, password)
                if user:
                    st.session_state.user_id = user.id
                    st.success("Logged in successfully")
                    st.rerun()
                else:
                    st.error("Invalid credentials")
    with tab2:
        st.text_input('email',key='register_email')
        st.text_input('password',key='register_password',type='password')
        if st.button("Register"):
            user = register_user(session, st.session_state.register_email, st.session_state.register_password)
            if user:
                st.success("Account created, you can login now")
            else:
                st.error("Email already exists")    
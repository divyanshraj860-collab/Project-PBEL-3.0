import streamlit as st

def check_login():
    # Disabled during development
    st.session_state.logged_in = True
    return
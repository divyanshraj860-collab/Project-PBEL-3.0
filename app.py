import streamlit as st

st.set_page_config(
    page_title="MindCare AI",
    page_icon="🧠",
    layout="wide"
)

# Skip login during development
st.session_state.logged_in = True

st.switch_page("pages/Home.py")
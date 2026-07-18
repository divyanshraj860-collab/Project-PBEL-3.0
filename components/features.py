import streamlit as st

def features():
    st.header("✨ Features")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.info("🧠 Mental Health Assessment")

    with col2:
        st.info("📊 AI Risk Prediction")

    with col3:
        st.info("📄 Professional Reports")
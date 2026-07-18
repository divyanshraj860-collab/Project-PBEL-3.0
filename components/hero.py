import streamlit as st

def hero():
    st.markdown("""
    <div style="text-align:center; padding:80px 20px;">
        <h1>🧠 MindCare AI</h1>
        <h2>Understand Your Mental Wellness with Artificial Intelligence</h2>
        <p>
            Professional AI-powered mental health monitoring,
            risk prediction, personalized recommendations,
            interactive analytics, and downloadable reports.
        </p>
    </div>
    """, unsafe_allow_html=True)
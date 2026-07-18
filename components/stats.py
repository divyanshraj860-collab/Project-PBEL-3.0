import streamlit as st

def stats():
    st.markdown("---")
    st.subheader("📈 Platform Statistics")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Assessments", "1,250+")

    with col2:
        st.metric("Accuracy", "94%")

    with col3:
        st.metric("Reports Generated", "980+")
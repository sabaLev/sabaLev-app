import streamlit as st

if 'email' not in st.session_state:
    st.session_state.email = ""

if 'show_hint' not in st.session_state:
    st.session_state.show_hint = True

def on_email_change():
    st.session_state.show_hint = False

col1, col2 = st.columns([3, 1])
with col1:
    email = st.text_input(
        "Email", 
        value=st.session_state.email,
        on_change=on_email_change,
        key="email_input"
    )
    
with col2:
    if st.session_state.show_hint or not email:
        st.markdown(
            '<div style="color: #888; font-style: italic; padding-top: 1.5rem;">user@example.com</div>',
            unsafe_allow_html=True
        )

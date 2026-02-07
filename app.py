import streamlit as st

col1, col2 = st.columns([2, 1])

with col1:
    # Основное поле
    user_input = st.text_input("Введите данные", label_visibility="collapsed")
    
with col2:
    # Плейсхолдер как статический текст
    if not user_input:
        st.markdown('<div style="color: #666; padding-top: 0.5rem;">пример@gmail.com</div>', 
                   unsafe_allow_html=True)

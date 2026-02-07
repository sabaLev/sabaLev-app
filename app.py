import streamlit as st

# Простейшая реализация с columns
st.subheader("Введите данные:")

# Email - разделяем на префикс и домен
col1, col2, col3 = st.columns([1, 3, 2])
with col1:
    st.markdown('<div style="padding-top: 0.5rem;">@</div>', unsafe_allow_html=True)
with col2:
    username = st.text_input("", placeholder="username", label_visibility="collapsed", key="user")
with col3:
    st.markdown('<div style="padding-top: 0.5rem; color: #666;">@gmail.com</div>', 
               unsafe_allow_html=True)

# Итог
if username:
    st.write(f"Ваш email: **{username}@gmail.com**")

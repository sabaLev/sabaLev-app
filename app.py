import streamlit as st

st.title("Двухколоночный макет")

# Создаем placeholder'ы для колонок
col1_placeholder = st.empty()
col2_placeholder = st.empty()

# Создаем контейнер для первой колонки
with col1_placeholder.container():
    st.subheader("Колонка 1")
    st.checkbox("Включить функцию 1", key="func1")
    st.text_input("Название проекта", key="project1")
    st.button("Сохранить 1", key="btn1")

# Создаем контейнер для второй колонки  
with col2_placeholder.container():
    st.subheader("Колонка 2")
    st.checkbox("Включить функцию 2", key="func2")
    st.text_input("Название задачи", key="task1")
    st.button("Сохранить 2", key="btn2")

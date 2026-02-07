import streamlit as st

st.set_page_config(layout="wide")

# Создаем основной контейнер
main_container = st.container()

with main_container:
    # Создаем две колонки
    left_col, right_col = st.columns(2)
    
    # Левая колонка в своем контейнере
    with left_col:
        col1_container = st.container()
        with col1_container:
            st.checkbox("Чекбокс 1", key="cb1")
            st.text_input("Введите текст 1", key="ti1")
            st.slider("Слайдер 1", 0, 100, 50, key="s1")
    
    # Правая колонка в своем контейнере
    with right_col:
        col2_container = st.container()
        with col2_container:
            st.checkbox("Чекбокс 2", key="cb2")
            st.text_input("Введите текст 2", key="ti2")
            st.slider("Слайдер 2", 0, 100, 30, key="s2")

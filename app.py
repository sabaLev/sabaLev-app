import streamlit as st

st.title("Форма регистрации")

# Используем beta_columns если доступно
try:
    col1, col2 = st.columns(2, vertical_alignment="top")
except:
    col1, col2 = st.columns(2)

with col1:
    st.subheader("Персональные данные")
    st.text_input("Имя", key="first_name")
    st.text_input("Фамилия", key="last_name")
    st.date_input("Дата рождения")
    st.radio("Пол", ["Мужской", "Женский"], horizontal=True)

with col2:
    st.subheader("Контактная информация")
    st.text_input("Email", type="default")
    st.text_input("Телефон", placeholder="+7 XXX XXX XX XX")
    st.text_area("Адрес", height=100)
    st.checkbox("Я согласен на обработку данных")

# Кнопка вне колонок
st.button("Зарегистрироваться", type="primary")

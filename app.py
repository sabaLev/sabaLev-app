import streamlet as st

# Метод 1: Две колонки в одной строке
col_label, col_input = st.columns([1, 3])
with col_label:
    st.write("Логин:")
with col_input:
    username = st.text_input("", placeholder="Введите логин", label_visibility="collapsed")

# Метод 2: С кнопкой рядом
col1, col2, col3 = st.columns([2, 4, 2])
with col1:
    st.write("Поиск:")
with col2:
    search_term = st.text_input("", placeholder="Введите запрос", label_visibility="collapsed")
with col3:
    st.button("Найти")

# Метод 3: Для формы
st.write("---")
col_a, col_b = st.columns(2)
with col_a:
    st.write("Email:")
    email = st.text_input("", placeholder="user@example.com", label_visibility="collapsed")
with col_b:
    st.write("Телефон:")
    phone = st.text_input("", placeholder="+7 999 123-45-67", label_visibility="collapsed")

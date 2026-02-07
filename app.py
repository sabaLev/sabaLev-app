import streamlit as st

# CSS для изменения стилей
st.markdown("""
<style>
/* Скрываем стандартный label */
div[data-testid="stTextInput"] > label {
    display: none !important;
}

/* Создаем inline контейнер */
.inline-input {
    display: flex;
    align-items: center;
    gap: 10px;
    margin-bottom: 1rem;
}
</style>
""", unsafe_allow_html=True)

# Создаем inline блок
st.markdown('<div class="inline-input">', unsafe_allow_html=True)
st.markdown('**Логин:**')
username = st.text_input("апрапрапр", placeholder="Введите логин", label_visibility="collapsed")
st.markdown('</div>', unsafe_allow_html=True)

# Еще пример
st.markdown('<div class="inline-input">', unsafe_allow_html=True)
st.markdown('**Пароль:**')
password = st.text_input("", type="password", placeholder="Введите пароль", label_visibility="collapsed")
st.markdown('</div>', unsafe_allow_html=True)

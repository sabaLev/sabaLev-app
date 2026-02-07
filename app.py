import streamlit as st

# Минимальные стили
st.markdown(
    """
    <style>
    div.row-widget.stRadio > div {
        flex-direction: row;
        align-items: center;
    }
    div.row-widget.stRadio > div[role="radiogroup"] > label {
        margin-right: 20px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

col1, col2 = st.columns(2)

with col1:
    # Группируем элементы в контейнер
    with st.container():
        st.write("**Левая панель**")
        st.checkbox("Согласен с условиями")
        st.text_input("Логин", key="login")
        st.radio("Выберите:", ["Да", "Нет"], horizontal=True)

with col2:
    with st.container():
        st.write("**Правая панель**")
        st.checkbox("Получать уведомления")
        st.text_input("Пароль", type="password", key="pass")
        st.select_slider("Уровень", options=["Низкий", "Средний", "Высокий"])

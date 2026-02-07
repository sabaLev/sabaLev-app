import streamlit as st

# Отключаем некоторые responsive-стили
st.markdown(
    """
    <style>
    .st-emotion-cache-1r6slb0 {
        flex-wrap: nowrap !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

col1, col2 = st.columns(2, gap="small")

with col1:
    # Используем markdown для создания блока
    st.markdown('<div style="min-height: 200px;">', unsafe_allow_html=True)
    st.checkbox("Опция A", value=True)
    st.text_input("Имя пользователя", placeholder="Введите имя")
    st.number_input("Количество", min_value=1, max_value=10, value=5)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div style="min-height: 200px;">', unsafe_allow_html=True)
    st.checkbox("Опция B")
    st.text_input("Email", placeholder="email@example.com")
    st.selectbox("Выберите вариант", ["Вариант 1", "Вариант 2", "Вариант 3"])
    st.markdown('</div>', unsafe_allow_html=True)

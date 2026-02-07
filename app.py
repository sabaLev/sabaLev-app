import streamlit as st

st.markdown("""
<style>
/* СБРАСЫВАЕМ ВСЕ СТИЛИ STREAMLIT ДЛЯ КОЛОНОК */
div[data-testid="column"] {
    width: auto !important;
    min-width: auto !important;
    max-width: none !important;
    flex: none !important;
    padding: 0 !important;
}

/* Наш контейнер для строки */
.panel-row-container {
    display: flex !important;
    width: 100% !important;
    margin-bottom: 15px !important;
}

/* Контейнер для поля ввода (фиксированная ширина) */
.input-wrapper {
    width: 80px !important;
    min-width: 80px !important;
    max-width: 80px !important;
    flex: 0 0 80px !important;
    margin-right: 10px !important;
}

/* Контейнер для текста */
.text-wrapper {
    flex: 1 !important;
    display: flex !important;
    align-items: center !important;
    justify-content: flex-end !important;
    padding-right: 15px !important;
}

/* Мобильная адаптация */
@media (max-width: 768px) {
    .input-wrapper {
        width: 70px !important;
        min-width: 70px !important;
        max-width: 70px !important;
        flex: 0 0 70px !important;
        margin-right: 8px !important;
    }
}

/* Заголовки */
.header-row {
    display: flex !important;
    width: 100% !important;
    margin-bottom: 10px !important;
    font-weight: bold !important;
}

.header-input {
    width: 80px !important;
    min-width: 80px !important;
    max-width: 80px !important;
    flex: 0 0 80px !important;
    margin-right: 10px !important;
    text-align: right !important;
}

.header-text {
    flex: 1 !important;
    text-align: right !important;
    padding-right: 15px !important;
}

@media (max-width: 768px) {
    .header-input {
        width: 70px !important;
        min-width: 70px !important;
        max-width: 70px !important;
        flex: 0 0 70px !important;
        margin-right: 8px !important;
    }
}
</style>
""", unsafe_allow_html=True)

st.title("Тест с абсолютным контролем")

# Заголовки
st.markdown('<div class="header-row">', unsafe_allow_html=True)
st.markdown('<div class="header-input">שורות</div>', unsafe_allow_html=True)
st.markdown('<div class="header-text">פאנלים</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Строка 1
st.markdown('<div class="panel-row-container">', unsafe_allow_html=True)

# Контейнер для поля ввода
st.markdown('<div class="input-wrapper">', unsafe_allow_html=True)
# Используем with st.container() чтобы изолировать
with st.container():
    st.number_input("", 0, 50, 0, key="r1", label_visibility="collapsed")
st.markdown('</div>', unsafe_allow_html=True)

# Контейнер для текста
st.markdown('<div class="text-wrapper">1</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# Строка 2
st.markdown('<div class="panel-row-container">', unsafe_allow_html=True)

st.markdown('<div class="input-wrapper">', unsafe_allow_html=True)
with st.container():
    st.number_input("", 0, 50, 0, key="r2", label_visibility="collapsed")
st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="text-wrapper">2</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

import streamlit as st

st.title("📱 Тест таблицы для мобильных")

# CSS, который гарантированно фиксирует строки
st.markdown("""
<style>
/* КОНТЕЙНЕР ДЛЯ СТРОКИ - ГЛАВНОЕ! */
.fixed-row {
    display: flex !important;
    flex-direction: row !important;
    align-items: center !important;
    width: 100% !important;
    margin-bottom: 15px !important;
    border: 2px solid #4CAF50 !important; /* Зеленая рамка для наглядности */
    padding: 10px !important;
    border-radius: 8px !important;
    background: #f9f9f9 !important;
}

/* Чекбокс - фиксированная ширина */
.fixed-checkbox {
    width: 50px !important;
    min-width: 50px !important;
    max-width: 50px !important;
    flex: 0 0 50px !important;
    margin-right: 15px !important;
}

/* Текст - занимает остальное пространство */
.fixed-text {
    flex: 1 !important;
    text-align: right !important;
    font-size: 18px !important;
    font-weight: normal !important;
    padding-right: 10px !important;
}

/* Заголовок таблицы */
.table-header {
    display: flex !important;
    width: 100% !important;
    margin-bottom: 10px !important;
    font-weight: bold !important;
    font-size: 16px !important;
    color: #333 !important;
}

.header-checkbox {
    width: 50px !important;
    margin-right: 15px !important;
    text-align: center !important;
}

.header-text {
    flex: 1 !important;
    text-align: right !important;
    padding-right: 10px !important;
}
</style>
""", unsafe_allow_html=True)

# Заголовок таблицы
st.markdown("""
<div class="table-header">
    <div class="header-checkbox">✓</div>
    <div class="header-text">שם פריט</div>
</div>
""", unsafe_allow_html=True)

# Строка 1
st.markdown('<div class="fixed-row">', unsafe_allow_html=True)

# Контейнер для чекбокса
st.markdown('<div class="fixed-checkbox">', unsafe_allow_html=True)
# Сам чекбокс
checkbox1 = st.checkbox("", key="cb1", label_visibility="collapsed")
st.markdown('</div>', unsafe_allow_html=True)

# Текст
st.markdown('<div class="fixed-text">מהדק הארקה</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# Строка 2
st.markdown('<div class="fixed-row">', unsafe_allow_html=True)

st.markdown('<div class="fixed-checkbox">', unsafe_allow_html=True)
checkbox2 = st.checkbox("", key="cb2", label_visibility="collapsed")
st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="fixed-text">מהדק אמצע</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# Строка 3
st.markdown('<div class="fixed-row">', unsafe_allow_html=True)

st.markdown('<div class="fixed-checkbox">', unsafe_allow_html=True)
checkbox3 = st.checkbox("", key="cb3", label_visibility="collapsed")
st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="fixed-text">בורג איסכורית</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# Информация для отладки
st.markdown("---")
st.write("**Что должно быть:**")
st.write("1. Каждая строка в зеленой рамке")
st.write("2. Чекбокс слева (фиксированные 50px)")
st.write("3. Текст справа (занимает остальное место)")
st.write("4. Всегда в одной строке, никогда не переносится")

st.write("**Состояние чекбоксов:**")
st.write(f"- Чекбокс 1: {checkbox1}")
st.write(f"- Чекбокс 2: {checkbox2}")
st.write(f"- Чекбокс 3: {checkbox3}")

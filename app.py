import streamlit as st

# CSS для мобильной адаптации
st.markdown("""
<style>
/* Базовые стили таблицы */
.panels-table {
    width: 100%;
    margin-bottom: 20px;
}

/* Строка таблицы */
.panels-row {
    display: flex;
    margin-bottom: 10px;
    align-items: center;
}

/* Колонка с полем ввода */
.input-column {
    flex: 1;
    padding-right: 10px;
}

/* Колонка с текстом (предустановленные числа) */
.text-column {
    flex: 1;
    display: flex;
    align-items: center;
    justify-content: center;
    min-height: 45px;
}

/* Число (просто текст) */
.panel-number {
    font-size: 16px;
    color: #333;
    font-weight: normal;
}

/* Адаптация для мобильных */
@media (max-width: 768px) {
    .panels-row {
        flex-direction: row !important; /* Важно: не переносим на новую строку */
        margin-bottom: 15px;
    }
    
    .input-column, .text-column {
        width: 50% !important;
        flex: 0 0 50% !important;
        padding-right: 5px;
        padding-left: 5px;
    }
    
    .panel-number {
        font-size: 16px;
        height: 44px;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    
    /* Поля ввода на мобильных */
    .stNumberInput > div > div > input {
        font-size: 16px !important;
        height: 44px !important;
    }
}

/* Заголовки */
.table-header {
    display: flex;
    margin-bottom: 10px;
    font-weight: bold;
    text-align: center;
}

.header-left, .header-right {
    flex: 1;
    padding: 5px;
}
</style>
""", unsafe_allow_html=True)

st.title("Тест таблицы для панелей")

# Заголовки таблицы
st.markdown("""
<div class="table-header">
    <div class="header-left" style="text-align: right;">שורות</div>
    <div class="header-right" style="text-align: right;">פאנלים</div>
</div>
""", unsafe_allow_html=True)

# Первая строка
st.markdown('<div class="panels-row">', unsafe_allow_html=True)
st.markdown('<div class="input-column">', unsafe_allow_html=True)
st.number_input("", 0, 50, 0, key="test_row_1", label_visibility="collapsed")
st.markdown('</div>', unsafe_allow_html=True)
st.markdown('<div class="text-column">', unsafe_allow_html=True)
st.markdown('<div class="panel-number">1</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Вторая строка
st.markdown('<div class="panels-row">', unsafe_allow_html=True)
st.markdown('<div class="input-column">', unsafe_allow_html=True)
st.number_input("", 0, 50, 0, key="test_row_2", label_visibility="collapsed")
st.markdown('</div>', unsafe_allow_html=True)
st.markdown('<div class="text-column">', unsafe_allow_html=True)
st.markdown('<div class="panel-number">2</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

st.markdown("---")
st.write("**На десктопе:** 2 колонки рядом")
st.write("**На мобильных:** 2 колонки рядом (не переносятся)")
st.write("Левая колонка: поле ввода (שורות)")
st.write("Правая колонка: текст (פאנלים)")

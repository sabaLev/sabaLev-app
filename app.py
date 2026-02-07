import streamlit as st

st.markdown("""
<style>
/* ФИКСИРУЕМ ширину колонок НАВСЕГДА */
.fixed-row {
    display: flex !important;
    flex-direction: row !important;
    align-items: center !important;
    margin-bottom: 10px !important;
    width: 100% !important;
}

/* Левая колонка - поле ввода (очень узкое) */
.fixed-input-col {
    width: 80px !important;
    min-width: 80px !important;
    max-width: 80px !important;
    flex: 0 0 80px !important;
    padding-right: 10px !important;
}

/* Правая колонка - текст (занимает остальное пространство) */
.fixed-text-col {
    flex: 1 !important;
    text-align: right !important;
    padding-right: 15px !important;
}

/* Делаем поле ввода компактным */
.compact-input input {
    width: 100% !important;
    min-width: 80px !important;
    max-width: 80px !important;
}

/* Для мобильных еще уменьшаем отступы */
@media (max-width: 768px) {
    .fixed-input-col {
        width: 70px !important;
        min-width: 70px !important;
        max-width: 70px !important;
        flex: 0 0 70px !important;
        padding-right: 8px !important;
    }
    
    .compact-input input {
        width: 100% !important;
        min-width: 70px !important;
        max-width: 70px !important;
        font-size: 16px !important;
        height: 44px !important;
    }
    
    .fixed-text-col {
        padding-right: 10px !important;
        font-size: 16px !important;
    }
}

/* Заголовки */
.table-header {
    display: flex !important;
    flex-direction: row !important;
    margin-bottom: 10px !important;
    font-weight: bold !important;
}

.header-left {
    width: 80px !important;
    min-width: 80px !important;
    max-width: 80px !important;
    padding-right: 10px !important;
    text-align: right !important;
}

.header-right {
    flex: 1 !important;
    text-align: right !important;
    padding-right: 15px !important;
}

@media (max-width: 768px) {
    .header-left {
        width: 70px !important;
        min-width: 70px !important;
        max-width: 70px !important;
        padding-right: 8px !important;
    }
    
    .header-right {
        padding-right: 10px !important;
    }
}
</style>
""", unsafe_allow_html=True)

st.title("Тест с фиксированной шириной")

# Заголовки
st.markdown('<div class="table-header">', unsafe_allow_html=True)
st.markdown('<div class="header-left">שורות</div>', unsafe_allow_html=True)
st.markdown('<div class="header-right">פאנלים</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Строка 1
st.markdown('<div class="fixed-row">', unsafe_allow_html=True)

# Левая колонка - поле ввода (фиксированная ширина)
st.markdown('<div class="fixed-input-col">', unsafe_allow_html=True)
st.markdown('<div class="compact-input">', unsafe_allow_html=True)
st.number_input("", 0, 50, 0, key="test1", label_visibility="collapsed")
st.markdown('</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Правая колонка - текст
st.markdown('<div class="fixed-text-col">', unsafe_allow_html=True)
st.markdown('<div style="height:45px; display:flex; align-items:center; justify-content:flex-end;">1</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# Строка 2
st.markdown('<div class="fixed-row">', unsafe_allow_html=True)

# Левая колонка - поле ввода
st.markdown('<div class="fixed-input-col">', unsafe_allow_html=True)
st.markdown('<div class="compact-input">', unsafe_allow_html=True)
st.number_input("", 0, 50, 0, key="test2", label_visibility="collapsed")
st.markdown('</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Правая колонка - текст
st.markdown('<div class="fixed-text-col">', unsafe_allow_html=True)
st.markdown('<div style="height:45px; display:flex; align-items:center; justify-content:flex-end;">2</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

st.markdown("---")
st.write("**На десктопе:** Левая колонка = 80px, правая = остальное")
st.write("**На мобильных:** Левая колонка = 70px, правая = остальное")
st.write("Поле ввода всегда компактное, цифра всегда справа от него")

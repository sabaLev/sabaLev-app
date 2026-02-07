import streamlit as st

st.markdown("""
<style>
/* Скрываем все границы и отступы Streamlit */
div[data-testid="column"] {
    min-width: 0px !important;
    padding: 0px !important;
    margin: 0px !important;
}

/* Главный контейнер, который НИКОГДА не ломается */
.super-fixed-container {
    display: flex !important;
    width: 100% !important;
    position: relative !important;
}

/* Невидимая граница посередине */
.middle-boundary {
    position: absolute !important;
    left: 50% !important;
    top: 0 !important;
    bottom: 0 !important;
    width: 1px !important;
    background: transparent !important;
    pointer-events: none !important;
    z-index: 9999 !important;
}

/* Левая часть (для поля ввода) */
.left-half {
    width: 50% !important;
    flex: 0 0 50% !important;
    max-width: 50% !important;
    padding-right: 10px !important;
    box-sizing: border-box !important;
}

/* Правая часть (для текста) */
.right-half {
    width: 50% !important;
    flex: 0 0 50% !important;
    max-width: 50% !important;
    padding-left: 10px !important;
    box-sizing: border-box !important;
    text-align: right !important;
}

/* Заголовки */
.header-container {
    display: flex !important;
    width: 100% !important;
    margin-bottom: 10px !important;
    font-weight: bold !important;
}

.header-left {
    width: 50% !important;
    flex: 0 0 50% !important;
    padding-right: 10px !important;
    text-align: right !important;
    box-sizing: border-box !important;
}

.header-right {
    width: 50% !important;
    flex: 0 0 50% !important;
    padding-left: 10px !important;
    text-align: right !important;
    box-sizing: border-box !important;
}

/* Мобильная адаптация */
@media (max-width: 768px) {
    .left-half {
        width: 40% !important;
        flex: 0 0 40% !important;
        max-width: 40% !important;
        padding-right: 5px !important;
    }
    
    .right-half {
        width: 60% !important;
        flex: 0 0 60% !important;
        max-width: 60% !important;
        padding-left: 5px !important;
    }
    
    .header-left {
        width: 40% !important;
        flex: 0 0 40% !important;
        padding-right: 5px !important;
    }
    
    .header-right {
        width: 60% !important;
        flex: 0 0 60% !important;
        padding-left: 5px !important;
    }
}
</style>
""", unsafe_allow_html=True)

st.title("Тест с невидимой границей")

# Заголовки
st.markdown('<div class="header-container">', unsafe_allow_html=True)
st.markdown('<div class="header-left">שורות</div>', unsafe_allow_html=True)
st.markdown('<div class="header-right">פאנלים</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Строка 1
st.markdown('<div class="super-fixed-container">', unsafe_allow_html=True)
# Невидимая граница посередине
st.markdown('<div class="middle-boundary"></div>', unsafe_allow_html=True)

# Левая половина - поле ввода
st.markdown('<div class="left-half">', unsafe_allow_html=True)
# Оборачиваем в контейнер чтобы ограничить ширину
with st.container():
    # Используем use_container_width=False чтобы не растягивалось
    st.number_input("", 0, 50, 0, key="fixed1", label_visibility="collapsed")
st.markdown('</div>', unsafe_allow_html=True)

# Правая половина - текст
st.markdown('<div class="right-half">', unsafe_allow_html=True)
st.markdown('<div style="height:45px; display:flex; align-items:center; justify-content:flex-end; font-size:16px;">1</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# Строка 2
st.markdown('<div class="super-fixed-container">', unsafe_allow_html=True)
st.markdown('<div class="middle-boundary"></div>', unsafe_allow_html=True)

st.markdown('<div class="left-half">', unsafe_allow_html=True)
with st.container():
    st.number_input("", 0, 50, 0, key="fixed2", label_visibility="collapsed")
st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="right-half">', unsafe_allow_html=True)
st.markdown('<div style="height:45px; display:flex; align-items:center; justify-content:flex-end; font-size:16px;">2</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

st.markdown("---")
st.write("Идея: есть невидимая граница посередине (50% ширины)")
st.write("Левая часть: всегда 50% (или 40% на мобильных)")
st.write("Правая часть: всегда 50% (или 60% на мобильных)")
st.write("Streamlit не может выйти за эти границы")

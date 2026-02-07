import streamlit as st

st.markdown("""
<style>
/* ОБЯЗАТЕЛЬНО для предотвращения переноса колонок */
[data-testid="column"] {
    min-width: 0px !important;
}

/* Для мобильных фиксируем ширину */
@media (max-width: 768px) {
    .mobile-fixed-row {
        display: flex !important;
        flex-direction: row !important;
        width: 100% !important;
    }
    
    .mobile-fixed-col {
        width: 50% !important;
        flex: 0 0 50% !important;
        min-width: 50% !important;
        max-width: 50% !important;
        padding: 0 5px !important;
    }
    
    .panel-number {
        font-size: 16px;
        height: 44px;
        display: flex;
        align-items: center;
        justify-content: center;
        padding: 12px 0;
    }
}

/* Для десктопа */
@media (min-width: 769px) {
    .desktop-col {
        width: 50% !important;
    }
}
</style>
""", unsafe_allow_html=True)

st.title("Тест с Streamlit columns")

# Заголовки
col1, col2 = st.columns(2)
with col1:
    st.markdown('<div style="text-align:right; font-weight:bold;">שורות</div>', unsafe_allow_html=True)
with col2:
    st.markdown('<div style="text-align:right; font-weight:bold;">פאנלים</div>', unsafe_allow_html=True)

# Строка 1
st.markdown('<div class="mobile-fixed-row">', unsafe_allow_html=True)
col1, col2 = st.columns(2)
with col1:
    st.markdown('<div class="mobile-fixed-col">', unsafe_allow_html=True)
    st.number_input("", 0, 50, 0, key="row1_input", label_visibility="collapsed")
    st.markdown('</div>', unsafe_allow_html=True)
with col2:
    st.markdown('<div class="mobile-fixed-col">', unsafe_allow_html=True)
    st.markdown('<div class="panel-number">1</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Строка 2
st.markdown('<div class="mobile-fixed-row">', unsafe_allow_html=True)
col1, col2 = st.columns(2)
with col1:
    st.markdown('<div class="mobile-fixed-col">', unsafe_allow_html=True)
    st.number_input("", 0, 50, 0, key="row2_input", label_visibility="collapsed")
    st.markdown('</div>', unsafe_allow_html=True)
with col2:
    st.markdown('<div class="mobile-fixed-col">', unsafe_allow_html=True)
    st.markdown('<div class="panel-number">2</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

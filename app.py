import streamlit as st

st.title("Тест лазейки №1: st.columns внутри")

st.markdown("""
<style>
/* Контейнер, который Streamlit должен уважать */
.my-container {
    border: 3px solid red;
    padding: 15px;
    margin: 20px 0;
    background: #fff9e6;
}
</style>

<div class="my-container">
""", unsafe_allow_html=True)

# ВАЖНО: Внутри HTML-контейнера создаем КОЛОНКИ STREAMLIT
col1, col2 = st.columns([1, 3])

with col1:
    st.checkbox("", key="test_cb_1", label_visibility="collapsed")

with col2:
    st.markdown('<div style="text-align:right; font-size:18px; padding:8px;">מהדק הארקה</div>', unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

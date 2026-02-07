import streamlit as st

# Минимальный CSS
st.markdown("""
<style>
@media (max-width: 640px) {
    .mobile-scroll {
        display: flex;
        min-width: 500px;
        overflow-x: auto;
        gap: 20px;
        padding: 10px 0;
    }
    .mobile-scroll > div {
        min-width: 250px;
        flex-shrink: 0;
    }
}
</style>
""", unsafe_allow_html=True)

st.title("Простая форма с горизонтальным скроллом")

st.markdown('<div class="mobile-scroll">', unsafe_allow_html=True)

# Блок 1
st.markdown('<div>', unsafe_allow_html=True)
st.subheader("Поле 1")
field1 = st.text_input("Введите текст 1", key="field1")
st.number_input("Число 1", 0, 100, 50, key="num1")
st.markdown('</div>')

# Блок 2  
st.markdown('<div>', unsafe_allow_html=True)
st.subheader("Поле 2")
field2 = st.text_input("Введите текст 2", key="field2")
st.selectbox("Выбор", ["Вариант A", "Вариант B"], key="select1")
st.markdown('</div>')

st.markdown('</div>')

if field1 or field2:
    st.success("Форма заполнена!")

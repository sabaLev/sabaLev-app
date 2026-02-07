import streamlit as st

st.set_page_config(layout="wide")

# CSS фикс
st.markdown("""
<style>
@media (max-width: 640px) {
    div[data-testid="column"] {
        min-width: calc(50% - 1rem) !important;
    }
}
</style>
""", unsafe_allow_html=True)

# Создаем две колонки
left_col, right_col = st.columns(2)

with left_col:
    st.checkbox("Опция A")
    st.text_input("Имя", key="name_left")
    
with right_col:
    st.checkbox("Опция B")
    st.text_input("Имя", key="name_right")

import streamlit as st

# Панель управления вверху
with st.expander("⚙️ Панель управления - нажмите чтобы открыть", expanded=True):
    col1, col2, col3 = st.columns(3)
    with col1:
        st.selectbox("Фильтр", ["Все", "Активные", "Завершенные"])
    with col2:
        st.slider("Диапазон", 0, 100, (25, 75))
    with col3:
        st.button("Применить")

# Основной контент
st.title("Основное содержимое")

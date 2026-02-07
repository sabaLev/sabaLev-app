import streamlit as st

# Всегда видимая панель управления
st.title("⚙️ Панель управления")
control_col1, control_col2, control_col3 = st.columns(3)
with control_col1:
    filter_option = st.selectbox("Фильтр", ["Все", "Новые", "Старые"])
with control_col2:
    date_range = st.date_input("Период")
with control_col3:
    if st.button("Обновить"):
        st.rerun()

st.divider()

# Основной контент
st.title("📊 Данные")
# ... ваш контент

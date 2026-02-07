import streamlit as st

st.title("Лучшее что можно сделать в нативном Streamlit")

# 1. Использовать number_input для чисел
st.subheader("1. Отдельные поля для чисел")
col1, col2 = st.columns(2)

with col1:
    price = st.number_input("Цена", min_value=0.0, value=100.0, step=0.01, format="%.2f")

with col2:
    quantity = st.number_input("Количество", min_value=0, value=1, step=1)

st.write(f"Итого: **{price * quantity:.2f}**")

# 2. Data editor с подсказками
st.subheader("2. Таблица с подсказками")
df = pd.DataFrame({
    'Число (нажмите 2 раза)': [100, 200],
    'Текст': ['A', 'B']
})

edited = st.data_editor(
    df,
    column_config={
        'Число (нажмите 2 раза)': st.column_config.NumberColumn(
            help="На телефоне: нажмите 2 раза для точного ввода"
        )
    }
)

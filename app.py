import streamlit as st
import pandas as pd

st.title("Таблица с динамической высотой")

# Больше данных для скролла
data = {
    'Параметр': [f'Параметр {i}' for i in range(1, 51)],
    'Значение': [f'Значение {i}' for i in range(1, 51)]
}
df = pd.DataFrame(data)

# Таблица с высотой и шириной
st.dataframe(
    df,
    use_container_width=True,
    height=400  # Фиксированная высота со скроллом
)

import streamlit as st
import pandas as pd
import numpy as np

st.title("Динамическая таблица")

# Пользователь выбирает количество строк
num_rows = st.slider("Количество строк:", 1, 100, 10)

# Генерируем данные
df = pd.DataFrame({
    'Колонка 1': [f'Строка {i}' for i in range(1, num_rows + 1)],
    'Колонка 2': np.random.randint(1, 100, num_rows)
})

# Отображаем таблицу
st.dataframe(
    df,
    use_container_width=True,
    height=min(400, num_rows * 35 + 50)  # Автоматическая высота
)

# Показываем статистику
st.write(f"Таблица занимает примерно {num_rows * 35 + 50}px по высоте")

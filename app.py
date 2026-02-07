import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")

st.title("Таблица на весь экран")

# Создаем данные
df = pd.DataFrame({
    'Колонка A': ['Строка 1', 'Строка 2', 'Строка 3', 'Строка 4', 'Строка 5'] * 10,
    'Колонка B': ['Данные 1', 'Данные 2', 'Данные 3', 'Данные 4', 'Данные 5'] * 10
})

# Таблица на всю ширину контейнера
st.dataframe(df, use_container_width=True)

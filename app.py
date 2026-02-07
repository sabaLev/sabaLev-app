import streamlit as st
import pandas as pd
from datetime import datetime

st.title("Таблица с типами полей Streamlit")

# Простая таблица
df = pd.DataFrame({
    'Текст': ['Введите текст здесь'],
    'Число': [50],
    'Чекбокс': [True],
    'Выбор': ['Вариант A']
})

edited_df = st.data_editor(
    df,
    column_config={
        'Текст': st.column_config.TextColumn("Текстовое поле"),
        'Число': st.column_config.NumberColumn("Числовое поле", step=1),
        'Чекбокс': st.column_config.CheckboxColumn("Флажок"),
        'Выбор': st.column_config.SelectboxColumn(
            "Выпадающий список",
            options=['Вариант A', 'Вариант B', 'Вариант C']
        )
    }
)

st.write("Отредактированные данные:")
st.write(edited_df)

import streamlit as st
import pandas as pd
from datetime import date

st.title("Демо всех типов полей")

df = pd.DataFrame({
    'Текст': ['Пример'],
    'Число': [100],
    'Десятичное': [50.5],
    'Чекбокс': [True],
    'Выбор': ['Опция A'],
    'Дата': [date(2023, 1, 1)],
    'Ссылка': ['https://example.com'],
    'Прогресс': [0.7]
})

edited = st.data_editor(
    df,
    column_config={
        'Текст': st.column_config.TextColumn("Текст", max_chars=50),
        'Число': st.column_config.NumberColumn("Целое", min_value=0, max_value=1000, step=1),
        'Десятичное': st.column_config.NumberColumn("Дробное", format="%.2f", step=0.1),
        'Чекбокс': st.column_config.CheckboxColumn("Статус"),
        'Выбор': st.column_config.SelectboxColumn("Список", options=['Опция A', 'Опция B', 'Опция C']),
        'Дата': st.column_config.DateColumn("Календарь"),
        'Ссылка': st.column_config.LinkColumn("Ссылка"),
        'Прогресс': st.column_config.ProgressColumn("Прогресс", format="%.0f%%")
    }
)

st.write("Итог:", edited)

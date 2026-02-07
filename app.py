import streamlit as st
import pandas as pd
from datetime import date, time

# Простая таблица с основными типами
df = pd.DataFrame({
    'Текст': ['Пример'],
    'Число': [100],
    'Чекбокс': [True],
    'Выбор': ['Вариант A'],
    'Дата': [date.today()],
    'Время': [time.now()]
})

edited = st.data_editor(
    df,
    column_config={
        'Текст': st.column_config.TextColumn("Текст"),
        'Число': st.column_config.NumberColumn("Число", step=1),
        'Чекбокс': st.column_config.CheckboxColumn("Включено"),
        'Выбор': st.column_config.SelectboxColumn(
            "Выбор",
            options=['Вариант A', 'Вариант B', 'Вариант C']
        ),
        'Дата': st.column_config.DateColumn("Дата"),
        'Время': st.column_config.TimeColumn("Время")
    }
)

st.write("Вы ввели:", edited)

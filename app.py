import streamlit as st
import pandas as pd

st.title("Адаптивная таблица")

df = pd.DataFrame({
    'Левый столбец': ['Текст 1', 'Текст 2', 'Текст 3'],
    'Правый столбец': ['Значение 1', 'Значение 2', 'Значение 3']
})

# Редактируемая таблица с настройкой ширины
edited_df = st.data_editor(
    df,
    use_container_width=True,
    hide_index=True,
    column_config={
        'Левый столбец': st.column_config.Column(width="large"),
        'Правый столбец': st.column_config.Column(width="large")
    }
)

import streamlit as st
import pandas as pd

st.title("Редактируемая таблица 2x2")

# Создаем DataFrame
df = pd.DataFrame(
    [[10, 20], 
     [30, 40]],
    columns=['Колонка A', 'Колонка B']
)

# Редактируемая таблица
edited_df = st.data_editor(df)

st.write("Измененные данные:")
st.write(edited_df)

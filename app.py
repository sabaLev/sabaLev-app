import streamlit as st
import pandas as pd

st.title("Контейнер с таблицей")

# Создаем контейнер на всю ширину
container = st.container()

with container:
    # Таблица внутри контейнера
    df = pd.DataFrame({
        'Слева': ['A1', 'A2', 'A3', 'A4', 'A5'],
        'Справа': ['B1', 'B2', 'B3', 'B4', 'B5']
    })
    
    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )

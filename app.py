# Установите: pip install streamlit-aggrid
from st_aggrid import AgGrid, GridOptionsBuilder
import pandas as pd
import streamlit as st

st.title("AgGrid с мобильной оптимизацией")

df = pd.DataFrame({
    'ID': [1, 2, 3],
    'Цена': [100.0, 200.0, 300.0],
    'Количество': [5, 3, 7]
})

gb = GridOptionsBuilder.from_dataframe(df)

# Настройка колонок для чисел
gb.configure_column('Цена', type=["numericColumn", "numberColumnFilter"])
gb.configure_column('Количество', type=["numericColumn"])

grid_options = gb.build()

AgGrid(
    df,
    gridOptions=grid_options,
    enable_enterprise_modules=False,
    height=300,
    theme='streamlit'
)

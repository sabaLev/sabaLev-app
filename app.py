import streamlit as st
import pandas as pd

df = pd.DataFrame({
    'Цена': [100, 200],
    'Кол-во': [5, 3]
})

edited = st.data_editor(
    df,
    column_config={
        'Цена': st.column_config.NumberColumn(step=10),
        'Кол-во': st.column_config.NumberColumn(step=1)
    }
)

import streamlit as st
import pandas as pd

# Просто таблица на всю ширину
df = pd.DataFrame({'A': [1, 2], 'B': [3, 4]})
st.dataframe(df, use_container_width=True)

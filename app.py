import streamlit as st
import pandas as pd

st.markdown("""
<style>
/* Таблица на всю ширину */
.stDataFrame {
    width: 100% !important;
}

/* Ячейки таблицы */
.stDataFrame td, .stDataFrame th {
    padding: 12px !important;
    text-align: left !important;
}

/* Адаптивность для мобильных */
@media (max-width: 768px) {
    .stDataFrame {
        font-size: 14px !important;
    }
    .stDataFrame td, .stDataFrame th {
        padding: 8px !important;
    }
}
</style>
""", unsafe_allow_html=True)

st.title("Респонсив таблица")

df = pd.DataFrame({
    'Название': ['Элемент 1', 'Элемент 2', 'Элемент 3', 'Элемент 4'],
    'Описание': ['Длинное описание первого элемента', 
                 'Описание второго элемента',
                 'Третье описание',
                 'Четвертое описание элемента']
})

st.dataframe(df, use_container_width=True)

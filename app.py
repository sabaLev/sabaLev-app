import streamlit as st
import pandas as pd
from datetime import datetime, time, date

st.title("Демонстрация типов полей таблицы")

# Создаем простую таблицу с одним набором данных
df = pd.DataFrame({
    'ID': [1],
    'Название': ['Пример товара'],
    'Количество': [10],
    'Цена': [100.50],
    'Активен': [True],
    'Категория': ['Электроника'],
    'Дата_добавления': [date.today()],
    'Время_доставки': [time(14, 30)],  # Конкретное время 14:30
    'Последнее_обновление': [datetime.now()],
    'Статус': ['В обработке']
})

# Отображаем таблицу с возможностью редактирования
edited_df = st.data_editor(
    df,
    num_rows="fixed",
    use_container_width=True,
    column_config={
        'ID': st.column_config.NumberColumn(
            "ID",
            disabled=True,
            help="Идентификатор записи"
        ),
        'Название': st.column_config.TextColumn(
            "Название товара",
            max_chars=100,
            help="Введите название до 100 символов"
        ),
        'Количество': st.column_config.NumberColumn(
            "Количество",
            min_value=0,
            max_value=1000,
            step=1,
            format="%d шт.",
            help="Количество товара на складе"
        ),
        'Цена': st.column_config.NumberColumn(
            "Цена",
            min_value=0.0,
            max_value=10000.0,
            step=0.01,
            format="%.2f ₽",
            help="Цена товара в рублях"
        ),
        'Активен': st.column_config.CheckboxColumn(
            "Активен",
            help="Товар доступен для продажи"
        ),
        'Категория': st.column_config.SelectboxColumn(
            "Категория",
            options=['Электроника', 'Одежда', 'Книги', 'Продукты', 'Другое'],
            help="Выберите категорию товара"
        ),
        'Дата_добавления': st.column_config.DateColumn(
            "Дата добавления",
            format="DD.MM.YYYY",
            help="Дата добавления товара"
        ),
        'Время_доставки': st.column_config.TimeColumn(
            "Время доставки",
            format="HH:mm",
            help="Планируемое время доставки"
        ),
        'Последнее_обновление': st.column_config.DatetimeColumn(
            "Последнее обновление",
            format="DD.MM.YYYY HH:mm",
            help="Дата и время последнего обновления"
        ),
        'Статус': st.column_config.TextColumn(
            "Статус заказа",
            help="Текущий статус обработки"
        )
    }
)

st.write("### Отредактированные данные:")
st.dataframe(edited_df)

# Показать разницу между исходными и отредактированными данными
st.write("### Сравнение с исходными данными:")
col1, col2 = st.columns(2)
with col1:
    st.write("**Исходные данные:**")
    st.write(df)
with col2:
    st.write("**Отредактированные данные:**")
    st.write(edited_df)

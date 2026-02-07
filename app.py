import streamlit as st
import pandas as pd

st.title("🛒 Таблица товаров с управлением")

# Инициализация
if 'products' not in st.session_state:
    st.session_state.products = pd.DataFrame({
        'Товар': ['Ноутбук', 'Смартфон', 'Наушники', 'Клавиатура'],
        'Категория': ['Электроника', 'Электроника', 'Аксессуары', 'Аксессуары'],
        'Цена': [50000, 25000, 5000, 2000],
        'Количество': [10, 25, 50, 30]
    })

st.write("### Управление количеством товаров")

# Создаем отдельные кнопки для каждой строки
for idx, row in st.session_state.products.iterrows():
    with st.container():
        cols = st.columns([3, 1, 2, 2, 2])
        
        with cols[0]:
            st.markdown(f"**{row['Товар']}**")
            st.caption(f"{row['Категория']} • {row['Цена']:,.0f} ₽")
        
        with cols[1]:
            st.markdown(f"<div style='text-align: center; font-size: 1.2em; font-weight: bold;'>{row['Количество']}</div>", 
                       unsafe_allow_html=True)
        
        with cols[2]:
            # Кнопки управления в маленьком формате
            btn_col1, btn_col2 = st.columns(2)
            with btn_col1:
                if st.button("➖", key=f"dec_{idx}", use_container_width=True):
                    new_qty = max(0, row['Количество'] - 1)
                    st.session_state.products.at[idx, 'Количество'] = new_qty
                    st.rerun()
            with btn_col2:
                if st.button("➕", key=f"inc_{idx}", use_container_width=True):
                    st.session_state.products.at[idx, 'Количество'] = row['Количество'] + 1
                    st.rerun()
        
        with cols[3]:
            # Быстрые действия
            if st.button("📥 +5", key=f"fast5_{idx}", use_container_width=True):
                st.session_state.products.at[idx, 'Количество'] += 5
                st.rerun()
        
        with cols[4]:
            if st.button("🔄 0", key=f"reset_{idx}", use_container_width=True):
                st.session_state.products.at[idx, 'Количество'] = 0
                st.rerun()
        
        # Прогресс-бар для наглядности
        max_qty = 100
        progress = min(row['Количество'] / max_qty, 1.0)
        st.progress(progress, text=f"{row['Количество']} из {max_qty}")

# Сводная информация
st.write("---")
st.write("### 📈 Сводка по складу")

total_value = (st.session_state.products['Цена'] * st.session_state.products['Количество']).sum()
total_items = st.session_state.products['Количество'].sum()

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Всего товаров", f"{total_items} шт.")
with col2:
    st.metric("Общая стоимость", f"{total_value:,.0f} ₽")
with col3:
    avg_price = total_value / total_items if total_items > 0 else 0
    st.metric("Средняя цена", f"{avg_price:,.0f} ₽")

# Фильтрация
st.write("---")
category_filter = st.multiselect(
    "Фильтр по категориям:",
    options=st.session_state.products['Категория'].unique(),
    default=st.session_state.products['Категория'].unique()
)

filtered_df = st.session_state.products[
    st.session_state.products['Категория'].isin(category_filter)
]

st.dataframe(
    filtered_df,
    use_container_width=True,
    column_config={
        "Товар": st.column_config.TextColumn(width="medium"),
        "Категория": st.column_config.TextColumn(width="small"),
        "Цена": st.column_config.NumberColumn(
            "Цена (₽)",
            format="%d ₽"
        ),
        "Количество": st.column_config.NumberColumn(
            "Кол-во",
            help="Используйте кнопки выше для изменения"
        )
    }
)

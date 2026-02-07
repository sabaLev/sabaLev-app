import streamlit as st
import pandas as pd

# Инициализация данных
if 'inventory' not in st.session_state:
    st.session_state.inventory = pd.DataFrame({
        'ID': [1, 2, 3, 4],
        'Товар': ['Ноутбук', 'Мышь', 'Клавиатура', 'Монитор'],
        'На складе': [15, 42, 28, 8],
        'Изменение': [0, 0, 0, 0]  # Для отслеживания изменений
    })

st.title("📦 Управление складом")

# Функция для создания интерфейса управления
def create_control_interface():
    st.write("### Изменение количества:")
    
    for idx, row in st.session_state.inventory.iterrows():
        col1, col2, col3, col4, col5 = st.columns([3, 1, 1, 1, 2])
        
        with col1:
            st.write(f"**{row['Товар']}** (ID: {row['ID']})")
            st.caption(f"На складе: {row['На складе']} шт.")
        
        with col2:
            if st.button("➖5", key=f"dec5_{idx}"):
                st.session_state.inventory.at[idx, 'На складе'] = max(0, row['На складе'] - 5)
                st.session_state.inventory.at[idx, 'Изменение'] -= 5
        
        with col3:
            if st.button("➖1", key=f"dec1_{idx}"):
                st.session_state.inventory.at[idx, 'На складе'] = max(0, row['На складе'] - 1)
                st.session_state.inventory.at[idx, 'Изменение'] -= 1
        
        with col4:
            if st.button("➕1", key=f"inc1_{idx}"):
                st.session_state.inventory.at[idx, 'На складе'] = row['На складе'] + 1
                st.session_state.inventory.at[idx, 'Изменение'] += 1
        
        with col5:
            if st.button("➕5", key=f"inc5_{idx}"):
                st.session_state.inventory.at[idx, 'На складе'] = row['На складе'] + 5
                st.session_state.inventory.at[idx, 'Изменение'] += 5
        
        # Отображаем изменение
        change = st.session_state.inventory.at[idx, 'Изменение']
        if change != 0:
            change_color = "green" if change > 0 else "red"
            change_symbol = "📈" if change > 0 else "📉"
            st.markdown(
                f"<div style='color:{change_color}; margin-left: 20px;'>"
                f"{change_symbol} Изменение: {change:+d}</div>",
                unsafe_allow_html=True
            )
        
        st.divider()

# Основной интерфейс
col_left, col_right = st.columns([2, 1])

with col_left:
    st.write("### Текущие запасы")
    st.dataframe(
        st.session_state.inventory[['ID', 'Товар', 'На складе']],
        use_container_width=True,
        hide_index=True
    )

with col_right:
    st.write("### Сводка")
    total_items = st.session_state.inventory['На складе'].sum()
    low_stock = (st.session_state.inventory['На складе'] < 10).sum()
    
    st.metric("Всего товаров", f"{total_items} шт.")
    st.metric("Товаров мало (<10)", f"{low_stock} шт.", delta_color="inverse")
    
    if low_stock > 0:
        st.warning(f"⚠️ {low_stock} товаров требуют пополнения!")

# Интерфейс управления
create_control_interface()

# Кнопки управления
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("💾 Сохранить изменения", use_container_width=True):
        # Здесь обычно сохранение в БД
        st.success("Изменения сохранены в базу данных!")
        
with col2:
    if st.button("📋 Экспорт в Excel", use_container_width=True):
        # Создаем Excel файл
        import io
        buffer = io.BytesIO()
        with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
            st.session_state.inventory.to_excel(writer, index=False)
        
        st.download_button(
            label="Скачать Excel",
            data=buffer.getvalue(),
            file_name="склад_запасы.xlsx",
            mime="application/vnd.ms-excel"
        )

with col3:
    if st.button("🔄 Сбросить все", use_container_width=True):
        # Возвращаем исходные значения
        st.session_state.inventory['На складе'] = [15, 42, 28, 8]
        st.session_state.inventory['Изменение'] = [0, 0, 0, 0]
        st.rerun()

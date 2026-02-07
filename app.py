import streamlit as st
import pandas as pd

st.title("➕➖ Простая интерактивная таблица")

# Инициализация данных
if 'data' not in st.session_state:
    st.session_state.data = [
        {"id": 1, "name": "Товар A", "quantity": 10, "price": 100},
        {"id": 2, "name": "Товар B", "quantity": 5, "price": 200},
        {"id": 3, "name": "Товар C", "quantity": 8, "price": 150},
        {"id": 4, "name": "Товар D", "quantity": 12, "price": 80}
    ]

st.write("### Таблица товаров")

# Заголовки
cols = st.columns([1, 2, 2, 2, 1])
with cols[0]:
    st.write("**ID**")
with cols[1]:
    st.write("**Название**")
with cols[2]:
    st.write("**Количество**")
with cols[3]:
    st.write("**Цена**")
with cols[4]:
    st.write("**Сумма**")

st.divider()

# Отображаем строки
for idx, item in enumerate(st.session_state.data):
    row_cols = st.columns([1, 2, 2, 2, 1])
    
    with row_cols[0]:
        st.write(f"**{item['id']}**")
    
    with row_cols[1]:
        st.write(f"**{item['name']}**")
    
    with row_cols[2]:
        # Ячейка с кнопками для количества
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col1:
            if st.button("➖", key=f"dec_{idx}"):
                st.session_state.data[idx]['quantity'] = max(0, item['quantity'] - 1)
                st.rerun()
        
        with col2:
            st.write(f"**{item['quantity']}**")
        
        with col3:
            if st.button("➕", key=f"inc_{idx}"):
                st.session_state.data[idx]['quantity'] = item['quantity'] + 1
                st.rerun()
    
    with row_cols[3]:
        # Ячейка с кнопками для цены
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col1:
            if st.button("−", key=f"price_dec_{idx}"):
                st.session_state.data[idx]['price'] = max(0, item['price'] - 10)
                st.rerun()
        
        with col2:
            st.write(f"**{item['price']} ₽**")
        
        with col3:
            if st.button("+", key=f"price_inc_{idx}"):
                st.session_state.data[idx]['price'] = item['price'] + 10
                st.rerun()
    
    with row_cols[4]:
        total = item['quantity'] * item['price']
        st.write(f"**{total} ₽**")
    
    if idx < len(st.session_state.data) - 1:
        st.divider()

# Итоги
st.write("---")
total_items = sum(item['quantity'] for item in st.session_state.data)
total_value = sum(item['quantity'] * item['price'] for item in st.session_state.data)

st.metric("Всего товаров", f"{total_items} шт.")
st.metric("Общая стоимость", f"{total_value} ₽")

# Сброс
if st.button("🔄 Сбросить все значения"):
    st.session_state.data = [
        {"id": 1, "name": "Товар A", "quantity": 10, "price": 100},
        {"id": 2, "name": "Товар B", "quantity": 5, "price": 200},
        {"id": 3, "name": "Товар C", "quantity": 8, "price": 150},
        {"id": 4, "name": "Товар D", "quantity": 12, "price": 80}
    ]
    st.rerun()

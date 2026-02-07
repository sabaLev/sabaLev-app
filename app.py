import streamlit as st
import pandas as pd
import numpy as np

# CSS для стилизации кнопок внутри таблицы
st.markdown("""
<style>
/* Стили для кнопок в таблице */
.button-cell {
    text-align: center !important;
    padding: 5px !important;
}

.increment-button {
    background: #4CAF50;
    color: white;
    border: none;
    border-radius: 50%;
    width: 30px;
    height: 30px;
    cursor: pointer;
    font-weight: bold;
}

.decrement-button {
    background: #f44336;
    color: white;
    border: none;
    border-radius: 50%;
    width: 30px;
    height: 30px;
    cursor: pointer;
    font-weight: bold;
}

/* Контейнер для кнопок и значения */
.counter-container {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 10px;
}

.counter-value {
    font-weight: bold;
    min-width: 30px;
    text-align: center;
}
</style>
""", unsafe_allow_html=True)

# Инициализация данных
if 'table_data' not in st.session_state:
    st.session_state.table_data = pd.DataFrame({
        'Товар': ['Яблоки', 'Бананы', 'Апельсины', 'Манго'],
        'Количество': [10, 15, 8, 12],
        'Цена': [100, 80, 120, 200],
        'Управление': ['🔽  ⏺️  🔼'] * 4  # Заглушка
    })

st.title("🛒 Таблица с интерактивными счетчиками")

# Создаем кастомные столбцы с кнопками
def create_counter_column():
    """Создает столбец с кнопками +/-"""
    html_output = []
    
    for i, row in st.session_state.table_data.iterrows():
        product = row['Товар']
        current_value = st.session_state.get(f'counter_{product}', row['Количество'])
        
        html = f"""
        <div class="counter-container">
            <button class="decrement-button" 
                    onclick="decrementCounter('{product}')">-</button>
            <div class="counter-value" id="value_{product}">{current_value}</div>
            <button class="increment-button" 
                    onclick="incrementCounter('{product}')">+</button>
        </div>
        """
        html_output.append(html)
    
    return html_output

# JavaScript для обновления значений
js_code = """
<script>
function updateCounter(product, delta) {
    // Отправляем данные в Streamlit
    window.parent.postMessage({
        type: 'streamlit:setComponentValue',
        value: product + ':' + delta
    }, '*');
    
    // Обновляем отображение
    const elem = document.getElementById('value_' + product);
    if (elem) {
        const current = parseInt(elem.innerText);
        elem.innerText = current + delta;
    }
}

function incrementCounter(product) {
    updateCounter(product, 1);
}

function decrementCounter(product) {
    updateCounter(product, -1);
}
</script>
"""

# Отображаем таблицу
st.write("### Интерактивная таблица товаров")

# Основная таблица
display_df = st.session_state.table_data.copy()
st.dataframe(
    display_df,
    use_container_width=True,
    hide_index=True,
    column_config={
        "Товар": st.column_config.TextColumn(width="medium"),
        "Количество": st.column_config.NumberColumn(width="small"),
        "Цена": st.column_config.NumberColumn(
            "Цена (₽)",
            format="₽%d",
            width="small"
        ),
        "Управление": st.column_config.Column(width="large")
    }
)

# Кастомные кнопки под таблицей
st.write("### Управление количеством:")

# Создаем строки с кнопками для каждого товара
for i, row in st.session_state.table_data.iterrows():
    product = row['Товар']
    current_value = st.session_state.get(f'counter_{product}', row['Количество'])
    price = row['Цена']
    total = current_value * price
    
    col1, col2, col3, col4, col5 = st.columns([2, 1, 1, 1, 2])
    
    with col1:
        st.write(f"**{product}**")
    
    with col2:
        if st.button("➖", key=f"dec_{product}"):
            st.session_state[f'counter_{product}'] = max(0, current_value - 1)
            st.rerun()
    
    with col3:
        st.markdown(f"<div style='text-align: center; font-weight: bold; font-size: 1.2em;'>{current_value}</div>", 
                   unsafe_allow_html=True)
    
    with col4:
        if st.button("➕", key=f"inc_{product}"):
            st.session_state[f'counter_{product}'] = current_value + 1
            st.rerun()
    
    with col5:
        st.write(f"**Итого:** ₽{total}")

# Обновляем общую сумму
total_sum = sum([
    st.session_state.get(f'counter_{row["Товар"]}', row['Количество']) * row['Цена']
    for _, row in st.session_state.table_data.iterrows()
])

st.success(f"💰 **Общая сумма заказа: ₽{total_sum}**")

# Кнопки управления
col_reset, col_update = st.columns(2)
with col_reset:
    if st.button("🔄 Сбросить все", use_container_width=True):
        for _, row in st.session_state.table_data.iterrows():
            st.session_state[f'counter_{row["Товар"]}'] = row['Количество']
        st.rerun()

with col_update:
    if st.button("💾 Сохранить изменения", use_container_width=True):
        # Обновляем данные в таблице
        for i, row in st.session_state.table_data.iterrows():
            product = row['Товар']
            st.session_state.table_data.at[i, 'Количество'] = st.session_state.get(
                f'counter_{product}', row['Количество']
            )
        st.success("Изменения сохранены!")

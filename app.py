import streamlit as st
import pandas as pd

st.title("🔄 Таблица с кнопками в ячейках")

# Инициализация данных
if 'product_data' not in st.session_state:
    st.session_state.product_data = pd.DataFrame({
        'Товар': ['Яблоки 🍎', 'Бананы 🍌', 'Апельсины 🍊'],
        'Цена': [100, 80, 120],
        'Количество': [10, 15, 8],
        'Управление': ['[-] 10 [+]', '[-] 15 [+]', '[-] 8 [+]']
    })

# Создаем кастомный HTML для кнопок
def create_cell_with_buttons(value, row_index):
    """Создает ячейку с кнопками +/-"""
    return f"""
    <div style="display: flex; align-items: center; justify-content: center; gap: 10px;">
        <button onclick="decrement({row_index})" 
                style="width: 30px; height: 30px; border-radius: 50%; border: none; background: #ff6b6b; color: white; font-weight: bold; cursor: pointer;">
            -
        </button>
        <span style="font-weight: bold; min-width: 30px; text-align: center;">{value}</span>
        <button onclick="increment({row_index})" 
                style="width: 30px; height: 30px; border-radius: 50%; border: none; background: #4ecdc4; color: white; font-weight: bold; cursor: pointer;">
            +
        </button>
    </div>
    """

# JavaScript для обработки
js_code = f"""
<script>
function increment(rowIndex) {{
    window.parent.postMessage({{
        type: 'streamlit:setComponentValue',
        value: 'INC:' + rowIndex
    }}, '*');
}}

function decrement(rowIndex) {{
    window.parent.postMessage({{
        type: 'streamlit:setComponentValue',
        value: 'DEC:' + rowIndex
    }}, '*');
}}
</script>
"""

# Отображаем таблицу с помощью st.dataframe
st.write("### Интерактивная таблица с кнопками в ячейках")

# Создаем HTML таблицу
html_table = """
<style>
.custom-table {
    width: 100%;
    border-collapse: collapse;
    margin: 20px 0;
    font-family: Arial, sans-serif;
}

.custom-table th {
    background-color: #4CAF50;
    color: white;
    padding: 12px;
    text-align: left;
}

.custom-table td {
    padding: 12px;
    border-bottom: 1px solid #ddd;
    text-align: center;
    vertical-align: middle;
}

.cell-buttons {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 10px;
}

.qty-btn {
    width: 30px;
    height: 30px;
    border-radius: 50%;
    border: none;
    font-weight: bold;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
}

.qty-btn.minus {
    background-color: #ff6b6b;
    color: white;
}

.qty-btn.plus {
    background-color: #4ecdc4;
    color: white;
}
</style>

<table class="custom-table">
    <thead>
        <tr>
            <th>Товар</th>
            <th>Цена (₽)</th>
            <th>Количество</th>
            <th>Сумма (₽)</th>
        </tr>
    </thead>
    <tbody>
"""

# Заполняем таблицу данными
for idx, row in st.session_state.product_data.iterrows():
    total = row['Цена'] * row['Количество']
    html_table += f"""
    <tr>
        <td><strong>{row['Товар']}</strong></td>
        <td>{row['Цена']} ₽</td>
        <td>
            <div class="cell-buttons">
                <button class="qty-btn minus" onclick="decrement({idx})">-</button>
                <span style="font-weight: bold; min-width: 30px;">{row['Количество']}</span>
                <button class="qty-btn plus" onclick="increment({idx})">+</button>
            </div>
        </td>
        <td><strong>{total} ₽</strong></td>
    </tr>
    """

html_table += """
    </tbody>
</table>
""" + js_code

# Отображаем таблицу
st.components.v1.html(html_table, height=300)

# Обработка кнопок
button_action = st.text_input("", key="button_action", label_visibility="collapsed")
if button_action:
    if button_action.startswith("INC:"):
        row_idx = int(button_action.split(":")[1])
        st.session_state.product_data.at[row_idx, 'Количество'] += 1
        st.rerun()
    elif button_action.startswith("DEC:"):
        row_idx = int(button_action.split(":")[1])
        st.session_state.product_data.at[row_idx, 'Количество'] = max(0, 
            st.session_state.product_data.at[row_idx, 'Количество'] - 1)
        st.rerun()

# Итоговая сумма
total_sum = sum(st.session_state.product_data['Цена'] * st.session_state.product_data['Количество'])
st.success(f"💰 **Общая сумма: {total_sum} ₽**")

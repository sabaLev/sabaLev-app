import streamlit as st
import pandas as pd

st.title("➕➖ Кнопки прямо в ячейках таблицы")

# Простой DataFrame
data = pd.DataFrame({
    'Понедельник': [5, 3, 7],
    'Вторник': [8, 4, 6],
    'Среда': [2, 9, 5],
    'Четверг': [6, 7, 8],
    'Пятница': [4, 5, 9]
}, index=['Задача 1', 'Задача 2', 'Задача 3'])

st.write("### Часы работы по задачам")

# Создаем HTML таблицу с кнопками в каждой ячейке
html_table = """
<style>
.hours-table {
    border-collapse: collapse;
    width: 100%;
    margin: 20px 0;
}

.hours-table th, .hours-table td {
    border: 1px solid #ddd;
    padding: 8px;
    text-align: center;
    min-width: 100px;
}

.hours-table th {
    background-color: #4CAF50;
    color: white;
    position: sticky;
    top: 0;
}

.hours-table tr:nth-child(even) {
    background-color: #f9f9f9;
}

.hours-table tr:hover {
    background-color: #f5f5f5;
}

.cell-controls {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 5px;
}

.hour-btn {
    width: 25px;
    height: 25px;
    border-radius: 4px;
    border: 1px solid #ccc;
    background: white;
    cursor: pointer;
    font-size: 14px;
    display: flex;
    align-items: center;
    justify-content: center;
}

.hour-btn.minus {
    background: #ffebee;
    color: #c62828;
    border-color: #ffcdd2;
}

.hour-btn.plus {
    background: #e8f5e8;
    color: #2e7d32;
    border-color: #c8e6c9;
}

.hour-value {
    font-weight: bold;
    min-width: 30px;
    text-align: center;
}
</style>

<table class="hours-table">
    <thead>
        <tr>
            <th>Задача / День</th>
"""

# Заголовки дней
for day in data.columns:
    html_table += f'<th>{day}</th>'
html_table += "</tr></thead><tbody>"

# Тело таблицы
for task_idx, task_name in enumerate(data.index):
    html_table += f'<tr><td style="font-weight: bold; text-align: left;">{task_name}</td>'
    
    for day_idx, day in enumerate(data.columns):
        value = data.loc[task_name, day]
        cell_id = f"{task_idx}_{day_idx}"
        
        html_table += f"""
        <td>
            <div class="cell-controls">
                <button class="hour-btn minus" onclick="updateHour('{cell_id}', -1)">-</button>
                <span class="hour-value" id="val_{cell_id}">{value}</span>
                <button class="hour-btn plus" onclick="updateHour('{cell_id}', 1)">+</button>
            </div>
            <div style="font-size: 11px; color: #666; margin-top: 3px;">
                <button onclick="setHour('{cell_id}', 4)" style="padding: 1px 3px; font-size: 10px;">4h</button>
                <button onclick="setHour('{cell_id}', 8)" style="padding: 1px 3px; font-size: 10px;">8h</button>
            </div>
        </td>
        """
    
    html_table += '</tr>'

html_table += """
</tbody>
</table>

<div style="margin-top: 20px; padding: 10px; background: #f0f8ff; border-radius: 5px;">
    <strong>Итого часов:</strong>
    <span id="total-hours">0</span> ч.
</div>

<script>
// Обновляем общее количество часов
function updateTotal() {
    let total = 0;
    document.querySelectorAll('.hour-value').forEach(el => {
        total += parseInt(el.innerText);
    });
    document.getElementById('total-hours').innerText = total;
}

// Функции для изменения часов
function updateHour(cellId, delta) {
    const elem = document.getElementById('val_' + cellId);
    const current = parseInt(elem.innerText);
    const newValue = Math.max(0, current + delta);
    elem.innerText = newValue;
    updateTotal();
    
    // Отправляем в Streamlit
    window.parent.postMessage({
        type: 'streamlit:setComponentValue',
        value: cellId + ':' + newValue
    }, '*');
}

function setHour(cellId, value) {
    const elem = document.getElementById('val_' + cellId);
    elem.innerText = value;
    updateTotal();
    
    window.parent.postMessage({
        type: 'streamlit:setComponentValue',
        value: cellId + ':' + value + ':set'
    }, '*');
}

// Инициализация
updateTotal();
</script>
"""

# Отображаем таблицу
st.components.v1.html(html_table, height=500)

# Получаем обновленные значения
cell_update = st.text_input("", key="cell_update", label_visibility="collapsed")
if cell_update:
    # Можно обработать обновления значений
    st.write(f"Обновлена ячейка: {cell_update}")

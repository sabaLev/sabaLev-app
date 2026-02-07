import streamlit as st
import pandas as pd
import numpy as np

st.title("📊 Таблица с интерактивными ячейками")

# Инициализация
if 'data' not in st.session_state:
    st.session_state.data = pd.DataFrame({
        'ID': [1, 2, 3, 4],
        'Наименование': ['Проект A', 'Проект B', 'Проект C', 'Проект D'],
        'Бюджет': [50000, 75000, 30000, 90000],
        'Прогресс': [65, 40, 85, 25],  # проценты
        'Управление': ['🔽⏺️🔼'] * 4
    })

# Создаем кастомные ячейки с кнопками
def create_progress_cell(value, row_idx):
    """Создает ячейку с прогресс-баром и кнопками"""
    button_html = f"""
    <div style="display: flex; align-items: center; gap: 8px; width: 100%;">
        <button onclick="adjustProgress({row_idx}, -10)"
                style="width: 25px; height: 25px; border-radius: 4px; border: 1px solid #ddd; background: white; cursor: pointer;">
            -10
        </button>
        
        <div style="flex-grow: 1; background: #e0e0e0; border-radius: 10px; height: 20px; overflow: hidden;">
            <div style="width: {value}%; background: {'#4CAF50' if value > 70 else '#FFC107' if value > 40 else '#F44336'}; 
                 height: 100%; border-radius: 10px; transition: width 0.3s;">
            </div>
        </div>
        
        <span style="min-width: 35px; text-align: center; font-weight: bold;">{value}%</span>
        
        <button onclick="adjustProgress({row_idx}, 10)"
                style="width: 25px; height: 25px; border-radius: 4px; border: 1px solid #ddd; background: white; cursor: pointer;">
            +10
        </button>
    </div>
    """
    return button_html

# Генерация HTML для всей таблицы
html_content = """
<style>
.progress-table {
    width: 100%;
    border-collapse: collapse;
    margin: 20px 0;
}

.progress-table th {
    background: #f5f5f5;
    padding: 12px 15px;
    text-align: left;
    border-bottom: 2px solid #ddd;
    font-weight: 600;
}

.progress-table td {
    padding: 12px 15px;
    border-bottom: 1px solid #eee;
    vertical-align: middle;
}

.progress-cell {
    min-width: 200px;
}

.small-btn {
    padding: 4px 8px;
    font-size: 12px;
    border: 1px solid #ccc;
    border-radius: 3px;
    background: white;
    cursor: pointer;
    transition: all 0.2s;
}

.small-btn:hover {
    background: #f0f0f0;
}

.small-btn:active {
    transform: scale(0.95);
}
</style>

<table class="progress-table">
    <thead>
        <tr>
            <th>ID</th>
            <th>Наименование</th>
            <th>Бюджет (₽)</th>
            <th>Прогресс</th>
            <th>Действия</th>
        </tr>
    </thead>
    <tbody>
"""

# Заполняем таблицу
for idx, row in st.session_state.data.iterrows():
    budget = f"{row['Бюджет']:,.0f}".replace(',', ' ')
    
    html_content += f"""
    <tr>
        <td>{row['ID']}</td>
        <td><strong>{row['Наименование']}</strong></td>
        <td>{budget} ₽</td>
        <td class="progress-cell">
            <div style="display: flex; align-items: center; gap: 10px;">
                <button class="small-btn" onclick="changeProgress({idx}, -5)">-5%</button>
                
                <div style="flex-grow: 1; position: relative; height: 24px;">
                    <div style="width: 100%; height: 100%; background: #e0e0e0; border-radius: 12px; overflow: hidden;">
                        <div style="width: {row['Прогресс']}%; height: 100%; 
                             background: {'#4CAF50' if row['Прогресс'] > 70 else '#FFC107' if row['Прогресс'] > 40 else '#F44336'};">
                        </div>
                    </div>
                    <div style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; 
                         display: flex; align-items: center; justify-content: center; font-weight: bold; font-size: 12px;">
                        {row['Прогресс']}%
                    </div>
                </div>
                
                <button class="small-btn" onclick="changeProgress({idx}, 5)">+5%</button>
            </div>
        </td>
        <td>
            <div style="display: flex; gap: 5px;">
                <button class="small-btn" onclick="resetProgress({idx})" style="background: #ffebee; color: #c62828;">
                    Сброс
                </button>
                <button class="small-btn" onclick="completeProgress({idx})" style="background: #e8f5e8; color: #2e7d32;">
                    ✅
                </button>
            </div>
        </td>
    </tr>
    """

html_content += """
    </tbody>
</table>

<script>
function changeProgress(rowIndex, delta) {
    window.parent.postMessage({
        type: 'streamlit:setComponentValue',
        value: JSON.stringify({
            action: 'change_progress',
            rowIndex: rowIndex,
            delta: delta
        })
    }, '*');
}

function resetProgress(rowIndex) {
    window.parent.postMessage({
        type: 'streamlit:setComponentValue',
        value: JSON.stringify({
            action: 'reset_progress',
            rowIndex: rowIndex
        })
    }, '*');
}

function completeProgress(rowIndex) {
    window.parent.postMessage({
        type: 'streamlit:setComponentValue',
        value: JSON.stringify({
            action: 'complete_progress',
            rowIndex: rowIndex
        })
    }, '*');
}
</script>
"""

# Отображаем таблицу
st.components.v1.html(html_content, height=400)

# Обработка действий
action_input = st.text_input("", key="table_action", label_visibility="collapsed")
if action_input:
    import json
    try:
        action_data = json.loads(action_input)
        row_idx = action_data['rowIndex']
        
        if action_data['action'] == 'change_progress':
            delta = action_data['delta']
            new_value = st.session_state.data.at[row_idx, 'Прогресс'] + delta
            st.session_state.data.at[row_idx, 'Прогресс'] = max(0, min(100, new_value))
            
        elif action_data['action'] == 'reset_progress':
            st.session_state.data.at[row_idx, 'Прогресс'] = 0
            
        elif action_data['action'] == 'complete_progress':
            st.session_state.data.at[row_idx, 'Прогресс'] = 100
            
        st.rerun()
    except:
        pass

# Статистика
st.write("### 📈 Статистика")
col1, col2, col3 = st.columns(3)
with col1:
    avg_progress = st.session_state.data['Прогресс'].mean()
    st.metric("Средний прогресс", f"{avg_progress:.1f}%")
with col2:
    completed = (st.session_state.data['Прогресс'] >= 100).sum()
    st.metric("Завершено", f"{completed}/{len(st.session_state.data)}")
with col3:
    total_budget = st.session_state.data['Бюджет'].sum()
    st.metric("Общий бюджет", f"{total_budget:,.0f} ₽")

import streamlit as st
import streamlit.components.v1 as components
import json

# Инициализация состояния
if 'table_data' not in st.session_state:
    st.session_state.table_data = [
        {'id': 1, 'checked': True, 'value': 0, 'label': 'מהדק הארקה'},
        {'id': 2, 'checked': True, 'value': 0, 'label': 'מהדק אמצע'},
        {'id': 3, 'checked': False, 'value': 5, 'label': 'בורג איסכורית'},
    ]

st.title("📱 Рабочая таблица (HTML+JS)")

# HTML/JS компонент
table_html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        
        .table {{ 
            width: 100%; 
            font-family: -apple-system, BlinkMacSystemFont, sans-serif;
            direction: rtl;
        }}
        
        .header {{
            display: flex;
            font-weight: bold;
            padding: 12px 10px;
            border-bottom: 2px solid #2E7D32;
            background: #f8f9fa;
            font-size: 16px;
        }}
        
        .row {{
            display: flex;
            align-items: center;
            padding: 15px 10px;
            border-bottom: 1px solid #e0e0e0;
            min-height: 65px;
        }}
        
        .col-check {{ 
            width: 50px; 
            flex: 0 0 50px;
            display: flex;
            justify-content: center;
        }}
        
        .col-label {{ 
            flex: 1;
            padding: 0 15px;
            font-size: 17px;
            text-align: right;
        }}
        
        .col-input {{ 
            width: 130px; 
            flex: 0 0 130px;
        }}
        
        /* Чекбокс */
        .checkbox {{
            width: 28px;
            height: 28px;
            border: 2px solid #4CAF50;
            border-radius: 6px;
            display: flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
            background: white;
            transition: all 0.2s;
        }}
        
        .checkbox.checked {{
            background: #4CAF50;
        }}
        
        .checkmark {{
            color: white;
            font-size: 18px;
            font-weight: bold;
            display: none;
        }}
        
        .checkbox.checked .checkmark {{
            display: block;
        }}
        
        /* Поле ввода */
        .number-input {{
            display: flex;
            align-items: center;
            border: 2px solid #2196F3;
            border-radius: 8px;
            overflow: hidden;
            background: white;
            height: 48px;
        }}
        
        .btn {{
            width: 45px;
            height: 100%;
            background: #2196F3;
            color: white;
            border: none;
            font-size: 24px;
            font-weight: bold;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
        }}
        
        .btn:hover {{ background: #1976D2; }}
        
        .btn-minus {{ border-right: 1px solid #1976D2; }}
        .btn-plus {{ border-left: 1px solid #1976D2; }}
        
        .value {{
            flex: 1;
            text-align: center;
            font-size: 18px;
            font-weight: bold;
            padding: 0 5px;
            min-width: 40px;
        }}
        
        /* Для iPhone */
        @media (max-width: 768px) {{
            .row {{ padding: 12px 8px; min-height: 58px; }}
            .col-input {{ width: 120px; flex: 0 0 120px; }}
            .btn {{ width: 42px; font-size: 22px; }}
            .value {{ font-size: 17px; }}
            .col-label {{ font-size: 16px; padding: 0 12px; }}
        }}
    </style>
</head>
<body>
    <div class="table">
        <div class="header">
            <div class="col-check">✓</div>
            <div class="col-label">שם פריט</div>
            <div class="col-input">כמות</div>
        </div>
        
        <div id="table-body">
            <!-- Строки будут здесь -->
        </div>
    </div>

    <script>
        // Данные из Python
        const tableData = {json.dumps(st.session_state.table_data)};
        
        // Создаем строки таблицы
        function createRow(item) {{
            return `
            <div class="row" data-id="${{item.id}}">
                <div class="col-check">
                    <div class="checkbox ${{item.checked ? 'checked' : ''}}" onclick="toggleCheckbox(${{item.id}})">
                        <div class="checkmark">✓</div>
                    </div>
                </div>
                <div class="col-label">${{item.label}}</div>
                <div class="col-input">
                    <div class="number-input">
                        <button class="btn btn-minus" onclick="changeValue(${{item.id}}, -1)">−</button>
                        <div class="value">${{item.value}}</div>
                        <button class="btn btn-plus" onclick="changeValue(${{item.id}}, 1)">+</button>
                    </div>
                </div>
            </div>
            `;
        }}
        
        // Заполняем таблицу
        document.getElementById('table-body').innerHTML = 
            tableData.map(item => createRow(item)).join('');
        
        // Функции для взаимодействия
        function toggleCheckbox(id) {{
            const checkbox = document.querySelector(`.row[data-id="${{id}}"] .checkbox`);
            checkbox.classList.toggle('checked');
            
            // Отправляем данные в Streamlit
            window.parent.postMessage({{
                type: 'TOGGLE_CHECKBOX',
                id: id,
                checked: checkbox.classList.contains('checked')
            }}, '*');
        }}
        
        function changeValue(id, delta) {{
            const valueEl = document.querySelector(`.row[data-id="${{id}}"] .value`);
            let value = parseInt(valueEl.textContent) + delta;
            if (value < 0) value = 0;
            valueEl.textContent = value;
            
            // Отправляем данные в Streamlit
            window.parent.postMessage({{
                type: 'CHANGE_VALUE',
                id: id,
                value: value
            }}, '*');
        }}
        
        // Получаем сообщения от Streamlit (если нужно обновить)
        window.addEventListener('message', (event) => {{
            if (event.data.type === 'UPDATE_DATA') {{
                document.getElementById('table-body').innerHTML = 
                    event.data.tableData.map(item => createRow(item)).join('');
            }}
        }});
    </script>
</body>
</html>
"""

# Отображаем компонент
component_value = components.html(table_html, height=400, scrolling=False)

# Обрабатываем взаимодействие с таблицей
if component_value:
    if isinstance(component_value, dict):
        if component_value.get('type') == 'TOGGLE_CHECKBOX':
            item_id = component_value['id']
            for item in st.session_state.table_data:
                if item['id'] == item_id:
                    item['checked'] = component_value['checked']
                    break
        elif component_value.get('type') == 'CHANGE_VALUE':
            item_id = component_value['id']
            for item in st.session_state.table_data:
                if item['id'] == item_id:
                    item['value'] = component_value['value']
                    break
        
        st.rerun()

# Показываем текущие данные
st.markdown("---")
st.write("**Текущее состояние таблицы:**")
st.json(st.session_state.table_data)

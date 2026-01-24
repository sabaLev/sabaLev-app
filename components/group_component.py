import streamlit.components.v1 as components

def create_groups_component(standing_rows=8, laying_rows=4, key="groups"):
    """Создает компоненту для ввода групп"""
    
    html = f'''
    <!DOCTYPE html>
    <html dir="rtl">
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            * {{
                box-sizing: border-box;
                margin: 0;
                padding: 0;
                font-family: -apple-system, BlinkMacSystemFont, sans-serif;
            }}
            
            .section {{
                background: #F0F2F6;
                border-radius: 10px;
                padding: 15px;
                margin: 20px 0;
                border: 1px solid #DCDCDC;
            }}
            
            .section-title {{
                font-size: 16px;
                font-weight: 600;
                color: #31333F;
                margin-bottom: 15px;
                text-align: center;
            }}
            
            .columns-header {{
                display: flex;
                width: 100%;
                margin-bottom: 10px;
                font-size: 14px;
                font-weight: 500;
                color: #31333F;
            }}
            
            .column-label {{
                flex: 1;
                text-align: center;
                padding: 0 5px;
            }}
            
            .row {{
                display: flex;
                width: 100%;
                gap: 10px;
                margin-bottom: 10px;
            }}
            
            .input-column {{
                flex: 1;
            }}
            
            .input-group {{
                display: flex;
                background: white;
                border-radius: 8px;
                border: 1px solid #DCDCDC;
                overflow: hidden;
                height: 42px;
            }}
            
            .input-group:focus-within {{
                border-color: #4b75c9;
                box-shadow: 0 0 0 1px #4b75c9;
            }}
            
            .btn {{
                width: 40px;
                background: #F0F2F6;
                border: none;
                color: #31333F;
                font-size: 20px;
                font-weight: 300;
                cursor: pointer;
                display: flex;
                align-items: center;
                justify-content: center;
                transition: all 0.15s;
            }}
            
            .btn:hover {{
                background: #EC5953 !important;
                color: white !important;
            }}
            
            .input {{
                flex: 1;
                border: none;
                text-align: center;
                font-size: 16px;
                font-weight: 500;
                color: #31333F;
                padding: 0;
                outline: none;
                min-width: 0;
            }}
            
            input::-webkit-outer-spin-button,
            input::-webkit-inner-spin-button {{
                -webkit-appearance: none;
                margin: 0;
            }}
            
            input[type=number] {{
                -moz-appearance: textfield;
                appearance: textfield;
            }}
            
            .add-btn {{
                background: #4b75c9;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 8px 16px;
                font-size: 14px;
                font-weight: 500;
                cursor: pointer;
                margin-top: 10px;
                display: block;
                margin-left: auto;
                margin-right: auto;
                transition: background 0.2s;
            }}
            
            .add-btn:hover {{
                background: #3a62b5;
            }}
            
            /* Для мобильных */
            @media (max-width: 768px) {{
                .row {{
                    gap: 8px;
                }}
                
                .input-group {{
                    height: 38px;
                }}
                
                .btn {{
                    width: 36px;
                    font-size: 18px;
                }}
                
                .input {{
                    font-size: 15px;
                }}
            }}
            
            @media (max-width: 480px) {{
                .row {{
                    gap: 6px;
                }}
                
                .input-group {{
                    height: 36px;
                }}
                
                .btn {{
                    width: 34px;
                    font-size: 16px;
                }}
                
                .input {{
                    font-size: 14px;
                }}
            }}
            
            /* Темная тема */
            @media (prefers-color-scheme: dark) {{
                .section {{
                    background: #1E293B;
                    border-color: #2D3748;
                }}
                
                .input-group {{
                    background: #1E293B;
                    border-color: #2D3748;
                }}
                
                .input {{
                    color: #FAFAFA;
                    background: #1E293B;
                }}
                
                .btn {{
                    background: #1E293B;
                    color: #FAFAFA;
                }}
            }}
        </style>
    </head>
    <body>
        <!-- СТОЯЧИЕ -->
        <div class="section">
            <div class="section-title">עומד</div>
            <div class="columns-header">
                <div class="column-label">פאנלים</div>
                <div class="column-label">שורות</div>
            </div>
            <div id="standing-rows">
                <!-- Строки будут добавлены через JS -->
            </div>
            <button class="add-btn" onclick="addRow('standing')">עוד שורה</button>
        </div>
        
        <!-- ЛЕЖАЧИЕ -->
        <div class="section">
            <div class="section-title">שוכב</div>
            <div class="columns-header">
                <div class="column-label">פאנלים</div>
                <div class="column-label">שורות</div>
            </div>
            <div id="laying-rows">
                <!-- Строки будут добавлены через JS -->
            </div>
            <button class="add-btn" onclick="addRow('laying')">עוד שורה</button>
        </div>
        
        <!-- Скрытый input для передачи данных в Streamlit -->
        <input type="hidden" id="streamlit-data" name="streamlit_data">
        
        <script>
        // Данные
        let standingRows = {standing_rows};
        let layingRows = {laying_rows};
        let data = {{
            standing: {{}},
            laying: {{}}
        }};
        
        // Инициализация
        function init() {{
            // Стоячие: 1-8 פאנלים, 0 שורות
            for (let i = 1; i <= standingRows; i++) {{
                data.standing[`n_${{i}}`] = i;
                data.standing[`g_${{i}}`] = 0;
            }}
            
            // Лежачие: 1-4 פאנלים, 0 שורות
            for (let i = 1; i <= layingRows; i++) {{
                data.laying[`n_${{i}}`] = i <= 4 ? i : 0;
                data.laying[`g_${{i}}`] = 0;
            }}
            
            renderAll();
        }}
        
        // Создание строки
        function createRow(type, index) {{
            const nValue = data[type][`n_${{index}}`] || 0;
            const gValue = data[type][`g_${{index}}`] || 0;
            
            return `
                <div class="row">
                    <div class="input-column">
                        <div class="input-group">
                            <button class="btn" type="button" onclick="adjustValue('${{type}}', 'n', ${{index}}, -1)">−</button>
                            <input type="number" class="input" id="${{type}}_n_${{index}}" 
                                   value="${{nValue}}" min="0" max="99" 
                                   oninput="updateValue('${{type}}', 'n', ${{index}}, this.value)">
                            <button class="btn" type="button" onclick="adjustValue('${{type}}', 'n', ${{index}}, 1)">+</button>
                        </div>
                    </div>
                    <div class="input-column">
                        <div class="input-group">
                            <button class="btn" type="button" onclick="adjustValue('${{type}}', 'g', ${{index}}, -1)">−</button>
                            <input type="number" class="input" id="${{type}}_g_${{index}}" 
                                   value="${{gValue}}" min="0" max="99" 
                                   oninput="updateValue('${{type}}', 'g', ${{index}}, this.value)">
                            <button class="btn" type="button" onclick="adjustValue('${{type}}', 'g', ${{index}}, 1)">+</button>
                        </div>
                    </div>
                </div>
            `;
        }}
        
        // Отрисовка всех строк
        function renderAll() {{
            let standingHtml = '';
            for (let i = 1; i <= standingRows; i++) {{
                standingHtml += createRow('standing', i);
            }}
            document.getElementById('standing-rows').innerHTML = standingHtml;
            
            let layingHtml = '';
            for (let i = 1; i <= layingRows; i++) {{
                layingHtml += createRow('laying', i);
            }}
            document.getElementById('laying-rows').innerHTML = layingHtml;
            
            // Сохраняем данные
            saveData();
        }}
        
        // Сохранение и отправка данных
        function saveData() {{
            // Преобразуем в формат для расчета
            const groupsForCalculation = [];
            
            // Стоячие
            for (let i = 1; i <= standingRows; i++) {{
                const n = data.standing[`n_${{i}}`] || 0;
                const g = data.standing[`g_${{i}}`] || 0;
                if (n > 0 && g > 0) {{
                    groupsForCalculation.push([n, g, 'עומד']);
                }}
            }}
            
            // Лежачие
            for (let i = 1; i <= layingRows; i++) {{
                const n = data.laying[`n_${{i}}`] || 0;
                const g = data.laying[`g_${{i}}`] || 0;
                if (n > 0 && g > 0) {{
                    groupsForCalculation.push([n, g, 'שוכב']);
                }}
            }}
            
            // Сохраняем в скрытом поле
            const hiddenInput = document.getElementById('streamlit-data');
            if (hiddenInput) {{
                hiddenInput.value = JSON.stringify(groupsForCalculation);
                
                // Триггерим событие input чтобы Streamlit увидел изменение
                const event = new Event('input', {{ bubbles: true }});
                hiddenInput.dispatchEvent(event);
            }}
            
            // Также сохраняем в глобальной переменной для доступа через JS
            window.solarGroupsData = groupsForCalculation;
            
            return groupsForCalculation;
        }}
        
        // Изменение значения кнопками
        function adjustValue(type, field, index, delta) {{
            const key = `${{field}}_${{index}}`;
            let value = parseInt(data[type][key]) || 0;
            value += delta;
            
            if (value < 0) value = 0;
            if (value > 99) value = 99;
            
            data[type][key] = value;
            
            // Обновляем поле ввода
            const input = document.getElementById(`${{type}}_${{field}}_${{index}}`);
            if (input) input.value = value;
            
            saveData();
        }}
        
        // Обновление ручного ввода
        function updateValue(type, field, index, value) {{
            const key = `${{field}}_${{index}}`;
            const numValue = parseInt(value) || 0;
            
            let finalValue = numValue;
            if (numValue < 0) finalValue = 0;
            if (numValue > 99) finalValue = 99;
            
            data[type][key] = finalValue;
            
            // Корректируем значение в поле если нужно
            if (numValue !== finalValue) {{
                const input = document.getElementById(`${{type}}_${{field}}_${{index}}`);
                if (input) input.value = finalValue;
            }}
            
            saveData();
        }}
        
        // Добавление строки
        function addRow(type) {{
            if (type === 'standing') {{
                standingRows++;
                data.standing[`n_${{standingRows}}`] = 0;
                data.standing[`g_${{standingRows}}`] = 0;
            }} else {{
                layingRows++;
                data.laying[`n_${{layingRows}}`] = 0;
                data.laying[`g_${{layingRows}}`] = 0;
            }}
            
            renderAll();
        }}
        
        // Функция для получения данных извне
        function getGroupsData() {{
            return saveData();
        }}
        
        // Инициализация при загрузке
        document.addEventListener('DOMContentLoaded', init);
        </script>
    </body>
    </html>
    '''
    
    # Отображаем компоненту
    component = components.html(html, height=600)
    
    return component

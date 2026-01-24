import streamlit.components.v1 as components
import json

def dual_column_inputs(standing_rows=8, laying_rows=4, key="groups"):
    """Кастомная компонента с двумя колонками"""
    
    # HTML/JS компонента
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
            
            .container {{
                width: 100%;
                max-width: 800px;
                margin: 0 auto;
                padding: 0 10px;
            }}
            
            .section {{
                margin-bottom: 30px;
                background: #F0F2F6;
                border-radius: 10px;
                padding: 15px;
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
            
            .input-row {{
                display: flex;
                width: 100%;
                gap: 10px;
                margin-bottom: 10px;
                align-items: center;
            }}
            
            .input-column {{
                flex: 1;
            }}
            
            .stepper {{
                display: flex;
                background: white;
                border-radius: 8px;
                border: 1px solid #DCDCDC;
                overflow: hidden;
                height: 42px;
            }}
            
            .stepper-button {{
                width: 40px;
                height: 100%;
                background: #F0F2F6;
                border: none;
                color: #31333F;
                font-size: 20px;
                font-weight: 300;
                cursor: pointer;
                display: flex;
                align-items: center;
                justify-content: center;
                transition: background 0.2s;
            }}
            
            .stepper-button:hover {{
                background: #EC5953;
                color: white;
            }}
            
            .stepper-input {{
                flex: 1;
                border: none;
                text-align: center;
                font-size: 16px;
                font-weight: 500;
                color: #31333F;
                padding: 0 10px;
                outline: none;
                min-width: 0;
            }}
            
            .add-button {{
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
            }}
            
            .add-button:hover {{
                background: #3a62b5;
            }}
            
            /* Для мобильных */
            @media (max-width: 768px) {{
                .input-row {{
                    gap: 8px;
                }}
                
                .stepper {{
                    height: 38px;
                }}
                
                .stepper-button {{
                    width: 36px;
                    font-size: 18px;
                }}
                
                .stepper-input {{
                    font-size: 15px;
                    padding: 0 8px;
                }}
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <!-- СТОЯЧИЕ ПАНЕЛИ -->
            <div class="section">
                <div class="section-title">עומד</div>
                <div class="columns-header">
                    <div class="column-label">פאנלים</div>
                    <div class="column-label">שורות</div>
                </div>
                <div id="standing-rows"></div>
                <button class="add-button" onclick="addRow('standing')">עוד שורה</button>
            </div>
            
            <!-- ЛЕЖАЧИЕ ПАНЕЛИ -->
            <div class="section">
                <div class="section-title">שוכב</div>
                <div class="columns-header">
                    <div class="column-label">פאנלים</div>
                    <div class="column-label">שורות</div>
                </div>
                <div id="laying-rows"></div>
                <button class="add-button" onclick="addRow('laying')">עוד שורה</button>
            </div>
        </div>
        
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
                sendDataToStreamlit();
            }}
            
            // Создание строки
            function createRow(type, index) {{
                const nValue = data[type][`n_${{index}}`] || 0;
                const gValue = data[type][`g_${{index}}`] || 0;
                
                return `
                    <div class="input-row">
                        <div class="input-column">
                            <div class="stepper">
                                <button class="stepper-button" onclick="adjustValue('${{type}}', 'n', ${{index}}, -1)">−</button>
                                <input type="number" class="stepper-input" value="${{nValue}}" 
                                       min="0" max="99" 
                                       oninput="updateValue('${{type}}', 'n', ${{index}}, this.value)">
                                <button class="stepper-button" onclick="adjustValue('${{type}}', 'n', ${{index}}, 1)">+</button>
                            </div>
                        </div>
                        <div class="input-column">
                            <div class="stepper">
                                <button class="stepper-button" onclick="adjustValue('${{type}}', 'g', ${{index}}, -1)">−</button>
                                <input type="number" class="stepper-input" value="${{gValue}}" 
                                       min="0" max="99" 
                                       oninput="updateValue('${{type}}', 'g', ${{index}}, this.value)">
                                <button class="stepper-button" onclick="adjustValue('${{type}}', 'g', ${{index}}, 1)">+</button>
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
            }}
            
            // Изменение значения
            function adjustValue(type, field, index, delta) {{
                const key = `${{field}}_${{index}}`;
                let value = parseInt(data[type][key]) || 0;
                value += delta;
                
                if (value < 0) value = 0;
                if (value > 99) value = 99;
                
                data[type][key] = value;
                
                // Обновляем отображение
                const inputs = document.querySelectorAll(`#${{type}}-rows input`);
                // Найдем нужный input и обновим
                renderAll(); // Простая перерисовка
                sendDataToStreamlit();
            }}
            
            // Обновление ручного ввода
            function updateValue(type, field, index, value) {{
                const key = `${{field}}_${{index}}`;
                const numValue = parseInt(value) || 0;
                
                if (numValue < 0) {{
                    data[type][key] = 0;
                }} else if (numValue > 99) {{
                    data[type][key] = 99;
                }} else {{
                    data[type][key] = numValue;
                }}
                
                sendDataToStreamlit();
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
                sendDataToStreamlit();
            }}
            
            // Отправка данных в Streamlit
            function sendDataToStreamlit() {{
                // Преобразуем данные в массив для расчета
                const groups = {{
                    standing: [],
                    laying: []
                }};
                
                // Стоячие
                for (let i = 1; i <= standingRows; i++) {{
                    const n = data.standing[`n_${{i}}`] || 0;
                    const g = data.standing[`g_${{i}}`] || 0;
                    if (n > 0 && g > 0) {{
                        groups.standing.push({{n: n, g: g, type: 'עומד'}});
                    }}
                }}
                
                // Лежачие
                for (let i = 1; i <= layingRows; i++) {{
                    const n = data.laying[`n_${{i}}`] || 0;
                    const g = data.laying[`g_${{i}}`] || 0;
                    if (n > 0 && g > 0) {{
                        groups.laying.push({{n: n, g: g, type: 'שוכב'}});
                    }}
                }}
                
                // Отправляем
                window.parent.postMessage({{
                    type: 'solar_groups_data',
                    data: groups,
                    raw: data
                }}, '*');
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

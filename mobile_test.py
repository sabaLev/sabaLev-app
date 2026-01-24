import streamlit as st
import streamlit.components.v1 as components

st.title("🧪 Тест только компоненты")

# Ваша компонента (скопируйте HTML код из моего предыдущего сообщения)
html_code = '''
<!DOCTYPE html>
<html dir="rtl">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            font-family: -apple-system, BlinkMacSystemFont, sans-serif;
        }
        
        .container {
            width: 100%;
            max-width: 800px;
            margin: 0 auto;
            padding: 0 10px;
        }
        
        .section {
            margin-bottom: 30px;
            background: #F0F2F6;
            border-radius: 10px;
            padding: 15px;
            border: 1px solid #DCDCDC;
        }
        
        .section-title {
            font-size: 16px;
            font-weight: 600;
            color: #31333F;
            margin-bottom: 15px;
            text-align: center;
        }
        
        .columns-header {
            display: flex;
            width: 100%;
            margin-bottom: 10px;
            font-size: 14px;
            font-weight: 500;
            color: #31333F;
        }
        
        .column-label {
            flex: 1;
            text-align: center;
            padding: 0 5px;
        }
        
        .input-row {
            display: flex;
            width: 100%;
            gap: 10px;
            margin-bottom: 10px;
            align-items: center;
        }
        
        .input-column {
            flex: 1;
        }
        
        .stepper {
            display: flex;
            background: white;
            border-radius: 8px;
            border: 1px solid #DCDCDC;
            overflow: hidden;
            height: 42px;
        }
        
        .stepper-button {
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
        }
        
        .stepper-button:hover {
            background: #EC5953;
            color: white;
        }
        
        .stepper-input {
            flex: 1;
            border: none;
            text-align: center;
            font-size: 16px;
            font-weight: 500;
            color: #31333F;
            padding: 0 10px;
            outline: none;
            min-width: 0;
        }
        
        .add-button {
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
        }
        
        .add-button:hover {
            background: #3a62b5;
        }
        
        /* Для мобильных */
        @media (max-width: 768px) {
            .input-row {
                gap: 8px;
            }
            
            .stepper {
                height: 38px;
            }
            
            .stepper-button {
                width: 36px;
                font-size: 18px;
            }
            
            .stepper-input {
                font-size: 15px;
                padding: 0 8px;
            }
        }
        
        .debug-box {
            background: #f0f9ff;
            border: 2px solid #bae6fd;
            border-radius: 8px;
            padding: 15px;
            margin: 20px 0;
            font-family: monospace;
            font-size: 14px;
            max-height: 200px;
            overflow-y: auto;
        }
    </style>
</head>
<body>
    <div class="container">
        <!-- СТОЯЧИЕ ПАНЕЛИ -->
        <div class="section">
            <div class="section-title">עומד (Тест)</div>
            <div class="columns-header">
                <div class="column-label">פאנלים</div>
                <div class="column-label">שורות</div>
            </div>
            <div id="standing-rows"></div>
            <button class="add-button" onclick="addRow('standing')">עוד שורה</button>
        </div>
        
        <!-- ЛЕЖАЧИЕ ПАНЕЛИ -->
        <div class="section">
            <div class="section-title">שוכב (Тест)</div>
            <div class="columns-header">
                <div class="column-label">פאנלים</div>
                <div class="column-label">שורות</div>
            </div>
            <div id="laying-rows"></div>
            <button class="add-button" onclick="addRow('laying')">עוד שורה</button>
        </div>
        
        <!-- ДЕБАГ ИНФОРМАЦИЯ -->
        <div class="debug-box">
            <div id="debug-info">Нажмите кнопки +/- для теста...</div>
        </div>
        
        <button class="add-button" onclick="showDebugInfo()" style="background: #10b981;">Показать данные</button>
    </div>
    
    <script>
        // Данные
        let standingRows = 4;  // Только 4 для теста
        let layingRows = 2;    // Только 2 для теста
        let data = {
            standing: {},
            laying: {}
        };
        
        // Инициализация
        function init() {
            // Стоячие: 1-4 פאנלים, 0 שורות
            for (let i = 1; i <= standingRows; i++) {
                data.standing[`n_${i}`] = i;
                data.standing[`g_${i}`] = 0;
            }
            
            // Лежачие: 1-2 פאנלים, 0 שורות
            for (let i = 1; i <= layingRows; i++) {
                data.laying[`n_${i}`] = i <= 2 ? i : 0;
                data.laying[`g_${i}`] = 0;
            }
            
            renderAll();
            updateDebugInfo();
        }
        
        // Создание строки
        function createRow(type, index) {
            const nValue = data[type][`n_${index}`] || 0;
            const gValue = data[type][`g_${index}`] || 0;
            
            return `
                <div class="input-row">
                    <div class="input-column">
                        <div class="stepper">
                            <button class="stepper-button" onclick="adjustValue('${type}', 'n', ${index}, -1)">−</button>
                            <input type="number" class="stepper-input" value="${nValue}" 
                                   min="0" max="99" 
                                   oninput="updateValue('${type}', 'n', ${index}, this.value)">
                            <button class="stepper-button" onclick="adjustValue('${type}', 'n', ${index}, 1)">+</button>
                        </div>
                    </div>
                    <div class="input-column">
                        <div class="stepper">
                            <button class="stepper-button" onclick="adjustValue('${type}', 'g', ${index}, -1)">−</button>
                            <input type="number" class="stepper-input" value="${gValue}" 
                                   min="0" max="99" 
                                   oninput="updateValue('${type}', 'g', ${index}, this.value)">
                            <button class="stepper-button" onclick="adjustValue('${type}', 'g', ${index}, 1)">+</button>
                        </div>
                    </div>
                </div>
            `;
        }
        
        // Отрисовка всех строк
        function renderAll() {
            let standingHtml = '';
            for (let i = 1; i <= standingRows; i++) {
                standingHtml += createRow('standing', i);
            }
            document.getElementById('standing-rows').innerHTML = standingHtml;
            
            let layingHtml = '';
            for (let i = 1; i <= layingRows; i++) {
                layingHtml += createRow('laying', i);
            }
            document.getElementById('laying-rows').innerHTML = layingHtml;
        }
        
        // Изменение значения кнопками
        function adjustValue(type, field, index, delta) {
            const key = `${field}_${index}`;
            let value = parseInt(data[type][key]) || 0;
            value += delta;
            
            if (value < 0) value = 0;
            if (value > 99) value = 99;
            
            data[type][key] = value;
            renderAll(); // Перерисовываем
            updateDebugInfo();
        }
        
        // Обновление ручного ввода
        function updateValue(type, field, index, value) {
            const key = `${field}_${index}`;
            const numValue = parseInt(value) || 0;
            
            if (numValue < 0) {
                data[type][key] = 0;
            } else if (numValue > 99) {
                data[type][key] = 99;
            } else {
                data[type][key] = numValue;
            }
            
            updateDebugInfo();
        }
        
        // Добавление строки
        function addRow(type) {
            if (type === 'standing') {
                standingRows++;
                data.standing[`n_${standingRows}`] = 0;
                data.standing[`g_${standingRows}`] = 0;
            } else {
                layingRows++;
                data.laying[`n_${layingRows}`] = 0;
                data.laying[`g_${layingRows}`] = 0;
            }
            
            renderAll();
            updateDebugInfo();
        }
        
        // Показать данные для дебага
        function showDebugInfo() {
            updateDebugInfo();
            alert('Данные в консоли! Откройте DevTools (F12) → Console');
            console.log('=== ДАННЫЕ КОМПОНЕНТЫ ===', data);
        }
        
        // Обновление дебаг информации
        function updateDebugInfo() {
            const debugDiv = document.getElementById('debug-info');
            if (debugDiv) {
                let html = '<strong>Текущие данные:</strong><br>';
                
                html += '<strong>עומד:</strong><br>';
                for (let i = 1; i <= standingRows; i++) {
                    const n = data.standing[`n_${i}`] || 0;
                    const g = data.standing[`g_${i}`] || 0;
                    html += `Строка ${i}: ${n} פאנלים, ${g} שורות<br>`;
                }
                
                html += '<strong>שוכב:</strong><br>';
                for (let i = 1; i <= layingRows; i++) {
                    const n = data.laying[`n_${i}`] || 0;
                    const g = data.laying[`g_${i}`] || 0;
                    html += `Строка ${i}: ${n} פאנלים, ${g} שורות<br>`;
                }
                
                debugDiv.innerHTML = html;
            }
        }
        
        // Инициализация при загрузке
        document.addEventListener('DOMContentLoaded', init);
    </script>
</body>
</html>
'''

# Отображаем компоненту
components.html(html_code, height=700)

st.markdown("---")
st.write("**Инструкция по тесту:**")
st.write("1. Откройте на телефоне")
st.write("2. Проверьте, что две колонки рядом")
st.write("3. Нажмите кнопки + и - (должны работать)")
st.write("4. Введите число вручную (должно работать)")
st.write("5. Нажмите 'Показать данные' для проверки")
st.write("6. Кнопки 'עוד שורה' добавляют строки")

st.write("**Результат теста:**")
st.write("- Если всё работает — компонента готова")
st.write("- Если что-то не работает — скажите что именно")import streamlit as st
import streamlit.components.v1 as components

# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="Тест групп - исправлено",
    page_icon="📱",
    layout="centered"
)

# ---------- CUSTOM STYLES ----------
st.markdown("""
<style>
    /* ОСНОВНЫЕ СТИЛИ */
    .main {
        padding: 20px;
        max-width: 800px;
        margin: 0 auto;
    }
    
    /* ЗАГОЛОВОК СПОЙЛЕРА */
    .spoiler-header {
        font-size: 18px;
        font-weight: 600;
        color: #31333F;
        margin: 20px 0 15px 0;
        text-align: center;
        padding: 12px;
        background: #F0F2F6;
        border-radius: 8px;
        border: 1px solid #DCDCDC;
    }
    
    /* ЗАГОЛОВКИ КОЛОНОК */
    .columns-header {
        display: flex;
        width: 100%;
        margin-bottom: 10px;
        font-size: 14px;
        font-weight: 500;
        color: #31333F;
        padding: 0 5px;
    }
    
    .column-label {
        flex: 1;
        text-align: center;
        padding: 0 5px;
    }
    
    /* СТРОКА С ДВУМЯ ИНПУТАМИ */
    .input-row {
        display: flex !important;
        width: 100% !important;
        gap: 12px !important;
        margin-bottom: 12px !important;
        align-items: stretch !important;
    }
    
    .input-column {
        flex: 1 !important;
        min-width: 0 !important;
    }
    
    /* ИНПУТ В СТИЛЕ STREAMLIT */
    .streamlit-style-input {
        display: flex;
        width: 100%;
        min-width: 0;
        background: #F0F2F6;
        border-radius: 0.5rem;
        border: 1px solid #DCDCDC;
        overflow: hidden;
        height: 42px;
        transition: all 0.2s;
    }
    
    .streamlit-style-input:focus-within {
        border-color: #4b75c9;
        box-shadow: 0 0 0 1px #4b75c9;
    }
    
    /* ПОЛЕ ВВОДА */
    .number-input {
        flex: 1;
        min-width: 0;
        width: 100%;
        border: none;
        background: transparent;
        font-family: -apple-system, BlinkMacSystemFont, sans-serif;
        font-size: 16px;
        color: #31333F;
        padding: 0 12px;
        height: 100%;
        text-align: center;
        outline: none;
        font-weight: 500;
    }
    
    .number-input::-webkit-inner-spin-button,
    .number-input::-webkit-outer-spin-button {
        -webkit-appearance: none;
        margin: 0;
    }
    
    .number-input {
        -moz-appearance: textfield;
        appearance: textfield;
    }
    
    /* КНОПКИ +/- */
    .button-group {
        display: flex;
        height: 100%;
        border-left: 1px solid rgba(0,0,0,0.1);
    }
    
    .stepper-button {
        width: 40px;
        height: 100%;
        background: #F0F2F6;
        border: none;
        padding: 0;
        cursor: pointer;
        color: #31333F;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 20px;
        font-weight: 300;
        user-select: none;
        transition: all 0.15s;
    }
    
    .stepper-button:hover {
        background: #EC5953 !important;
        color: white !important;
    }
    
    .stepper-button:active {
        background: #D94E48 !important;
    }
    
    /* Граница между кнопками */
    .stepper-button:first-child {
        border-right: 1px solid rgba(0,0,0,0.1);
    }
    
    /* КНОПКА "ЕЩЕ СТРОКА" */
    .add-row-btn {
        background: #4b75c9;
        color: white;
        border: none;
        border-radius: 6px;
        padding: 10px 20px;
        font-size: 14px;
        font-weight: 500;
        cursor: pointer;
        margin-top: 15px;
        transition: background 0.2s;
        display: block;
        width: 140px;
        margin-left: auto;
        margin-right: auto;
    }
    
    .add-row-btn:hover {
        background: #3a62b5;
    }
    
    /* ИНФО БЛОК */
    .info-box {
        background: #f0f9ff;
        border: 1px solid #bae6fd;
        border-radius: 8px;
        padding: 15px;
        margin: 20px 0;
        font-size: 14px;
        color: #0369a1;
    }
    
    /* АДАПТАЦИЯ ДЛЯ МОБИЛЬНЫХ */
    @media (max-width: 768px) {
        .input-row {
            gap: 8px !important;
            margin-bottom: 10px !important;
        }
        
        .streamlit-style-input {
            height: 38px;
        }
        
        .stepper-button {
            width: 36px;
            font-size: 18px;
        }
        
        .number-input {
            font-size: 15px;
            padding: 0 8px;
        }
        
        .add-row-btn {
            width: 130px;
            padding: 9px 18px;
        }
    }
    
    @media (max-width: 480px) {
        .input-row {
            gap: 6px !important;
            margin-bottom: 8px !important;
        }
        
        .streamlit-style-input {
            height: 36px;
        }
        
        .stepper-button {
            width: 34px;
            font-size: 16px;
        }
        
        .number-input {
            font-size: 14px;
            padding: 0 6px;
        }
        
        .add-row-btn {
            width: 120px;
            padding: 8px 16px;
            font-size: 13px;
        }
    }
    
    /* ТЕМНАЯ ТЕМА */
    @media (prefers-color-scheme: dark) {
        .spoiler-header {
            background: #1E293B;
            color: #FAFAFA;
            border-color: #2D3748;
        }
        
        .streamlit-style-input {
            background: #1E293B;
            border-color: #2D3748;
        }
        
        .number-input {
            color: #FAFAFA;
        }
        
        .stepper-button {
            background: #1E293B;
            color: #FAFAFA;
        }
        
        .stepper-button:hover {
            background: #EC5953 !important;
        }
    }
</style>
""", unsafe_allow_html=True)

# ---------- ФУНКЦИЯ ДЛЯ СОЗДАНИЯ СТРОКИ ----------
def create_input_row_html(panel_type, row_num, default_n=0, default_g=0):
    """Возвращает HTML для строки с двумя инпутами"""
    return f'''
    <div class="input-row">
        <div class="input-column">
            <div class="streamlit-style-input">
                <input type="number" 
                       id="{panel_type}_n_{row_num}" 
                       value="{default_n}" 
                       min="0" 
                       max="99" 
                       class="number-input">
                <div class="button-group">
                    <button class="stepper-button" type="button" 
                            onclick="adjustValue('{panel_type}_n_{row_num}', -1)">−</button>
                    <button class="stepper-button" type="button" 
                            onclick="adjustValue('{panel_type}_n_{row_num}', 1)">+</button>
                </div>
            </div>
        </div>
        <div class="input-column">
            <div class="streamlit-style-input">
                <input type="number" 
                       id="{panel_type}_g_{row_num}" 
                       value="{default_g}" 
                       min="0" 
                       max="99" 
                       class="number-input">
                <div class="button-group">
                    <button class="stepper-button" type="button" 
                            onclick="adjustValue('{panel_type}_g_{row_num}', -1)">−</button>
                    <button class="stepper-button" type="button" 
                            onclick="adjustValue('{panel_type}_g_{row_num}', 1)">+</button>
                </div>
            </div>
        </div>
    </div>
    '''

# ---------- JAVASCRIPT ----------
javascript_code = '''
<script>
// Корректировка значения кнопками +/-
function adjustValue(inputId, change) {
    const input = document.getElementById(inputId);
    let value = parseInt(input.value) || 0;
    value += change;
    
    if (value < 0) value = 0;
    if (value > 99) value = 99;
    
    input.value = value;
    console.log(inputId + " = " + value);
}

// Валидация ручного ввода
document.addEventListener('DOMContentLoaded', function() {
    const inputs = document.querySelectorAll('.number-input');
    inputs.forEach(input => {
        input.addEventListener('input', function() {
            let value = parseInt(this.value) || 0;
            if (value < 0) this.value = 0;
            if (value > 99) this.value = 99;
        });
    });
});

// Получить все значения для отладки
function getAllValues() {
    const values = {standing: [], laying: []};
    
    // Стоячие
    for (let i = 1; i <= 20; i++) {
        const nInput = document.getElementById('standing_n_' + i);
        const gInput = document.getElementById('standing_g_' + i);
        if (nInput && gInput) {
            values.standing.push({
                n: parseInt(nInput.value) || 0,
                g: parseInt(gInput.value) || 0
            });
        }
    }
    
    // Лежачие
    for (let i = 1; i <= 20; i++) {
        const nInput = document.getElementById('laying_n_' + i);
        const gInput = document.getElementById('laying_g_' + i);
        if (nInput && gInput) {
            values.laying.push({
                n: parseInt(nInput.value) || 0,
                g: parseInt(gInput.value) || 0
            });
        }
    }
    
    return values;
}

// Показать значения
function showValues() {
    const values = getAllValues();
    const resultDiv = document.getElementById('resultDisplay');
    if (resultDiv) {
        let html = '<h4>📊 Текущие значения:</h4>';
        
        // Стоячие
        html += '<p><strong>עומד:</strong></p>';
        values.standing.forEach((item, idx) => {
            if (item.n > 0 || item.g > 0) {
                html += `<p>Строка ${idx+1}: ${item.n} פאנלים, ${item.g} שורות</p>`;
            }
        });
        
        // Лежачие
        html += '<p><strong>שוכב:</strong></p>';
        values.laying.forEach((item, idx) => {
            if (item.n > 0 || item.g > 0) {
                html += `<p>Строка ${idx+1}: ${item.n} פאנלים, ${item.g} שורות</p>`;
            }
        });
        
        resultDiv.innerHTML = html;
    }
}
</script>
'''

# ---------- ОСНОВНОЕ ПРИЛОЖЕНИЕ ----------
st.title("📱 Тест раздела групп - ИСПРАВЛЕНО")

st.markdown("""
<div class="info-box">
<strong>Инструкция:</strong>
<ol>
<li>Должны появиться два раздела (עומד и שוכב)</li>
<li>В каждом разделе - строки с двумя полями рядом</li>
<li>Кнопки + и - должны работать</li>
<li>Можно вводить числа вручную</li>
</ol>
</div>
""", unsafe_allow_html=True)

# Инициализация
if 'standing_rows' not in st.session_state:
    st.session_state.standing_rows = 4  # Уменьшил для теста
if 'laying_rows' not in st.session_state:
    st.session_state.laying_rows = 2

# ---------- РАЗДЕЛ 1: СТОЯЧИЕ ----------
st.markdown('<div class="spoiler-header">עומד (стоячие панели)</div>', unsafe_allow_html=True)

# Заголовки колонок
st.markdown('''
<div class="columns-header">
    <div class="column-label">פאנלים</div>
    <div class="column-label">שורות</div>
</div>
''', unsafe_allow_html=True)

# Создаем строки
for i in range(1, st.session_state.standing_rows + 1):
    html = create_input_row_html("standing", i, default_n=i, default_g=0)
    st.markdown(html, unsafe_allow_html=True)

# Кнопка добавить строку
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    if st.button("➕ עוד שורה (עומד)", key="add_standing"):
        st.session_state.standing_rows += 1
        st.rerun()

# ---------- РАЗДЕЛ 2: ЛЕЖАЧИЕ ----------
st.markdown('<div class="spoiler-header">שוכב (лежачие панели)</div>', unsafe_allow_html=True)

# Заголовки колонок
st.markdown('''
<div class="columns-header">
    <div class="column-label">פאנלים</div>
    <div class="column-label">שורות</div>
</div>
''', unsafe_allow_html=True)

# Создаем строки
for i in range(1, st.session_state.laying_rows + 1):
    default_n = i if i <= 4 else 0
    html = create_input_row_html("laying", i, default_n=default_n, default_g=0)
    st.markdown(html, unsafe_allow_html=True)

# Кнопка добавить строку
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    if st.button("➕ עוד שורה (שוכב)", key="add_laying"):
        st.session_state.laying_rows += 1
        st.rerun()

# ---------- ДОБАВЛЯЕМ JAVASCRIPT ----------
st.markdown(javascript_code, unsafe_allow_html=True)

# ---------- ТЕСТОВАЯ ОБЛАСТЬ ----------
st.markdown("---")
st.subheader("🧪 Тест функциональности")

# Место для отображения результатов
st.markdown('<div id="resultDisplay" style="padding: 15px; border: 1px solid #e2e8f0; border-radius: 8px; margin: 15px 0;"></div>', unsafe_allow_html=True)

# Кнопка для теста
if st.button("🔄 Показать текущие значения", key="test_button"):
    # Запускаем JavaScript
    test_js = '''
    <script>
    setTimeout(function() {
        showValues();
    }, 100);
    </script>
    '''
    components.html(test_js, height=0)

# ---------- СТАТУС ----------
st.markdown("---")
st.write("**Текущее состояние:**")
st.write(f"- Стоячие строки: {st.session_state.standing_rows}")
st.write(f"- Лежачие строки: {st.session_state.laying_rows}")
st.write("**Проверьте на телефоне:** поля должны быть РЯДОМ, не друг под другом")

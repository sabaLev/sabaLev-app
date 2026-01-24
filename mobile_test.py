import streamlit as st
import streamlit.components.v1 as components

st.title("קבוצות פאנלים - простая версия")

# HTML компонента с работающими кнопками
html = '''
<!DOCTYPE html>
<html dir="rtl">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        .section {
            background: #F0F2F6;
            border-radius: 10px;
            padding: 15px;
            margin: 20px 0;
            border: 1px solid #DCDCDC;
        }
        
        .title {
            font-size: 16px;
            font-weight: 600;
            color: #31333F;
            margin-bottom: 15px;
            text-align: center;
        }
        
        .columns {
            display: flex;
            gap: 10px;
            margin-bottom: 10px;
        }
        
        .column-label {
            flex: 1;
            text-align: center;
            font-size: 14px;
            font-weight: 500;
            color: #31333F;
        }
        
        .row {
            display: flex;
            gap: 10px;
            margin-bottom: 10px;
        }
        
        .input-group {
            flex: 1;
            display: flex;
            background: white;
            border-radius: 8px;
            border: 1px solid #DCDCDC;
            overflow: hidden;
            height: 42px;
        }
        
        .btn {
            width: 40px;
            background: #F0F2F6;
            border: none;
            color: #31333F;
            font-size: 20px;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        
        .btn:hover {
            background: #EC5953;
            color: white;
        }
        
        .input {
            flex: 1;
            border: none;
            text-align: center;
            font-size: 16px;
            font-weight: 500;
            padding: 0;
            outline: none;
        }
        
        .add-btn {
            background: #4b75c9;
            color: white;
            border: none;
            border-radius: 6px;
            padding: 8px 16px;
            margin: 10px auto;
            display: block;
            cursor: pointer;
        }
        
        .results {
            background: #f0f9ff;
            border: 2px solid #bae6fd;
            border-radius: 8px;
            padding: 15px;
            margin: 20px 0;
        }
        
        @media (max-width: 768px) {
            .row { gap: 8px; }
            .input-group { height: 38px; }
            .btn { width: 36px; font-size: 18px; }
            .input { font-size: 15px; }
        }
    </style>
</head>
<body>
    <div class="section">
        <div class="title">עומד</div>
        <div class="columns">
            <div class="column-label">פאנלים</div>
            <div class="column-label">שורות</div>
        </div>
        
        <!-- Строка 1 -->
        <div class="row">
            <div class="input-group">
                <button class="btn" onclick="changeValue('standing_n_1', -1)">−</button>
                <input type="number" id="standing_n_1" class="input" value="1" min="0" max="99" oninput="updateValue('standing_n_1', this.value)">
                <button class="btn" onclick="changeValue('standing_n_1', 1)">+</button>
            </div>
            <div class="input-group">
                <button class="btn" onclick="changeValue('standing_g_1', -1)">−</button>
                <input type="number" id="standing_g_1" class="input" value="0" min="0" max="99" oninput="updateValue('standing_g_1', this.value)">
                <button class="btn" onclick="changeValue('standing_g_1', 1)">+</button>
            </div>
        </div>
        
        <!-- Строка 2 -->
        <div class="row">
            <div class="input-group">
                <button class="btn" onclick="changeValue('standing_n_2', -1)">−</button>
                <input type="number" id="standing_n_2" class="input" value="2" min="0" max="99" oninput="updateValue('standing_n_2', this.value)">
                <button class="btn" onclick="changeValue('standing_n_2', 1)">+</button>
            </div>
            <div class="input-group">
                <button class="btn" onclick="changeValue('standing_g_2', -1)">−</button>
                <input type="number" id="standing_g_2" class="input" value="0" min="0" max="99" oninput="updateValue('standing_g_2', this.value)">
                <button class="btn" onclick="changeValue('standing_g_2', 1)">+</button>
            </div>
        </div>
        
        <button class="add-btn" onclick="addRow('standing')">עוד שורה</button>
    </div>
    
    <div class="section">
        <div class="title">שוכב</div>
        <div class="columns">
            <div class="column-label">פאנלים</div>
            <div class="column-label">שורות</div>
        </div>
        
        <!-- Строка 1 -->
        <div class="row">
            <div class="input-group">
                <button class="btn" onclick="changeValue('laying_n_1', -1)">−</button>
                <input type="number" id="laying_n_1" class="input" value="1" min="0" max="99" oninput="updateValue('laying_n_1', this.value)">
                <button class="btn" onclick="changeValue('laying_n_1', 1)">+</button>
            </div>
            <div class="input-group">
                <button class="btn" onclick="changeValue('laying_g_1', -1)">−</button>
                <input type="number" id="laying_g_1" class="input" value="0" min="0" max="99" oninput="updateValue('laying_g_1', this.value)">
                <button class="btn" onclick="changeValue('laying_g_1', 1)">+</button>
            </div>
        </div>
        
        <!-- Строка 2 -->
        <div class="row">
            <div class="input-group">
                <button class="btn" onclick="changeValue('laying_n_2', -1)">−</button>
                <input type="number" id="laying_n_2" class="input" value="2" min="0" max="99" oninput="updateValue('laying_n_2', this.value)">
                <button class="btn" onclick="changeValue('laying_n_2', 1)">+</button>
            </div>
            <div class="input-group">
                <button class="btn" onclick="changeValue('laying_g_2', -1)">−</button>
                <input type="number" id="laying_g_2" class="input" value="0" min="0" max="99" oninput="updateValue('laying_g_2', this.value)">
                <button class="btn" onclick="changeValue('laying_g_2', 1)">+</button>
            </div>
        </div>
        
        <button class="add-btn" onclick="addRow('laying')">עוד שורה</button>
    </div>
    
    <div class="results">
        <h4>🧪 Тест работы:</h4>
        <p>1. Нажмите кнопки + и -</p>
        <p>2. Введите число вручную</p>
        <p>3. Нажмите кнопку ниже</p>
        <button onclick="showValues()" style="background: #10b981; color: white; border: none; padding: 10px 20px; border-radius: 6px; cursor: pointer;">Показать значения</button>
        <div id="values-display" style="margin-top: 15px; padding: 10px; background: white; border-radius: 6px;"></div>
    </div>
    
    <script>
    // Храним данные
    let data = {
        standing: {
            'n_1': 1, 'g_1': 0,
            'n_2': 2, 'g_2': 0
        },
        laying: {
            'n_1': 1, 'g_1': 0,
            'n_2': 2, 'g_2': 0
        }
    };
    
    // Изменить значение
    function changeValue(id, delta) {
        const input = document.getElementById(id);
        let value = parseInt(input.value) || 0;
        value += delta;
        if (value < 0) value = 0;
        if (value > 99) value = 99;
        input.value = value;
        saveValue(id, value);
    }
    
    // Обновить значение ручного ввода
    function updateValue(id, value) {
        const numValue = parseInt(value) || 0;
        if (numValue < 0) document.getElementById(id).value = 0;
        if (numValue > 99) document.getElementById(id).value = 99;
        saveValue(id, numValue);
    }
    
    // Сохранить значение
    function saveValue(id, value) {
        const [type, field, index] = id.split('_');
        const key = `${field}_${index}`;
        if (type === 'standing') {
            data.standing[key] = value;
        } else {
            data.laying[key] = value;
        }
        console.log('Сохранено:', id, '=', value);
    }
    
    // Добавить строку (упрощенная версия)
    function addRow(type) {
        alert('Функция "עוד שורה" работает! В реальном приложении добавится новая строка.');
    }
    
    // Показать значения
    function showValues() {
        const display = document.getElementById('values-display');
        let html = '<strong>Текущие значения:</strong><br><br>';
        
        html += '<strong>עומד:</strong><br>';
        for (let i = 1; i <= 2; i++) {
            const n = data.standing[`n_${i}`] || 0;
            const g = data.standing[`g_${i}`] || 0;
            html += `Строка ${i}: ${n} פאנלים, ${g} שורות<br>`;
        }
        
        html += '<br><strong>שוכב:</strong><br>';
        for (let i = 1; i <= 2; i++) {
            const n = data.laying[`n_${i}`] || 0;
            const g = data.laying[`g_${i}`] || 0;
            html += `Строка ${i}: ${n} פאנלים, ${g} שורות<br>`;
        }
        
        display.innerHTML = html;
        
        // Отправляем в Streamlit (для будущей интеграции)
        window.parent.postMessage({
            type: 'groups_data',
            data: data
        }, '*');
    }
    </script>
</body>
</html>
'''

# Отображаем компоненту
components.html(html, height=800)

# Кнопка расчета в Streamlit
st.write("---")
if st.button("חשב (тест)", type="primary"):
    st.info("В реальном приложении здесь будет расчет на основе значений из компоненты")
    
    # JavaScript для получения данных
    js = '''
    <script>
    // Запрашиваем данные у компоненты
    if (window.showValues) {
        showValues();
        setTimeout(() => {
            alert("Данные отправлены в Streamlit!");
        }, 500);
    }
    </script>
    '''
    components.html(js, height=0)

st.write("**Проверьте:**")
st.write("1. Кнопки + и - работают?")
st.write("2. Ручной ввод работает?")
st.write("3. Нажмите 'Показать значения' в компоненте")
st.write("4. Значения отображаются правильно?")

import streamlit as st
import streamlit.components.v1 as components

# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="Тест групп",
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
        margin: 0 0 15px 0;
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

# ---------- HELPER FUNCTION ----------
def create_input_row(panel_type, row_num, default_n=0, default_g=0):
    """Создает строку с двумя инпутами"""
    
    return f'''
    <div class="input-row" id="row_{panel_type}_{row_num}">
        <!-- Поле "פאנלים" -->
        <div class="input-column">
            <div class="streamlit-style-input">
                <input type="number" 
                       id="{panel_type}_n_{row_num}" 
                       value="{default_n}" 
                       min="0" 
                       max="99" 
                       class="number-input"
                       oninput="validateInput(this)">
                <div class="button-group">
                    <button class="stepper-button" type="button" 
                            onclick="adjustValue('{panel_type}_n_{row_num}', -1)">−</button>
                    <button class="stepper-button" type="button" 
                            onclick="adjustValue('{panel_type}_n_{row_num}', 1)">+</button>
                </div>
            </div>
        </div>
        
        <!-- Поле "שורות" -->
        <div class="input-column">
            <div class="streamlit-style-input">
                <input type="number" 
                       id="{panel_type}_g_{row_num}" 
                       value="{default_g}" 
                       min="0" 
                       max="99" 
                       class="number-input"
                       oninput="validateInput(this)">
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
javascript = '''
<script>
// Корректировка значения кнопками +/-
function adjustValue(inputId, change) {
    const input = document.getElementById(inputId);
    let value = parseInt(input.value) || 0;
    value += change;
    
    // Ограничения 0-99
    if (value < 0) value = 0;
    if (value > 99) value = 99;
    
    input.value = value;
    
    // Проверка на слишком большие значения
    if (value > 90) {
        showWarning(inputId, value);
    }
}

// Валидация ручного ввода
function validateInput(input) {
    let value = parseInt(input.value) || 0;
    
    if (value < 0) {
        input.value = 0;
        value = 0;
    }
    
    if (value > 99) {
        input.value = 99;
        value = 99;
        showWarning(input.id, value);
    }
}

// Предупреждение для больших значений
function showWarning(inputId, value) {
    const isRows = inputId.includes('_g_');
    const isPanels = inputId.includes('_n_');
    
    if (value > 90) {
        if (isRows) {
            alert(`וואי! ${value} שורות? אולי תפצל למערכות קטנות יותר? 😄`);
        } else if (isPanels) {
            alert(`וואי! ${value} פאנלים בשורה אחת? אולי תפצל לשתי שורות? 😄`);
        }
    }
}

// Функция для получения всех значений (для теста)
function getAllValues() {
    const values = {
        standing: [],
        laying: []
    };
    
    console.log("Собираем значения...");
    
    // Собираем стоячие (до 20 строк)
    for (let i = 1; i <= 20; i++) {
        const nInput = document.getElementById('standing_n_' + i);
        const gInput = document.getElementById('standing_g_' + i);
        
        if (nInput && gInput) {
            const n = parseInt(nInput.value) || 0;
            const g = parseInt(gInput.value) || 0;
            
            console.log(`Стоячие строка ${i}: n=${n}, g=${g}`);
            
            if (n > 0 && g > 0) {
                values.standing.push({n: n, g: g, type: 'עומד'});
            }
        }
    }
    
    // Собираем лежачие (до 20 строк)
    for (let i = 1; i <= 20; i++) {
        const nInput = document.getElementById('laying_n_' + i);
        const gInput = document.getElementById('laying_g_' + i);
        
        if (nInput && gInput) {
            const n = parseInt(nInput.value) || 0;
            const g = parseInt(gInput.value) || 0;
            
            console.log(`Лежачие строка ${i}: n=${n}, g=${g}`);
            
            if (n > 0 && g > 0) {
                values.laying.push({n: n, g: g, type: 'שוכב'});
            }
        }
    }
    
    console.log("Итоговые значения:", values);
    return values;
}

// Тестовая функция для показа значений
function showCurrentValues() {
    const values = getAllValues();
    const resultDiv = document.getElementById('testResult');
    
    if (resultDiv) {
        let html = '<h4>📊 Текущие значения:</h4>';
        
        if (values.standing.length > 0) {
            html += '<p><strong>עומד (стоячие):</strong></p>';
            values.standing.forEach((item, i) => {
                html += `<p>Строка ${i+1}: ${item.n} פאנלים × ${item.g} שורות</p>`;
            });
        } else {
            html += '<p>עומד: нет данных</p>';
        }
        
        if (values.laying.length > 0) {
            html += '<p><strong>שוכב (лежачие):</strong></p>';
            values.laying.forEach((item, i) => {
                html += `<p>Строка ${i+1}: ${item.n} פאנלים × ${item.g} שורות</p>`;
            });
        } else {
            html += '<p>שוכב: нет данных</p>';
        }
        
        resultDiv.innerHTML = html;
    }
    
    return values;
}
</script>
'''

# ---------- MAIN APP ----------
st.title("📱 Тест раздела групп")

st.markdown("""
<div class="info-box">
<strong>Что тестируем:</strong>
<ul>
<li>Два спойлера (עומד и שוכב)</li>
<li>Две колонки на мобильных (פאנלים и שורות)</li>
<li>Кнопки + и - работают</li>
<li>Можно вводить вручную</li>
<li>Дизайн похож на нативные Streamlit кнопки</li>
</ul>
</div>
""", unsafe_allow_html=True)

# Инициализация состояния
if 'standing_rows' not in st.session_state:
    st.session_state.standing_rows = 8

if 'laying_rows' not in st.session_state:
    st.session_state.laying_rows = 4

# ---------- СПОЙЛЕР 1: СТОЯЧИЕ ПАНЕЛИ ----------
st.markdown('<div class="spoiler-header">עומד (стоячие панели)</div>', unsafe_allow_html=True)

# Заголовки колонок
st.markdown('''
<div class="columns-header">
    <div class="column-label">פאנלים</div>
    <div class="column-label">שורות</div>
</div>
''', unsafe_allow_html=True)

# Создаем строки для стоячих панелей
standing_html = ""
for i in range(1, st.session_state.standing_rows + 1):
    default_n = i  # 1, 2, 3... 8
    default_g = 0  # всегда 0 по умолчанию
    standing_html += create_input_row("standing", i, default_n, default_g)

st.markdown(standing_html, unsafe_allow_html=True)

# Кнопка "עוד שורה" для стоячих
if st.button("עוד שורה (עומד)", key="add_standing"):
    st.session_state.standing_rows += 1
    st.rerun()

# ---------- СПОЙЛЕР 2: ЛЕЖАЧИЕ ПАНЕЛИ ----------
st.markdown('<div class="spoiler-header">שוכב (лежачие панели)</div>', unsafe_allow_html=True)

# Заголовки колонок
st.markdown('''
<div class="columns-header">
    <div class="column-label">פאנלים</div>
    <div class="column-label">שורות</div>
</div>
''', unsafe_allow_html=True)

# Создаем строки для лежачих панелей
laying_html = ""
for i in range(1, st.session_state.laying_rows + 1):
    default_n = i if i <= 4 else 0  # 1, 2, 3, 4, потом 0
    default_g = 0  # всегда 0 по умолчанию
    laying_html += create_input_row("laying", i, default_n, default_g)

st.markdown(laying_html, unsafe_allow_html=True)

# Кнопка "עוד שורה" для лежачих
if st.button("עוד שורה (שוכב)", key="add_laying"):
    st.session_state.laying_rows += 1
    st.rerun()

# ---------- JAVASCRIPT КОД ----------
st.markdown(javascript, unsafe_allow_html=True)

# ---------- ТЕСТОВАЯ КНОПКА ----------
st.markdown("---")
st.markdown("### 🧪 Тест функциональности")

# Место для вывода результатов
st.markdown('<div id="testResult" style="margin: 20px 0; padding: 15px; border: 1px solid #e2e8f0; border-radius: 8px;"></div>', unsafe_allow_html=True)

# Кнопка для теста
if st.button("Показать текущие значения", key="show_values"):
    # JavaScript для получения и отображения значений
    test_js = '''
    <script>
    setTimeout(function() {
        showCurrentValues();
    }, 100);
    </script>
    '''
    components.html(test_js, height=0)

# ---------- ИНФОРМАЦИЯ ----------
st.markdown("---")
st.markdown("""
<div class="info-box">
<strong>Инструкция по тесту:</strong>
<ol>
<li>Откройте на телефоне</li>
<li>Проверьте, что два поля в строке идут РЯДОМ (не друг под другом)</li>
<li>Нажмите кнопки + и - (значения должны меняться)</li>
<li>Введите число вручную (должно работать)</li>
<li>Нажмите "Показать текущие значения"</li>
<li>Добавьте строки кнопками "עוד שורה"</li>
</ol>
</div>
""", unsafe_allow_html=True)

# ---------- СТАТУС ----------
st.markdown("---")
st.write(f"**Текущее состояние:**")
st.write(f"- Стоячие строки: {st.session_state.standing_rows}")
st.write(f"- Лежачие строки: {st.session_state.laying_rows}")

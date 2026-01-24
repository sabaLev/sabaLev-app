import streamlit as st
import streamlit.components.v1 as components

st.title("📱 Тест рабочих кнопок")

# Инициализация значения в памяти
if 'test_value' not in st.session_state:
    st.session_state.test_value = 1

st.write(f"**Текущее значение в памяти:** {st.session_state.test_value}")

# HTML компонента с работающими кнопками
html = f'''
<div style="
    background: #f8f9fa;
    border-radius: 12px;
    padding: 20px;
    margin: 20px 0;
    border: 1px solid #dee2e6;
">
    <h3 style="text-align: center; margin-bottom: 15px;">פאנלים</h3>
    
    <div style="
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 15px;
    ">
        <button style="
            background: #dc3545;
            color: white;
            border: none;
            border-radius: 8px;
            width: 50px;
            height: 50px;
            font-size: 24px;
            cursor: pointer;
            font-weight: bold;
        "
        onclick="changeValue(-1)"
        >-</button>
        
        <div id="valueDisplay" style="
            font-size: 36px;
            font-weight: bold;
            min-width: 60px;
            text-align: center;
            background: white;
            padding: 10px 20px;
            border-radius: 8px;
            border: 2px solid #4b75c9;
        ">{st.session_state.test_value}</div>
        
        <button style="
            background: #28a745;
            color: white;
            border: none;
            border-radius: 8px;
            width: 50px;
            height: 50px;
            font-size: 24px;
            cursor: pointer;
            font-weight: bold;
        "
        onclick="changeValue(1)"
        >+</button>
    </div>
    
    <div style="
        text-align: center;
        margin-top: 15px;
        color: #6c757d;
        font-size: 14px;
    ">
        Нажмите + или - чтобы изменить значение
    </div>
</div>

<script>
let currentValue = {st.session_state.test_value};

function changeValue(delta) {{
    currentValue += delta;
    if (currentValue < 0) currentValue = 0;
    if (currentValue > 99) currentValue = 99;
    
    // Обновляем отображение
    document.getElementById('valueDisplay').innerText = currentValue;
    
    // Отправляем в Streamlit
    window.parent.postMessage({{
        type: 'update_value',
        value: currentValue
    }}, '*');
}}
</script>
'''

components.html(html, height=250)

# JavaScript для получения данных от компоненты
components.html('''
<script>
window.addEventListener('message', function(event) {
    if (event.data.type === 'update_value') {
        // Отправляем в Streamlit
        window.parent.postMessage({
            type: 'streamlit:setComponentValue',
            value: event.data.value
        }, '*');
    }
});
</script>
''', height=0)

# Кнопка для проверки сохранения значения
st.write("---")
st.write("**Проверка:**")

if st.button("🔄 Обновить страницу и проверить значение"):
    st.rerun()

st.write("**Инструкция:**")
st.write("1. Нажмите кнопку + или - несколько раз")
st.write("2. Значение в центре должно меняться")
st.write("3. Нажмите кнопку 'Обновить' выше")
st.write("4. Значение должно сохраниться после обновления")

# Отображаем все значения session_state
with st.expander("📊 Показать все значения в памяти"):
    st.write(st.session_state)

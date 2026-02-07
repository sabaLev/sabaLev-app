import streamlit as st

# CSS для создания двух сайдбаров
st.markdown("""
<style>
/* Левая панель (кастомный сайдбар) */
[data-testid="stSidebar"] {
    min-width: 300px !important;
    max-width: 300px !important;
}

/* Создаем правую панель */
.right-sidebar {
    position: fixed;
    top: 0;
    right: 0;
    height: 100vh;
    width: 300px;
    background: #f0f2f6;
    padding: 20px;
    overflow-y: auto;
    z-index: 999;
    border-left: 1px solid #ddd;
}

/* Сдвигаем основной контент */
.main .block-container {
    padding-left: 320px !important;
    padding-right: 320px !important;
    max-width: calc(100vw - 640px) !important;
}

/* Скрываем дефолтный правый padding */
.css-1d391kg {
    padding-right: 0 !important;
}
</style>
""", unsafe_allow_html=True)

# ===== ЛЕВАЯ ПАНЕЛЬ (нативный сайдбар) =====
with st.sidebar:
    st.title("📁 Панель А")
    st.markdown("---")
    
    # Независимые элементы левой панели
    left_counter = st.number_input("Счетчик А", 0, 100, 10, key="left_counter")
    st.progress(left_counter / 100)
    
    left_text = st.text_input("Введите для А:", key="left_text")
    st.write(f"**А получил:** {left_text}")
    
    left_option = st.selectbox("Выбор А:", ["Опция 1", "Опция 2"], key="left_select")
    st.button("Действие А", key="btn_a")

# ===== ОСНОВНОЙ КОНТЕНТ =====
st.title("🎯 Центральная панель")
st.write("Это основное рабочее пространство")
st.slider("Общий слайдер", 0, 100, 50)

# ===== ПРАВАЯ ПАНЕЛЬ (через HTML) =====
right_panel_html = f"""
<div class="right-sidebar">
    <h2>📊 Панель Б</h2>
    <hr>
    <p>Независимая правая панель</p>
    
    <div style="margin: 20px 0;">
        <label>Счетчик Б:</label>
        <input type="range" min="0" max="100" value="30" 
               id="rightSlider" style="width: 100%;">
        <div id="rightValue">30</div>
    </div>
    
    <div style="margin: 20px 0;">
        <input type="text" id="rightInput" placeholder="Введите для Б" 
               style="width: 100%; padding: 8px;">
    </div>
    
    <button onclick="alert('Из панели Б: ' + document.getElementById('rightInput').value)"
            style="padding: 10px; width: 100%; background: #4CAF50; color: white; border: none;">
        Отправить Б
    </button>
    
    <script>
        // Обновление значения слайдера
        document.getElementById('rightSlider').addEventListener('input', function(e) {{
            document.getElementById('rightValue').innerText = e.target.value;
        }});
        
        // Отправка данных в Streamlit
        function sendToStreamlit() {{
            window.parent.postMessage({{
                type: 'streamlit:setComponentValue',
                value: document.getElementById('rightInput').value
            }}, '*');
        }}
    </script>
</div>
"""

st.components.v1.html(right_panel_html, height=0)

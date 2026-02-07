import streamlit as st

# Настройка страницы
st.set_page_config(layout="wide", initial_sidebar_state="collapsed")

# CSS для фиксированных панелей
st.markdown("""
<style>
/* Отключаем скролл у body */
.stApp {
    overflow: hidden;
}

/* Левая фиксированная панель */
.fixed-left-panel {
    position: fixed;
    left: 0;
    top: 0;
    width: 280px;
    height: 100vh;
    background: white;
    border-right: 2px solid #e0e0e0;
    padding: 20px;
    overflow-y: auto;
    z-index: 100;
}

/* Правая фиксированная панель */
.fixed-right-panel {
    position: fixed;
    right: 0;
    top: 0;
    width: 280px;
    height: 100vh;
    background: white;
    border-left: 2px solid #e0e0e0;
    padding: 20px;
    overflow-y: auto;
    z-index: 100;
}

/* Центральный контент */
.main-content {
    margin-left: 300px;
    margin-right: 300px;
    padding: 20px;
    min-height: 100vh;
}
</style>
""", unsafe_allow_html=True)

# ===== ЛЕВАЯ ПАНЕЛЬ =====
left_panel = """
<div class="fixed-left-panel">
    <h3>🔧 Инструменты</h3>
    <hr>
    <div style="margin: 15px 0;">
        <strong>Настройки:</strong><br>
        <input type="checkbox" id="tool1"> <label for="tool1">Опция 1</label><br>
        <input type="checkbox" id="tool2"> <label for="tool2">Опция 2</label><br>
        <input type="checkbox" id="tool3"> <label for="tool3">Опция 3</label>
    </div>
    
    <div style="margin: 15px 0;">
        <label>Уровень:</label>
        <input type="range" min="1" max="10" value="5" style="width: 100%;">
    </div>
    
    <button onclick="runLeftPanel()" 
            style="width: 100%; padding: 10px; background: #2196F3; color: white; border: none;">
        Применить
    </button>
    
    <div style="margin-top: 20px; padding: 10px; background: #f5f5f5; border-radius: 5px;">
        <small>Левая панель полностью независима</small>
    </div>
    
    <script>
    function runLeftPanel() {
        const checks = [
            document.getElementById('tool1').checked,
            document.getElementById('tool2').checked,
            document.getElementById('tool3').checked
        ];
        alert('Левые настройки: ' + checks);
    }
    </script>
</div>
"""

# ===== ПРАВАЯ ПАНЕЛЬ =====
right_panel = """
<div class="fixed-right-panel">
    <h3>📈 Мониторинг</h3>
    <hr>
    
    <div style="margin: 15px 0;">
        <strong>Показатели:</strong>
        <div style="background: #e8f5e8; padding: 10px; margin: 5px 0; border-radius: 5px;">
            CPU: <span id="cpu">45%</span>
        </div>
        <div style="background: #e3f2fd; padding: 10px; margin: 5px 0; border-radius: 5px;">
            Память: <span id="mem">67%</span>
        </div>
    </div>
    
    <div style="margin: 15px 0;">
        <label>Обновлять каждые:</label>
        <select style="width: 100%; padding: 5px;">
            <option>5 секунд</option>
            <option>10 секунд</option>
            <option>30 секунд</option>
        </select>
    </div>
    
    <button onclick="refreshMetrics()"
            style="width: 100%; padding: 10px; background: #4CAF50; color: white; border: none; margin-top: 10px;">
        Обновить
    </button>
    
    <script>
    function refreshMetrics() {
        // Случайные значения для демонстрации
        document.getElementById('cpu').innerText = Math.floor(Math.random() * 100) + '%';
        document.getElementById('mem').innerText = Math.floor(Math.random() * 100) + '%';
    }
    
    // Автообновление каждые 10 секунд
    setInterval(refreshMetrics, 10000);
    </script>
</div>
"""

# ===== ОТОБРАЖЕНИЕ =====
# Рендерим фиксированные панели
st.components.v1.html(left_panel, height=0)
st.components.v1.html(right_panel, height=0)

# Основной контент
st.markdown('<div class="main-content">', unsafe_allow_html=True)

st.title("📝 Основное рабочее пространство")
st.write("Это центральная область между двумя независимыми панелями")

# Пример основного контента
tab1, tab2, tab3 = st.tabs(["Документ", "Графики", "Настройки"])

with tab1:
    st.header("Редактор")
    content = st.text_area("Содержание:", height=200, placeholder="Введите текст здесь...")
    if st.button("Сохранить документ"):
        st.success("Документ сохранен!")

with tab2:
    import pandas as pd
    import numpy as np
    chart_data = pd.DataFrame(np.random.randn(50, 3), columns=['A', 'B', 'C'])
    st.line_chart(chart_data)

with tab3:
    col1, col2 = st.columns(2)
    with col1:
        st.checkbox("Автосохранение")
        st.checkbox("Уведомления")
    with col2:
        st.selectbox("Тема", ["Светлая", "Темная"])
        st.color_picker("Цвет акцента")

st.markdown('</div>', unsafe_allow_html=True)

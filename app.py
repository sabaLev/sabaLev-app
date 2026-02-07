import streamlit as st
import streamlit.components.v1 as components

# HTML/CSS компонент для таблицы
table_html = """
<style>
.panels-container {
    width: 100%;
    margin: 20px 0;
}

.table-header {
    display: flex;
    margin-bottom: 10px;
    font-weight: bold;
}

.header-cell {
    flex: 1;
    text-align: right;
    padding: 0 10px;
}

.table-row {
    display: flex;
    margin-bottom: 15px;
    align-items: center;
}

.input-cell {
    flex: 1;
    padding: 0 10px;
}

.text-cell {
    flex: 1;
    text-align: center;
    padding: 0 10px;
    font-size: 16px;
    color: #333;
    min-height: 45px;
    display: flex;
    align-items: center;
    justify-content: center;
}

/* Мобильная адаптация */
@media (max-width: 768px) {
    .table-row {
        flex-direction: row !important;
    }
    
    .input-cell, .text-cell {
        width: 50% !important;
        flex: 0 0 50% !important;
    }
    
    .text-cell {
        font-size: 16px;
        height: 44px;
    }
    
    /* Стили для input внутри ячейки */
    .input-cell input {
        width: 100% !important;
        height: 44px !important;
        font-size: 16px !important;
        padding: 10px 12px !important;
        box-sizing: border-box !important;
    }
}

/* Десктоп */
@media (min-width: 769px) {
    .input-cell input {
        width: 100%;
        height: 45px;
        padding: 8px 12px;
        font-size: 16px;
        border: 1px solid #d1d5db;
        border-radius: 6px;
        box-sizing: border-box;
    }
}
</style>

<div class="panels-container">
    <!-- Заголовки -->
    <div class="table-header">
        <div class="header-cell">שורות</div>
        <div class="header-cell">פאנלים</div>
    </div>
    
    <!-- Строка 1 -->
    <div class="table-row">
        <div class="input-cell">
            <input type="number" min="0" max="50" value="0" 
                   style="width:100%; height:45px; padding:8px 12px; font-size:16px; border:1px solid #d1d5db; border-radius:6px; box-sizing:border-box;">
        </div>
        <div class="text-cell">1</div>
    </div>
    
    <!-- Строка 2 -->
    <div class="table-row">
        <div class="input-cell">
            <input type="number" min="0" max="50" value="0" 
                   style="width:100%; height:45px; padding:8px 12px; font-size:16px; border:1px solid #d1d5db; border-radius:6px; box-sizing:border-box;">
        </div>
        <div class="text-cell">2</div>
    </div>
</div>
"""

st.title("Тест таблицы (чистый HTML)")

# Отображаем HTML компонент
components.html(table_html, height=200)

st.markdown("---")
st.write("**Что должно быть:**")
st.write("На всех устройствах - 2 колонки рядом")
st.write("Левая: поле ввода, Правая: текст '1' и '2'")

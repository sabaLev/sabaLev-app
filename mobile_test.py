import streamlit as st
import pandas as pd
import math

# Настройки страницы
st.set_page_config(
    page_title="סולארי פשוט",
    page_icon="☀️",
    layout="centered"
)

# Стили для мобильных
st.markdown("""
<style>
/* Базовая стилизация */
.main {
    padding: 15px;
}
.group-box {
    background: #f8fafc;
    border-radius: 12px;
    padding: 15px;
    margin: 15px 0;
    border: 1px solid #e2e8f0;
}
.group-title {
    color: #1e40af;
    text-align: right;
    font-size: 18px;
    font-weight: 600;
    margin-bottom: 15px;
    padding-bottom: 8px;
    border-bottom: 2px solid #e2e8f0;
}
.row {
    display: flex;
    align-items: center;
    margin: 10px 0;
    padding: 8px;
    background: white;
    border-radius: 8px;
    border: 1px solid #e2e8f0;
}
.label {
    flex: 1;
    text-align: right;
    padding: 0 10px;
    font-weight: 500;
}
.input-container {
    flex: 2;
    min-width: 0;
}
/* Убираем стрелки у number input */
input[type="number"]::-webkit-inner-spin-button,
input[type="number"]::-webkit-outer-spin-button {
    -webkit-appearance: none;
    margin: 0;
}
input[type="number"] {
    -moz-appearance: textfield;
    appearance: textfield;
}
/* Кнопка расчета */
.calc-btn {
    background: linear-gradient(135deg, #1e40af, #3b82f6);
    color: white;
    border: none;
    border-radius: 10px;
    padding: 16px;
    font-size: 18px;
    font-weight: 600;
    width: 100%;
    margin: 20px 0;
    cursor: pointer;
}
.calc-btn:hover {
    background: linear-gradient(135deg, #1e3a8a, #2563eb);
}
/* Результаты */
.result-box {
    background: #f0f9ff;
    border: 2px solid #0ea5e9;
    border-radius: 10px;
    padding: 15px;
    margin: 15px 0;
}
/* На мобильных */
@media (max-width: 768px) {
    .row {
        flex-direction: row;
        padding: 6px;
    }
    .label {
        font-size: 14px;
    }
    input {
        font-size: 16px;
        padding: 10px;
    }
}
</style>
""", unsafe_allow_html=True)

# Заголовок
st.markdown("<h1 style='text-align: center; color: #1e40af;'>סולארי פשוט</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #64748b;'>חישוב פאנלים סולאריים</p>", unsafe_allow_html=True)

# Стоячие панели
st.markdown("<div class='group-box'>", unsafe_allow_html=True)
st.markdown("<div class='group-title'>פאנלים עומדים</div>", unsafe_allow_html=True)

standing_data = {}
for i in range(1, 9):  # 1-8 панелей
    st.markdown("<div class='row'>", unsafe_allow_html=True)
    st.markdown(f"<div class='label'>{i} פאנלים</div>", unsafe_allow_html=True)
    st.markdown("<div class='input-container'>", unsafe_allow_html=True)
    
    # Числовое поле с кнопками
    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        if st.button("➖", key=f"s_minus_{i}", use_container_width=True):
            if f"standing_{i}" not in st.session_state:
                st.session_state[f"standing_{i}"] = 0
            st.session_state[f"standing_{i}"] = max(0, st.session_state[f"standing_{i}"] - 1)
            st.rerun()
    
    with col2:
        value = st.number_input(
            "",
            min_value=0,
            max_value=99,
            value=st.session_state.get(f"standing_{i}", 0),
            key=f"standing_input_{i}",
            label_visibility="collapsed"
        )
        standing_data[i] = value
    
    with col3:
        if st.button("➕", key=f"s_plus_{i}", use_container_width=True):
            if f"standing_{i}" not in st.session_state:
                st.session_state[f"standing_{i}"] = 0
            st.session_state[f"standing_{i}"] = min(99, st.session_state[f"standing_{i}"] + 1)
            st.rerun()
    
    st.markdown("</div></div>", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# Лежачие панели
st.markdown("<div class='group-box'>", unsafe_allow_html=True)
st.markdown("<div class='group-title'>פאנלים שוכבים</div>", unsafe_allow_html=True)

laying_data = {}
for i in range(1, 5):  # 1-4 панели
    st.markdown("<div class='row'>", unsafe_allow_html=True)
    st.markdown(f"<div class='label'>{i} פאנלים</div>", unsafe_allow_html=True)
    st.markdown("<div class='input-container'>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        if st.button("➖", key=f"l_minus_{i}", use_container_width=True):
            if f"laying_{i}" not in st.session_state:
                st.session_state[f"laying_{i}"] = 0
            st.session_state[f"laying_{i}"] = max(0, st.session_state[f"laying_{i}"] - 1)
            st.rerun()
    
    with col2:
        value = st.number_input(
            "",
            min_value=0,
            max_value=99,
            value=st.session_state.get(f"laying_{i}", 0),
            key=f"laying_input_{i}",
            label_visibility="collapsed"
        )
        laying_data[i] = value
    
    with col3:
        if st.button("➕", key=f"l_plus_{i}", use_container_width=True):
            if f"laying_{i}" not in st.session_state:
                st.session_state[f"laying_{i}"] = 0
            st.session_state[f"laying_{i}"] = min(99, st.session_state[f"laying_{i}"] + 1)
            st.rerun()
    
    st.markdown("</div></div>", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# Кнопка расчета
if st.button("🧮 חשב תוצאות", key="calculate", use_container_width=True):
    # Собираем данные
    groups = []
    total_panels = 0
    total_rows = 0
    
    for panels_count, rows_count in standing_data.items():
        if rows_count > 0:
            groups.append([panels_count, rows_count, "עומד"])
            total_panels += panels_count * rows_count
            total_rows += rows_count
    
    for panels_count, rows_count in laying_data.items():
        if rows_count > 0:
            groups.append([panels_count, rows_count, "שוכב"])
            total_panels += panels_count * rows_count
            total_rows += rows_count
    
    # Показываем результаты
    st.markdown("<div class='result-box'>", unsafe_allow_html=True)
    
    if groups:
        st.markdown(f"### 📊 תוצאות")
        st.markdown(f"**קבוצות:** {len(groups)}")
        st.markdown(f"**פאנלים:** {total_panels}")
        st.markdown(f"**שורות:** {total_rows}")
        
        st.markdown("**פירוט:**")
        for n, g, o in groups:
            st.markdown(f"- {n} פאנלים {o} (x{g})")
        
        # Простой расчет (пример)
        st.markdown("---")
        st.markdown("**חומרים (דוגמה):**")
        st.markdown(f"- קושרות: {total_rows * 2}")
        st.markdown(f"- מהדקים: {total_panels * 2}")
        st.markdown(f"- ברגים: {total_panels * 4}")
    else:
        st.warning("לא הוזנו נתונים")
    
    st.markdown("</div>", unsafe_allow_html=True)

# Инструкция
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #64748b; font-size: 14px;'>
    <strong>הוראות:</strong>
    <br>1. הזן מספר שורות עבור כל קבוצת פאנלים
    <br>2. לחץ על ➕/➖ כדי לשנות
    <br>3. לחץ "חשב תוצאות"
</div>
""", unsafe_allow_html=True)

# Футер
st.markdown("""
<div style='text-align: center; margin-top: 30px; color: #94a3b8; font-size: 12px;'>
    © 2024 סולארי פשוט | גרסה בסיסית
</div>
""", unsafe_allow_html=True)

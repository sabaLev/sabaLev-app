import streamlit as st
import pandas as pd
import numpy as np

# Инициализация независимых состояний
if 'panel1_state' not in st.session_state:
    st.session_state.panel1_state = {'counter': 0, 'data': [], 'text': ''}
if 'panel2_state' not in st.session_state:
    st.session_state.panel2_state = {'counter': 0, 'data': [], 'text': ''}

def render_panel(panel_name, panel_state):
    """Рендерит независимую панель"""
    st.header(f"📌 {panel_name}")
    
    # Счетчик только для этой панели
    col1, col2 = st.columns(2)
    with col1:
        if st.button(f"➕ {panel_name}", key=f"inc_{panel_name}"):
            panel_state['counter'] += 1
    with col2:
        if st.button(f"➖ {panel_name}", key=f"dec_{panel_name}"):
            panel_state['counter'] -= 1
    
    st.metric(f"Счетчик {panel_name}", panel_state['counter'])
    
    # Ввод текста только для этой панели
    text = st.text_input(f"Введите текст для {panel_name}", 
                        value=panel_state['text'],
                        key=f"text_{panel_name}")
    panel_state['text'] = text
    
    # Данные только для этой панели
    if st.button(f"Сгенерировать данные для {panel_name}", key=f"data_{panel_name}"):
        panel_state['data'] = np.random.randn(10, 2).tolist()
    
    if panel_state['data']:
        df = pd.DataFrame(panel_state['data'], columns=['X', 'Y'])
        st.line_chart(df)
    
    return panel_state

# Основной layout
st.set_page_config(layout="wide")

# Две независимые колонки
col_left, col_right = st.columns(2, gap="large")

with col_left:
    st.session_state.panel1_state = render_panel(
        "Левая панель", 
        st.session_state.panel1_state
    )

with col_right:
    st.session_state.panel2_state = render_panel(
        "Правая панель", 
        st.session_state.panel2_state
    )

# Панель управления (опционально)
st.divider()
st.write("**Состояния панелей (только для отладки):**")
st.json({
    "Левая панель": st.session_state.panel1_state,
    "Правая панель": st.session_state.panel2_state
})

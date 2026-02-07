import streamlit as st

st.markdown("""
<style>
/* Контейнер для горизонтальных табов */
.horizontal-tabs {
    display: flex;
    overflow-x: auto;
    white-space: nowrap;
    padding: 10px 0;
    margin: 20px 0;
    border-bottom: 2px solid #e0e0e0;
    min-width: 600px;
}

/* Индивидуальные табы */
.horizontal-tab {
    padding: 10px 20px;
    margin-right: 5px;
    background: #f0f2f6;
    border-radius: 5px 5px 0 0;
    cursor: pointer;
    border: 1px solid #ddd;
    border-bottom: none;
    min-width: 150px;
    text-align: center;
}

.horizontal-tab.active {
    background: white;
    border-color: #262730;
    font-weight: bold;
}

/* Контент табов */
.tab-content {
    min-width: 600px;
    padding: 20px;
    border: 1px solid #ddd;
    border-top: none;
    border-radius: 0 0 5px 5px;
}

/* Поддержка touch-скролла */
@media (max-width: 640px) {
    .horizontal-tabs {
        -webkit-overflow-scrolling: touch;
        scrollbar-width: thin;
    }
    
    .tab-content {
        min-width: 550px;
    }
}
</style>
""", unsafe_allow_html=True)

st.title("📱 Горизонтальные табы с прокруткой")

# Инициализация состояния
if 'active_tab' not in st.session_state:
    st.session_state.active_tab = "tab1"

# HTML для табов
tabs_html = """
<div class="horizontal-tabs">
    <div class="horizontal-tab %s" onclick="setActiveTab('tab1')">📊 Дашборд</div>
    <div class="horizontal-tab %s" onclick="setActiveTab('tab2')">📈 Аналитика</div>
    <div class="horizontal-tab %s" onclick="setActiveTab('tab3')">👥 Пользователи</div>
    <div class="horizontal-tab %s" onclick="setActiveTab('tab4')">⚙️ Настройки</div>
    <div class="horizontal-tab %s" onclick="setActiveTab('tab5')">📋 Отчеты</div>
    <div class="horizontal-tab %s" onclick="setActiveTab('tab6')">🔧 Инструменты</div>
</div>

<script>
function setActiveTab(tabName) {
    window.parent.postMessage({
        type: 'streamlit:setComponentValue',
        value: tabName
    }, '*');
}
</script>
""" % (
    "active" if st.session_state.active_tab == "tab1" else "",
    "active" if st.session_state.active_tab == "tab2" else "",
    "active" if st.session_state.active_tab == "tab3" else "",
    "active" if st.session_state.active_tab == "tab4" else "",
    "active" if st.session_state.active_tab == "tab5" else "",
    "active" if st.session_state.active_tab == "tab6" else ""
)

# Отображаем табы
st.components.v1.html(tabs_html, height=100)

# Обработка выбора таба через session_state
tab_input = st.text_input("", key="tab_selector", label_visibility="collapsed")
if tab_input in ["tab1", "tab2", "tab3", "tab4", "tab5", "tab6"]:
    st.session_state.active_tab = tab_input
    st.rerun()

# Контент активного таба
st.markdown('<div class="tab-content">', unsafe_allow_html=True)

if st.session_state.active_tab == "tab1":
    st.header("Дашборд")
    col1, col2, col3 = st.columns(3)
    with col1: st.metric("Продажи", "₽123,456", "+12%")
    with col2: st.metric("Посетители", "2,345", "+8%")
    with col3: st.metric("Конверсия", "4.2%", "+0.5%")
    
elif st.session_state.active_tab == "tab2":
    st.header("Аналитика")
    import pandas as pd
    import numpy as np
    data = pd.DataFrame(np.random.randn(20, 3), columns=['A', 'B', 'C'])
    st.line_chart(data)
    
elif st.session_state.active_tab == "tab3":
    st.header("Пользователи")
    st.text_input("Поиск пользователей", key="user_search")
    # ... больше контента ...

st.markdown('</div>', unsafe_allow_html=True)

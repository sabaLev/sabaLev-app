import streamlit as st

st.markdown("""
<style>
/* Контейнер с горизонтальным скроллом */
.horizontal-scroll-container {
    min-width: 1000px;  /* Фиксированная минимальная ширина */
    overflow-x: auto;   /* Горизонтальный скролл */
    padding: 20px;
    background: #f8f9fa;
    border-radius: 10px;
    margin: 10px 0;
}

/* Для мобильных - включаем скролл */
@media (max-width: 640px) {
    .horizontal-scroll-container {
        min-width: 800px;
        overflow-x: scroll;
        -webkit-overflow-scrolling: touch; /* Плавный скролл на iOS */
    }
    
    /* Подсказка пользователю */
    .scroll-hint {
        display: block;
        text-align: center;
        color: #666;
        font-style: italic;
        margin: 10px 0;
    }
}

/* Широкие элементы внутри контейнера */
.wide-content {
    display: flex;
    gap: 20px;
    min-width: 900px;
}

.wide-column {
    min-width: 280px;
    background: white;
    padding: 15px;
    border-radius: 8px;
    border: 1px solid #ddd;
}
</style>
""", unsafe_allow_html=True)

st.title("📊 Панель управления с горизонтальным скроллом")

# Подсказка для мобильных пользователей
st.markdown(
    '<p class="scroll-hint">📱 На мобильных: проведите пальцем вправо/влево для прокрутки</p>', 
    unsafe_allow_html=True
)

# Контейнер с горизонтальным скроллом
with st.container():
    st.markdown('<div class="horizontal-scroll-container">', unsafe_allow_html=True)
    
    # Широкий макет из 3 колонок
    st.markdown('<div class="wide-content">', unsafe_allow_html=True)
    
    # Колонка 1
    st.markdown('<div class="wide-column">', unsafe_allow_html=True)
    st.header("📈 Аналитика")
    st.metric("Конверсия", "24%", "+3%")
    st.metric("Доход", "₽245,678", "+12%")
    st.metric("Посетители", "1,234", "+23")
    st.markdown('</div>')
    
    # Колонка 2  
    st.markdown('<div class="wide-column">', unsafe_allow_html=True)
    st.header("⚙️ Настройки")
    st.slider("Целевая температура", 0, 100, 25, key="temp_setting")
    st.selectbox("Режим работы", ["Авто", "Ручной", "Расписание"], key="mode")
    st.checkbox("Уведомления", key="notifications")
    st.checkbox("Автосохранение", key="autosave")
    st.markdown('</div>')
    
    # Колонка 3
    st.markdown('<div class="wide-column">', unsafe_allow_html=True)
    st.header("👥 Пользователи")
    st.text_input("Имя пользователя", key="username")
    st.text_input("Email", key="email", type="default")
    st.selectbox("Роль", ["Админ", "Редактор", "Зритель"], key="role")
    st.button("Сохранить", key="save_user")
    st.markdown('</div>')
    
    # Колонка 4
    st.markdown('<div class="wide-column">', unsafe_allow_html=True)
    st.header("📊 Графики")
    
    import pandas as pd
    import numpy as np
    
    chart_data = pd.DataFrame({
        'Месяц': ['Янв', 'Фев', 'Мар', 'Апр', 'Май', 'Июн'],
        'Продажи': [100, 200, 150, 300, 250, 400],
        'Затраты': [50, 80, 60, 120, 100, 150]
    })
    
    st.bar_chart(chart_data.set_index('Месяц'))
    st.markdown('</div>')
    
    st.markdown('</div>')  # закрываем wide-content
    st.markdown('</div>')  # закрываем horizontal-scroll-container

# Контент вне скролла (всегда видимый)
st.divider()
st.write("**Эта часть всегда видна без скролла:**")
important_info = st.text_area("Важные заметки:", height=100)
if st.button("Сохранить заметки"):
    st.success("Заметки сохранены!")

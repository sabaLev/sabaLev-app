import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(layout="wide")

st.markdown("""
<style>
/* Основной контейнер приложения */
.stApp {
    min-width: 1200px !important;
    overflow-x: auto !important;
}

/* Для мобильных устройств */
@media (max-width: 640px) {
    .stApp {
        min-width: 1000px !important;
        overflow-x: scroll !important;
    }
    
    /* Улучшаем скролл на touch-устройствах */
    .stApp::-webkit-scrollbar {
        height: 8px;
    }
    
    .stApp::-webkit-scrollbar-track {
        background: #f1f1f1;
    }
    
    .stApp::-webkit-scrollbar-thumb {
        background: #888;
        border-radius: 4px;
    }
    
    /* Индикатор скролла */
    .scroll-indicator {
        position: fixed;
        bottom: 10px;
        left: 50%;
        transform: translateX(-50%);
        background: rgba(0,0,0,0.7);
        color: white;
        padding: 5px 15px;
        border-radius: 20px;
        font-size: 12px;
        z-index: 1000;
    }
}

/* Контейнер для широкого контента */
.wide-dashboard {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 20px;
    min-width: 1000px;
    padding: 20px;
}

.dashboard-card {
    background: white;
    border: 1px solid #e0e0e0;
    border-radius: 10px;
    padding: 20px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

/* Широкая таблица */
.wide-table {
    min-width: 800px;
    overflow-x: auto;
    margin: 20px 0;
}
</style>
""", unsafe_allow_html=True)

# Индикатор для мобильных
st.markdown(
    '<div class="scroll-indicator">↔️ Проведите для прокрутки</div>',
    unsafe_allow_html=True
)

st.title("📱 Адаптивный дашборд с горизонтальным скроллом")

# Широкий контейнер с карточками
st.markdown('<div class="wide-dashboard">', unsafe_allow_html=True)

# Карточка 1
st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
st.subheader("📊 Продажи")
sales_data = pd.DataFrame({
    'День': ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс'],
    'Сумма': [12000, 15000, 18000, 22000, 25000, 14000, 9000]
})
st.bar_chart(sales_data.set_index('День'))
st.markdown('</div>')

# Карточка 2
st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
st.subheader("👥 Пользователи")
st.metric("Активные", "1,234", "+23")
st.metric("Новые", "89", "+12")
st.metric("Конверсия", "4.2%", "+0.5%")
st.markdown('</div>')

# Карточка 3
st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
st.subheader("📈 Тренды")
trend_data = pd.DataFrame(np.random.randn(30, 1), columns=['Тренд'])
st.line_chart(trend_data)
st.markdown('</div>')

# Карточка 4
st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
st.subheader("⚙️ Настройки")
st.checkbox("Уведомления по email", value=True)
st.checkbox("SMS-уведомления")
st.slider("Частота отчетов", 1, 24, 4)
st.button("Сохранить настройки")
st.markdown('</div>')

st.markdown('</div>')  # закрываем wide-dashboard

# Широкая таблица
st.subheader("📋 Детальные данные")
st.markdown('<div class="wide-table">', unsafe_allow_html=True)

# Создаем широкую таблицу
columns = [f"Показатель {i}" for i in range(1, 9)] + ["Сумма", "Изменение"]
data = []
for i in range(10):
    row = list(np.random.randn(8) * 1000) + [np.random.randint(1000, 10000), f"+{np.random.randint(1, 20)}%"]
    data.append(row)

df = pd.DataFrame(data, columns=columns)
st.dataframe(df, use_container_width=False, width=1200)

st.markdown('</div>')

# Фиксированные элементы (без скролла)
st.divider()
with st.expander("💡 Подсказки по использованию"):
    st.write("""
    - На мобильных устройствах используйте горизонтальную прокрутку
    - На компьютере весь контент отображается полностью
    - Все элементы остаются функциональными при любом размере экрана
    """)

import streamlit as st

# CSS для горизонтального скролла
st.markdown("""
<style>
/* Для всего приложения */
.stApp {
    min-width: 1000px !important;  /* Минимальная ширина */
    overflow-x: auto !important;   /* Горизонтальный скролл */
}

/* Убираем вертикальный скролл для маленьких экранов */
@media (max-width: 640px) {
    .stApp {
        min-width: 1000px !important;
        overflow-x: scroll !important;
        overflow-y: hidden !important;
    }
    
    /* Делаем элементы не сжимаемыми */
    .main-content > div {
        min-width: 300px !important;
    }
}
</style>
""", unsafe_allow_html=True)

# Создаем широкий контент
st.title("📱 Адаптивная страница с горизонтальным скроллом")

# Создаем широкую панель с колонками
wide_container = st.container()

with wide_container:
    # Широкий макет (шире 640px)
    cols = st.columns(4)  # 4 колонки для широкого экрана
    
    for i, col in enumerate(cols, 1):
        with col:
            st.header(f"Колонка {i}")
            st.text_input(f"Ввод {i}", key=f"input_{i}")
            st.slider(f"Слайдер {i}", 0, 100, 50, key=f"slider_{i}")
            st.button(f"Кнопка {i}", key=f"btn_{i}")
    
    # Еще один широкий элемент
    st.subheader("Широкая таблица")
    import pandas as pd
    import numpy as np
    
    # Создаем широкую таблицу
    wide_data = pd.DataFrame(
        np.random.randn(5, 8),
        columns=[f'Колонка {i+1}' for i in range(8)]
    )
    st.dataframe(wide_data, use_container_width=False, width=1200)

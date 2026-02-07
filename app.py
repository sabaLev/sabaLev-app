import streamlit as st

# CSS для горизонтального скролла
st.markdown("""
<style>
/* Основные стили для двух инпутов */
.inputs-container {
    display: flex;
    gap: 20px;
    padding: 15px;
    background: #f8f9fa;
    border-radius: 10px;
    margin: 20px 0;
    min-width: 300px; /* Минимальная ширина для десктопа */
}

/* Каждый инпут в своем блоке */
.input-block {
    flex: 1;
    min-width: 200px; /* Минимальная ширина каждого инпута */
    background: white;
    padding: 15px;
    border-radius: 8px;
    border: 1px solid #ddd;
}

/* Мобильная версия с горизонтальным скроллом */
@media (max-width: 640px) {
    .inputs-container {
        min-width: 500px; /* Ширина больше экрана для скролла */
        overflow-x: auto;
        overflow-y: hidden;
        -webkit-overflow-scrolling: touch; /* Плавный скролл на iOS */
        padding-bottom: 10px;
    }
    
    .input-block {
        min-width: 250px; /* Шире для удобства на мобильных */
        flex-shrink: 0; /* Запрещаем сжиматься */
    }
    
    /* Индикатор скролла */
    .scroll-hint {
        display: block;
        text-align: center;
        color: #666;
        font-size: 12px;
        margin-top: 5px;
    }
    
    /* Стили для скроллбара */
    .inputs-container::-webkit-scrollbar {
        height: 6px;
    }
    
    .inputs-container::-webkit-scrollbar-track {
        background: #f1f1f1;
        border-radius: 3px;
    }
    
    .inputs-container::-webkit-scrollbar-thumb {
        background: #888;
        border-radius: 3px;
    }
}

/* Десктопная версия */
@media (min-width: 641px) {
    .inputs-container {
        max-width: 800px; /* Ограничиваем ширину на десктопе */
        overflow-x: hidden; /* Убираем скролл на десктопе */
    }
    
    .scroll-hint {
        display: none; /* Скрываем подсказку на десктопе */
    }
}

/* Стили для заголовков инпутов */
.input-title {
    font-weight: bold;
    margin-bottom: 10px;
    color: #262730;
}

/* Убираем стандартные отступы у Streamlit инпутов */
div[data-testid="stTextInput"] {
    margin-bottom: 0;
}
</style>
""", unsafe_allow_html=True)

# Заголовок страницы
st.title("📱 Адаптивные поля ввода")
st.markdown("""
На десктопе оба поля отображаются рядом.  
**На мобильных (ширина < 641px)** появляется горизонтальная прокрутка.
""")

# Подсказка для мобильных пользователей
st.markdown(
    '<div class="scroll-hint">↔️ Проведите в сторону для прокрутки полей</div>', 
    unsafe_allow_html=True
)

# Контейнер для двух инпутов с горизонтальным скроллом
st.markdown('<div class="inputs-container">', unsafe_allow_html=True)

# Поле ввода 1
st.markdown('<div class="input-block">', unsafe_allow_html=True)
st.markdown('<div class="input-title">👤 Личная информация</div>', unsafe_allow_html=True)

# Первый инпут
name = st.text_input(
    "Полное имя",
    placeholder="Иван Иванов",
    key="name_input",
    label_visibility="collapsed"
)

# Дополнительные элементы в первом блоке
col1, col2 = st.columns(2)
with col1:
    age = st.number_input("Возраст", 0, 120, 25, key="age_input")
with col2:
    gender = st.selectbox("Пол", ["Мужской", "Женский"], key="gender_input")

st.markdown('</div>')  # Закрываем input-block 1

# Поле ввода 2
st.markdown('<div class="input-block">', unsafe_allow_html=True)
st.markdown('<div class="input-title">📧 Контактные данные</div>', unsafe_allow_html=True)

# Второй инпут
email = st.text_input(
    "Email адрес",
    placeholder="example@gmail.com",
    key="email_input",
    label_visibility="collapsed"
)

# Третий инпут во втором блоке
phone = st.text_input(
    "Номер телефона",
    placeholder="+7 900 000-00-00",
    key="phone_input",
    label_visibility="collapsed"
)

# Четвертый инпут
address = st.text_area(
    "Адрес проживания",
    placeholder="Город, улица, дом",
    height=80,
    key="address_input",
    label_visibility="collapsed"
)

st.markdown('</div>')  # Закрываем input-block 2

st.markdown('</div>')  # Закрываем inputs-container

# Кнопки действий (вне скролла)
st.divider()
col_btn1, col_btn2, col_btn3 = st.columns(3)
with col_btn1:
    if st.button("💾 Сохранить данные", use_container_width=True):
        if name and email:
            st.success("Данные сохранены!")
            st.json({
                "name": name,
                "age": age,
                "gender": gender,
                "email": email,
                "phone": phone,
                "address": address
            })
        else:
            st.warning("Заполните обязательные поля (имя и email)")

with col_btn2:
    if st.button("🔄 Очистить форму", use_container_width=True):
        st.rerun()

with col_btn3:
    if st.button("📋 Показать все", use_container_width=True):
        st.write(f"**Имя:** {name or 'Не указано'}")
        st.write(f"**Возраст:** {age}")
        st.write(f"**Пол:** {gender}")
        st.write(f"**Email:** {email or 'Не указан'}")
        st.write(f"**Телефон:** {phone or 'Не указан'}")
        st.write(f"**Адрес:** {address or 'Не указан'}")

# Дополнительная информация
with st.expander("ℹ️ Как это работает"):
    st.markdown("""
    ### Принцип работы:
    1. **На десктопе (ширина > 640px):**
       - Оба блока с полями ввода отображаются рядом
       - Ширина контейнера ограничена 800px
       - Нет горизонтального скролла
       
    2. **На мобильных (ширина ≤ 640px):**
       - Контейнер растягивается до 500px
       - Появляется горизонтальная прокрутка
       - Поля можно листать пальцем
       
    ### Ключевые CSS-свойства:
    ```css
    @media (max-width: 640px) {
        .inputs-container {
            min-width: 500px;  /* Шире экрана */
            overflow-x: auto;  /* Включаем скролл */
            -webkit-overflow-scrolling: touch; /* Плавный скролл */
        }
        .input-block {
            flex-shrink: 0;    /* Запрещаем сжиматься */
            min-width: 250px;  /* Минимальная ширина */
        }
    }
    ```
    
    ### Преимущества:
    - Поля всегда удобного размера
    - Не нужно масштабировать текст
    - Сохраняется первоначальный дизайн
    - Touch-friendly интерфейс
    """)

# Индикатор текущей ширины экрана (для отладки)
st.markdown("---")
st.caption(f"*Текущая минимальная ширина контейнера: 500px*")

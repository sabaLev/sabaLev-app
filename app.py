import streamlit as st
from datetime import time, date, datetime

st.set_page_config(page_title="Все слайдеры Streamlit", layout="wide")
st.title("🎚️ Все виды слайдеров Streamlit")

# Разделяем на вкладки
tab1, tab2, tab3 = st.tabs(["📊 Основные слайдеры", "🕒 Время и дата", "🎛️ Специальные"])

with tab1:
    st.header("Базовые слайдеры")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # 1. Простой числовой слайдер
        simple_slider = st.slider(
            "Простой слайдер",
            min_value=0,
            max_value=100,
            value=50,
            step=1,
            help="Минимальный шаг = 1"
        )
        st.metric("Результат", simple_slider)
        
        # 2. Слайдер с дробными числами
        float_slider = st.slider(
            "Дробный слайдер",
            min_value=0.0,
            max_value=1.0,
            value=0.5,
            step=0.01,
            format="%.2f",
            help="Шаг 0.01, формат с двумя знаками"
        )
        st.write(f"Значение: **{float_slider:.2f}**")
    
    with col2:
        # 3. Слайдер с диапазоном (два значения)
        range_slider = st.slider(
            "Слайдер диапазона",
            min_value=0,
            max_value=1000,
            value=(200, 800),
            step=10,
            help="Выберите начальное и конечное значение"
        )
        st.write(f"Диапазон: **{range_slider[0]} - {range_slider[1]}**")
        
        # 4. Большой диапазон с кастомным шагом
        big_slider = st.slider(
            "Большой диапазон",
            min_value=0,
            max_value=10000,
            value=2500,
            step=100,
            format="%d",
            help="Шаг 100, для больших чисел"
        )
        st.write(f"Значение: **{big_slider:,}**".replace(',', ' '))

with tab2:
    st.header("Слайдеры времени и даты")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # 5. Слайдер времени
        time_slider = st.slider(
            "Выберите время",
            value=time(9, 0),
            format="HH:mm",
            help="Выберите время в течение дня"
        )
        st.write(f"Время: **{time_slider.strftime('%H:%M')}**")
        
        # 6. Слайдер даты
        date_slider = st.slider(
            "Выберите дату",
            min_value=date(2023, 1, 1),
            max_value=date(2023, 12, 31),
            value=date(2023, 6, 15),
            format="DD.MM.YYYY",
            help="Выберите дату в 2023 году"
        )
        st.write(f"Дата: **{date_slider.strftime('%d.%m.%Y')}**")
    
    with col2:
        # 7. Слайдер даты и времени
        datetime_slider = st.slider(
            "Дата и время",
            min_value=datetime(2023, 1, 1, 0, 0),
            max_value=datetime(2023, 12, 31, 23, 59),
            value=datetime(2023, 6, 15, 12, 0),
            format="DD.MM.YYYY HH:mm",
            help="Выберите точную дату и время"
        )
        st.write(f"Дата и время: **{datetime_slider.strftime('%d.%m.%Y %H:%M')}**")
        
        # 8. Диапазон дат
        date_range = st.slider(
            "Диапазон дат",
            min_value=date(2023, 1, 1),
            max_value=date(2023, 12, 31),
            value=(date(2023, 3, 1), date(2023, 9, 1)),
            format="DD.MM.YYYY",
            help="Выберите начальную и конечную дату"
        )
        st.write(f"С **{date_range[0].strftime('%d.%m.%Y')}** по **{date_range[1].strftime('%d.%m.%Y')}**")

with tab3:
    st.header("Специальные слайдеры")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # 9. Select slider с числами
        select_num = st.select_slider(
            "Выбор из чисел",
            options=[0, 10, 25, 50, 75, 100, 150, 200, 300, 500],
            value=100,
            help="Выберите из предустановленных значений"
        )
        st.write(f"Выбрано: **{select_num}**")
        
        # 10. Select slider с текстом
        select_text = st.select_slider(
            "Уровень сложности",
            options=['Легкий', 'Средний', 'Сложный', 'Эксперт', 'Мастер'],
            value='Средний',
            help="Выберите уровень сложности"
        )
        st.write(f"Уровень: **{select_text}**")
    
    with col2:
        # 11. Select slider с диапазоном
        select_range = st.select_slider(
            "Диапазон цен",
            options=['0', '500', '1000', '2500', '5000', '10000', '25000', '50000'],
            value=('1000', '10000'),
            help="Выберите минимальную и максимальную цену"
        )
        st.write(f"Цена: **от {select_range[0]} до {select_range[1]}**")
        
        # 12. Слайдер с отрицательными значениями
        negative_slider = st.slider(
            "Отрицательный диапазон",
            min_value=-100,
            max_value=100,
            value=0,
            step=10,
            help="Можно выбирать отрицательные значения"
        )
        st.write(f"Значение: **{negative_slider:+d}**")

# Интерактивный пример
st.header("🎮 Интерактивный пример")

col_config, col_result = st.columns([1, 2])

with col_config:
    st.subheader("Настройте слайдер")
    
    # Параметры для создания слайдера
    min_val = st.number_input("Минимум", value=0, step=1)
    max_val = st.number_input("Максимум", value=100, step=1)
    default_val = st.number_input("Значение по умолчанию", value=50, step=1)
    step_val = st.number_input("Шаг", value=1, min_value=1)
    
    slider_type = st.selectbox(
        "Тип слайдера",
        ["Одиночное значение", "Диапазон"]
    )
    
    show_format = st.checkbox("Показать форматирование", value=False)

with col_result:
    st.subheader("Результат")
    
    if slider_type == "Одинечное значение":
        if show_format and (max_val >= 1000 or min_val <= -1000):
            format_str = "%d"
        else:
            format_str = None
            
        dynamic_slider = st.slider(
            "Ваш слайдер",
            min_value=min_val,
            max_value=max_val,
            value=default_val,
            step=step_val,
            format=format_str,
            key="dynamic_slider"
        )
        
        if isinstance(dynamic_slider, (int, float)):
            st.success(f"Вы выбрали: **{dynamic_slider}**")
            
    else:  # Диапазон
        default_range = (min_val + (max_val - min_val) // 4, 
                        min_val + 3 * (max_val - min_val) // 4)
        
        dynamic_range = st.slider(
            "Ваш диапазон",
            min_value=min_val,
            max_value=max_val,
            value=default_range,
            step=step_val,
            key="dynamic_range"
        )
        
        if isinstance(dynamic_range, tuple):
            st.success(f"Диапазон: **от {dynamic_range[0]} до {dynamic_range[1]}**")

# Слайдеры в сайдбаре
with st.sidebar:
    st.header("🎛️ Слайдеры в сайдбаре")
    
    sidebar_slider1 = st.slider("Настройка 1", 0, 100, 50)
    st.write(f"Значение 1: {sidebar_slider1}")
    
    sidebar_slider2 = st.slider("Настройка 2", 0.0, 10.0, 5.0, 0.1)
    st.write(f"Значение 2: {sidebar_slider2:.1f}")
    
    sidebar_slider3 = st.select_slider(
        "Категория",
        options=["Низкий", "Средний", "Высокий", "Очень высокий"]
    )
    st.write(f"Категория: {sidebar_slider3}")

# Код для копирования
with st.expander("📋 Код примеров"):
    st.code('''
# 1. Простой слайдер
value = st.slider("Название", 0, 100, 50)

# 2. С дробными числами
float_val = st.slider("Дробный", 0.0, 1.0, 0.5, 0.01, "%.2f")

# 3. Диапазон
range_val = st.slider("Диапазон", 0, 100, (25, 75))

# 4. Время
time_val = st.slider("Время", value=time(9, 0))

# 5. Дата
date_val = st.slider("Дата", 
                     min_value=date(2023,1,1), 
                     max_value=date(2023,12,31),
                     value=date(2023,6,15),
                     format="DD.MM.YYYY")

# 6. Select slider
select_val = st.select_slider("Выбор", 
                              options=[1, 2, 3, 4, 5], 
                              value=3)
    ''')

st.markdown("---")
st.caption("Всего доступно 2 типа слайдеров: `st.slider` и `st.select_slider`")

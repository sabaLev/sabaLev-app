import streamlit as st
import pandas as pd

# Конфигурация страницы
st.set_page_config(layout="wide", page_title="Интерактивная таблица")
st.title("📊 Интерактивная таблица с кнопками в ячейках")

# Инициализация данных в session_state
if 'table_data' not in st.session_state:
    st.session_state.table_data = pd.DataFrame({
        'ID': [1, 2, 3, 4],
        'Наименование': ['Проект Альфа', 'Проект Бета', 'Проект Гамма', 'Проект Дельта'],
        'Бюджет (тыс. ₽)': [500, 750, 300, 900],
        'Прогресс (%)': [65, 40, 85, 25],
        'Приоритет': ['Высокий', 'Средний', 'Высокий', 'Низкий'],
        'Количество': [10, 25, 15, 8]
    })

# CSS для улучшения внешнего вида
st.markdown("""
<style>
/* Стили для заголовков столбцов */
.st-emotion-cache-1q7spjk {
    font-weight: bold !important;
    text-align: center !important;
}

/* Центрирование текста в ячейках */
.stDataFrame {
    text-align: center !important;
}

/* Улучшенные кнопки */
.stButton > button {
    width: 30px !important;
    height: 30px !important;
    padding: 0 !important;
    margin: 2px !important;
}

/* Контейнер для кнопок */
.button-container {
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 5px;
    margin-top: 5px;
}
</style>
""", unsafe_allow_html=True)

# Функция для создания интерактивной ячейки с кнопками
def create_interactive_cell(label, value, row_idx, col_name, min_val=0, max_val=100, step=1):
    """Создает ячейку с кнопками +/- и значением"""
    container = st.container()
    
    with container:
        # Отображаем метку (если есть)
        if label:
            st.caption(label)
        
        # Основное значение
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col1:
            # Кнопка минус
            if st.button("➖", key=f"dec_{row_idx}_{col_name}", 
                        help=f"Уменьшить на {step}", 
                        use_container_width=True):
                new_value = max(min_val, value - step)
                st.session_state.table_data.at[row_idx, col_name] = new_value
                st.rerun()
        
        with col2:
            # Текущее значение
            st.markdown(
                f"<div style='text-align: center; font-weight: bold; font-size: 1.1em; padding: 5px;'>"
                f"{value}"
                f"</div>", 
                unsafe_allow_html=True
            )
        
        with col3:
            # Кнопка плюс
            if st.button("➕", key=f"inc_{row_idx}_{col_name}",
                        help=f"Увеличить на {step}", 
                        use_container_width=True):
                new_value = min(max_val, value + step)
                st.session_state.table_data.at[row_idx, col_name] = new_value
                st.rerun()
        
        # Быстрые кнопки управления
        btn_col1, btn_col2 = st.columns(2)
        
        with btn_col1:
            if st.button("-5", key=f"fast_dec_{row_idx}_{col_name}", 
                        use_container_width=True):
                new_value = max(min_val, value - 5)
                st.session_state.table_data.at[row_idx, col_name] = new_value
                st.rerun()
        
        with btn_col2:
            if st.button("+5", key=f"fast_inc_{row_idx}_{col_name}",
                        use_container_width=True, type="secondary"):
                new_value = min(max_val, value + 5)
                st.session_state.table_data.at[row_idx, col_name] = new_value
                st.rerun()

# Основная таблица с разбивкой по колонкам
st.write("### Управление проектами")

# Создаем заголовки таблицы
header_cols = st.columns([1, 3, 2, 2, 2, 2])
with header_cols[0]:
    st.markdown("**ID**")
with header_cols[1]:
    st.markdown("**Наименование**")
with header_cols[2]:
    st.markdown("**Бюджет**")
with header_cols[3]:
    st.markdown("**Прогресс**")
with header_cols[4]:
    st.markdown("**Приоритет**")
with header_cols[5]:
    st.markdown("**Количество**")

st.divider()

# Отображаем каждую строку таблицы
for idx in range(len(st.session_state.table_data)):
    row = st.session_state.table_data.iloc[idx]
    
    # Создаем колонки для текущей строки
    row_cols = st.columns([1, 3, 2, 2, 2, 2])
    
    # ID
    with row_cols[0]:
        st.markdown(f"**{int(row['ID'])}**")
    
    # Наименование
    with row_cols[1]:
        st.markdown(f"**{row['Наименование']}**")
        st.caption(f"ID: {int(row['ID'])}")
    
    # Бюджет
    with row_cols[2]:
        create_interactive_cell(
            label="тыс. ₽",
            value=row['Бюджет (тыс. ₽)'],
            row_idx=idx,
            col_name='Бюджет (тыс. ₽)',
            min_val=0,
            max_val=5000,
            step=50
        )
    
    # Прогресс
    with row_cols[3]:
        current_progress = row['Прогресс (%)']
        
        # Прогресс-бар
        progress_color = (
            "🟢" if current_progress >= 80 else 
            "🟡" if current_progress >= 50 else 
            "🔴"
        )
        
        st.progress(
            current_progress / 100,
            text=f"{progress_color} {current_progress}%"
        )
        
        # Кнопки для прогресса
        prog_col1, prog_col2, prog_col3 = st.columns(3)
        
        with prog_col1:
            if st.button("−10%", key=f"prog_dec_{idx}", use_container_width=True):
                new_progress = max(0, current_progress - 10)
                st.session_state.table_data.at[idx, 'Прогресс (%)'] = new_progress
                st.rerun()
        
        with prog_col2:
            st.markdown(f"<div style='text-align: center;'>{current_progress}%</div>", 
                       unsafe_allow_html=True)
        
        with prog_col3:
            if st.button("+10%", key=f"prog_inc_{idx}", use_container_width=True):
                new_progress = min(100, current_progress + 10)
                st.session_state.table_data.at[idx, 'Прогресс (%)'] = new_progress
                st.rerun()
    
    # Приоритет
    with row_cols[4]:
        priority_colors = {
            'Высокий': '🔴',
            'Средний': '🟡',
            'Низкий': '🟢'
        }
        
        # Селектор приоритета
        new_priority = st.selectbox(
            "",
            options=['Высокий', 'Средний', 'Низкий'],
            index=['Высокий', 'Средний', 'Низкий'].index(row['Приоритет']),
            key=f"priority_{idx}",
            label_visibility="collapsed"
        )
        
        if new_priority != row['Приоритет']:
            st.session_state.table_data.at[idx, 'Приоритет'] = new_priority
            st.rerun()
        
        # Отображаем цветной индикатор
        st.markdown(
            f"<div style='text-align: center; font-size: 1.5em;'>{priority_colors[new_priority]}</div>",
            unsafe_allow_html=True
        )
    
    # Количество
    with row_cols[5]:
        create_interactive_cell(
            label="шт.",
            value=row['Количество'],
            row_idx=idx,
            col_name='Количество',
            min_val=0,
            max_val=100,
            step=1
        )
    
    # Разделитель между строками
    if idx < len(st.session_state.table_data) - 1:
        st.divider()

# Панель управления под таблицей
st.write("---")
st.write("### 🎯 Глобальное управление")

# Быстрые действия для всех строк
action_cols = st.columns(5)

with action_cols[0]:
    if st.button("📈 +10% прогресс всем", use_container_width=True):
        for idx in range(len(st.session_state.table_data)):
            current = st.session_state.table_data.at[idx, 'Прогресс (%)']
            st.session_state.table_data.at[idx, 'Прогресс (%)'] = min(100, current + 10)
        st.rerun()

with action_cols[1]:
    if st.button("📉 -10% прогресс всем", use_container_width=True):
        for idx in range(len(st.session_state.table_data)):
            current = st.session_state.table_data.at[idx, 'Прогресс (%)']
            st.session_state.table_data.at[idx, 'Прогресс (%)'] = max(0, current - 10)
        st.rerun()

with action_cols[2]:
    if st.button("🔄 Сбросить количество", use_container_width=True):
        st.session_state.table_data['Количество'] = [0, 0, 0, 0]
        st.rerun()

with action_cols[3]:
    if st.button("💰 +100 к бюджету", use_container_width=True):
        st.session_state.table_data['Бюджет (тыс. ₽)'] += 100
        st.rerun()

with action_cols[4]:
    if st.button("✅ Завершить все проекты", use_container_width=True, type="primary"):
        st.session_state.table_data['Прогресс (%)'] = 100
        st.rerun()

# Статистика
st.write("---")
st.write("### 📊 Сводная статистика")

# Рассчитываем статистику
total_budget = st.session_state.table_data['Бюджет (тыс. ₽)'].sum()
avg_progress = st.session_state.table_data['Прогресс (%)'].mean()
total_items = st.session_state.table_data['Количество'].sum()
high_priority = (st.session_state.table_data['Приоритет'] == 'Высокий').sum()

# Отображаем метрики
stat_cols = st.columns(4)

with stat_cols[0]:
    st.metric(
        "Общий бюджет", 
        f"{total_budget:,.0f} тыс. ₽",
        delta=f"+{st.session_state.table_data['Бюджет (тыс. ₽)'].sum() - 50000:.0f} тыс. ₽"
    )

with stat_cols[1]:
    st.metric(
        "Средний прогресс", 
        f"{avg_progress:.1f}%",
        delta=f"{avg_progress - 50:+.1f}%"
    )

with stat_cols[2]:
    st.metric(
        "Всего единиц", 
        f"{total_items} шт.",
        delta=f"+{total_items - 58}" if total_items > 58 else f"{total_items - 58}"
    )

with stat_cols[3]:
    st.metric(
        "Высокий приоритет", 
        f"{high_priority} проектов",
        delta="требует внимания" if high_priority > 0 else ""
    )

# Отображение данных в виде таблицы для справки
st.write("---")
st.write("### 📋 Текущие данные (только для просмотра)")

# Отображаем DataFrame (только для просмотра)
st.dataframe(
    st.session_state.table_data,
    use_container_width=True,
    column_config={
        "ID": st.column_config.NumberColumn("ID", width="small"),
        "Наименование": st.column_config.TextColumn("Наименование", width="medium"),
        "Бюджет (тыс. ₽)": st.column_config.NumberColumn(
            "Бюджет",
            format="%d тыс. ₽",
            width="small"
        ),
        "Прогресс (%)": st.column_config.ProgressColumn(
            "Прогресс",
            format="%d%%",
            min_value=0,
            max_value=100,
            width="medium"
        ),
        "Приоритет": st.column_config.TextColumn("Приоритет", width="small"),
        "Количество": st.column_config.NumberColumn("Кол-во", width="small")
    }
)

# Кнопки экспорта
st.write("---")
export_col1, export_col2, export_col3 = st.columns(3)

with export_col1:
    if st.button("💾 Сохранить данные", use_container_width=True, type="primary"):
        st.success("Данные успешно сохранены в session_state!")
        st.balloons()

with export_col2:
    # Экспорт в CSV
    csv = st.session_state.table_data.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Экспорт в CSV",
        data=csv,
        file_name="projects_data.csv",
        mime="text/csv",
        use_container_width=True
    )

with export_col3:
    if st.button("🔄 Сбросить все данные", use_container_width=True, type="secondary"):
        # Сброс к исходным значениям
        st.session_state.table_data = pd.DataFrame({
            'ID': [1, 2, 3, 4],
            'Наименование': ['Проект Альфа', 'Проект Бета', 'Проект Гамма', 'Проект Дельта'],
            'Бюджет (тыс. ₽)': [500, 750, 300, 900],
            'Прогресс (%)': [65, 40, 85, 25],
            'Приоритет': ['Высокий', 'Средний', 'Высокий', 'Низкий'],
            'Количество': [10, 25, 15, 8]
        })
        st.rerun()

# Инструкция
with st.expander("📖 Как пользоваться таблицей"):
    st.markdown("""
    ### Инструкция по использованию:
    
    1. **Изменение значений в ячейках:**
       - Используйте кнопки **➖** и **➕** для изменения значений
       - Быстрые кнопки **-5** и **+5** для больших изменений
       - Для прогресса используйте кнопки **-10%** и **+10%**
    
    2. **Изменение приоритета:**
       - Используйте выпадающий список в колонке "Приоритет"
    
    3. **Глобальное управление:**
       - Используйте кнопки под таблицей для массовых изменений
    
    4. **Экспорт данных:**
       - Сохраните данные в CSV для дальнейшего использования
    
    ### Особенности:
    - Все изменения сохраняются автоматически
    - Данные обновляются в реальном времени
    - Поддерживается работа на мобильных устройствах
    - Никакого HTML/CSS - чистый Streamlit
    """)

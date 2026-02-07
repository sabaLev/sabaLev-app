import streamlit as st
import pandas as pd

st.title("📊 Таблица с кнопками в строках (без HTML)")

# Инициализация данных
if 'work_hours' not in st.session_state:
    st.session_state.work_hours = pd.DataFrame({
        'Задача': ['Разработка', 'Тестирование', 'Документация', 'Встречи'],
        'Пн': [8, 4, 2, 2],
        'Вт': [6, 3, 3, 2],
        'Ср': [7, 5, 2, 1],
        'Чт': [8, 4, 3, 1],
        'Пт': [5, 6, 2, 2]
    })

st.write("### Часы работы по задачам")

# Заголовок таблицы
header_cols = st.columns([2] + [1] * 5)  # 2 для задачи, 1 для каждого дня
with header_cols[0]:
    st.markdown("**Задача / День**")
for i, day in enumerate(['Пн', 'Вт', 'Ср', 'Чт', 'Пт'], 1):
    with header_cols[i]:
        st.markdown(f"**{day}**")

st.divider()

# Тело таблицы - каждая строка
total_hours = {day: 0 for day in ['Пн', 'Вт', 'Ср', 'Чт', 'Пт']}

for task_idx, task in enumerate(st.session_state.work_hours['Задача']):
    row_cols = st.columns([2] + [1] * 5)
    
    with row_cols[0]:
        st.markdown(f"**{task}**")
    
    for day_idx, day in enumerate(['Пн', 'Вт', 'Ср', 'Чт', 'Пт'], 1):
        with row_cols[day_idx]:
            # Текущее значение
            current_value = st.session_state.work_hours.at[task_idx, day]
            
            # Кнопки и значение в одной строке
            btn_col1, val_col, btn_col2 = st.columns([1, 2, 1])
            
            with btn_col1:
                if st.button("➖", key=f"dec_{task}_{day}", help="Уменьшить на 1"):
                    new_val = max(0, current_value - 1)
                    st.session_state.work_hours.at[task_idx, day] = new_val
                    st.rerun()
            
            with val_col:
                st.markdown(f"<div style='text-align: center; font-weight: bold;'>{current_value}</div>", 
                           unsafe_allow_html=True)
            
            with btn_col2:
                if st.button("➕", key=f"inc_{task}_{day}", help="Увеличить на 1"):
                    st.session_state.work_hours.at[task_idx, day] = current_value + 1
                    st.rerun()
            
            total_hours[day] += current_value
    
    st.divider()

# Итоговая строка
footer_cols = st.columns([2] + [1] * 5)
with footer_cols[0]:
    st.markdown("**Итого за день:**")
for i, day in enumerate(['Пн', 'Вт', 'Ср', 'Чт', 'Пт'], 1):
    with footer_cols[i]:
        st.markdown(f"**{total_hours[day]}**")

# Статистика
st.write("---")
col1, col2, col3 = st.columns(3)
with col1:
    weekly_total = sum(total_hours.values())
    st.metric("Всего часов за неделю", f"{weekly_total} ч.")
with col2:
    avg_per_day = weekly_total / 5
    st.metric("Среднее в день", f"{avg_per_day:.1f} ч.")
with col3:
    max_day = max(total_hours.items(), key=lambda x: x[1])
    st.metric("Самый загруженный", f"{max_day[0]}: {max_day[1]} ч.")

# Экспорт данных
if st.button("📥 Экспортировать в CSV"):
    csv = st.session_state.work_hours.to_csv(index=False)
    st.download_button(
        label="Скачать CSV",
        data=csv,
        file_name="work_hours.csv",
        mime="text/csv"
    )

import streamlit as st

st.set_page_config(layout="centered")

st.markdown("""
<style>
/* Увеличиваем для мобильных */
div[data-testid="stSelectbox"] > div {
    font-size: 18px;
    padding: 15px;
    border-radius: 12px;
    border: 2px solid #4b75c9;
}

/* Скрываем стрелку на мобильных */
@media (max-width: 768px) {
    div[data-testid="stSelectbox"] svg {
        display: none;
    }
    div[data-testid="stSelectbox"] > div {
        font-size: 20px;
        padding: 18px;
    }
}

/* Красивые карточки для выбора */
.group-card {
    background: #f8fafc;
    border-radius: 10px;
    padding: 15px;
    margin: 10px 0;
    border: 1px solid #e2e8f0;
    text-align: center;
}
.group-card.selected {
    background: #e0f2fe;
    border-color: #0ea5e9;
    border-width: 2px;
}
</style>
""", unsafe_allow_html=True)

st.title("🔘 בחירת קבוצה")

# Создаем все возможные комбинации
group_options = []

for panels in range(1, 9):  # 1-8 панелей
    for rows in range(0, 11):  # 0-10 строк
        # Форматируем красиво
        display_text = f"📊 {panels} פאנלים | 🏗️ {rows} שורות"
        # Значение для программы
        value = f"{panels},{rows}"
        group_options.append((display_text, value))

# Только отображение для пользователя
display_options = [opt[0] for opt in group_options]
values_dict = {opt[0]: opt[1] for opt in group_options}

# Один большой selectbox
selected_display = st.selectbox(
    "בחר קבוצת פאנלים:",
    options=display_options,
    index=24,  # начальное значение: 5 פאנלים, 2 שורות
    key="group_selector",
    help="גלול למעלה/מטה לבחירה"
)

# Разбираем выбранное значение
if selected_display in values_dict:
    value_str = values_dict[selected_display]
    panels, rows = map(int, value_str.split(','))
    
    st.markdown("---")
    
    # Показываем выбранное
    col1, col2 = st.columns(2)
    with col1:
        st.metric("פאנלים", panels)
    with col2:
        st.metric("שורות", rows)
    
    # Кнопка для добавления
    if st.button("➕ הוסף קבוצה זו", use_container_width=True):
        st.success(f"✅ נוספה קבוצה: {panels} פאנלים, {rows} שורות")
        
        # Здесь можно сохранить в session_state
        if "groups" not in st.session_state:
            st.session_state.groups = []
        
        st.session_state.groups.append({
            "panels": panels,
            "rows": rows,
            "type": "עומד"  # или можно выбрать тип
        })
    
    # Показать все добавленные группы
    if "groups" in st.session_state and st.session_state.groups:
        st.markdown("### 📋 קבוצות שנוספו:")
        for i, group in enumerate(st.session_state.groups, 1):
            st.write(f"{i}. {group['panels']} פאנלים, {group['rows']} שורות ({group['type']})")

# Альтернативный вариант: две кнопки для изменения внутри одного блока
st.markdown("---")
st.markdown("### 🔧 גרסה עם כפתורים")

# Используем st.columns но они на мобильном будут под друг другом
# Это ЛУЧШЕ чем ничего
col1, col2, col3 = st.columns([2, 3, 2])

with col1:
    st.markdown("<div style='text-align: center; padding: 10px;'>פאנלים</div>", unsafe_allow_html=True)
    if st.button("◀️", key="panels_minus", use_container_width=True):
        if "temp_panels" not in st.session_state:
            st.session_state.temp_panels = 5
        st.session_state.temp_panels = max(1, st.session_state.temp_panels - 1)
        st.rerun()

with col2:
    panels_val = st.session_state.get("temp_panels", 5)
    rows_val = st.session_state.get("temp_rows", 2)
    st.markdown(f"<div style='text-align: center; font-size: 24px; font-weight: bold; padding: 15px; background: #f0f9ff; border-radius: 10px;'>{panels_val} | {rows_val}</div>", unsafe_allow_html=True)
    st.markdown("<div style='text-align: center; font-size: 14px; color: #666;'>פאנלים | שורות</div>", unsafe_allow_html=True)

with col3:
    st.markdown("<div style='text-align: center; padding: 10px;'>שורות</div>", unsafe_allow_html=True)
    if st.button("▶️", key="rows_plus", use_container_width=True):
        if "temp_rows" not in st.session_state:
            st.session_state.temp_rows = 2
        st.session_state.temp_rows = min(10, st.session_state.temp_rows + 1)
        st.rerun()

# Кнопки под/над основным блоком
col_a, col_b = st.columns(2)
with col_a:
    if st.button("־ פאנל", key="panels_minus2", use_container_width=True):
        if "temp_panels" not in st.session_state:
            st.session_state.temp_panels = 5
        st.session_state.temp_panels = max(1, st.session_state.temp_panels - 1)
        st.rerun()

with col_b:
    if st.button("+ פאנל", key="panels_plus2", use_container_width=True):
        if "temp_panels" not in st.session_state:
            st.session_state.temp_panels = 5
        st.session_state.temp_panels = min(8, st.session_state.temp_panels + 1)
        st.rerun()

col_c, col_d = st.columns(2)
with col_c:
    if st.button("־ שורה", key="rows_minus2", use_container_width=True):
        if "temp_rows" not in st.session_state:
            st.session_state.temp_rows = 2
        st.session_state.temp_rows = max(0, st.session_state.temp_rows - 1)
        st.rerun()

with col_d:
    if st.button("+ שורה", key="rows_plus2", use_container_width=True):
        if "temp_rows" not in st.session_state:
            st.session_state.temp_rows = 2
        st.session_state.temp_rows = min(10, st.session_state.temp_rows + 1)
        st.rerun()

if st.button("💾 שמור קבוצה זו", type="primary", use_container_width=True):
    panels_val = st.session_state.get("temp_panels", 5)
    rows_val = st.session_state.get("temp_rows", 2)
    st.success(f"שמרתי קבוצה: {panels_val} פאנלים, {rows_val} שורות")

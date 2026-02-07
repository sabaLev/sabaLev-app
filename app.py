import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import math
import json

# ---------- ИНИЦИАЛИЗАЦИЯ SESSION STATE ----------
if "fasteners" not in st.session_state:
    st.session_state.fasteners = None
if "fasteners_include" not in st.session_state:
    st.session_state.fasteners_include = {}
if "vertical_rows" not in st.session_state:
    st.session_state.vertical_rows = 8
if "horizontal_rows" not in st.session_state:
    st.session_state.horizontal_rows = 4
if "calc_result" not in st.session_state:
    st.session_state.calc_result = None
if "just_calculated" not in st.session_state:
    st.session_state.just_calculated = False
if "channel_order" not in st.session_state:
    st.session_state.channel_order = {}
if "extra_parts" not in st.session_state:
    st.session_state.extra_parts = []
if "manual_rows" not in st.session_state:
    st.session_state.manual_rows = 1
if "manual_form_version" not in st.session_state:
    st.session_state.manual_form_version = 0
if "koshrot_boxes_version" not in st.session_state:
    st.session_state.koshrot_boxes_version = 0
if "manual_rails" not in st.session_state:
    st.session_state.manual_rails = {}
if "panel_name" not in st.session_state:
    st.session_state.panel_name = None
if "extra_rows" not in st.session_state:
    st.session_state.extra_rows = 1
if "project_name" not in st.session_state:
    st.session_state.project_name = ""
if "manual_deleted_rows" not in st.session_state:
    st.session_state.manual_deleted_rows = set()
if "koshrot_qty" not in st.session_state:
    st.session_state.koshrot_qty = {}
if "calculation_counter" not in st.session_state:
    st.session_state.calculation_counter = 0
if "initial_calc_result" not in st.session_state:
    st.session_state.initial_calc_result = None
if "initial_fasteners" not in st.session_state:
    st.session_state.initial_fasteners = None
if "initial_fasteners_include" not in st.session_state:
    st.session_state.initial_fasteners_include = {}
if "manual_rails_reset_version" not in st.session_state:
    st.session_state.manual_rails_reset_version = 0
if "report_needs_update" not in st.session_state:
    st.session_state.report_needs_update = True
if "previous_groups_hash" not in st.session_state:
    st.session_state.previous_groups_hash = None
if "show_add_dialog_vertical" not in st.session_state:
    st.session_state.show_add_dialog_vertical = False
if "show_add_dialog_horizontal" not in st.session_state:
    st.session_state.show_add_dialog_horizontal = False
if "new_panel_value_vertical" not in st.session_state:
    st.session_state.new_panel_value_vertical = 9
if "new_panel_value_horizontal" not in st.session_state:
    st.session_state.new_panel_value_horizontal = 5
if "delete_row_confirm" not in st.session_state:
    st.session_state.delete_row_confirm = None
if "vertical_panel_values" not in st.session_state:
    st.session_state.vertical_panel_values = list(range(1, 9))
if "horizontal_panel_values" not in st.session_state:
    st.session_state.horizontal_panel_values = list(range(1, 5))
if "vertical_group_values" not in st.session_state:
    st.session_state.vertical_group_values = [0] * 8
if "horizontal_group_values" not in st.session_state:
    st.session_state.horizontal_group_values = [0] * 4
if "vertical_custom_rows" not in st.session_state:
    st.session_state.vertical_custom_rows = []
if "horizontal_custom_rows" not in st.session_state:
    st.session_state.horizontal_custom_rows = []

# ---------- ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ ----------
def right_label(text: str) -> str:
    return f'<div style="text-align:right; font-weight:bold;">{text}</div>'

def right_header(text: str) -> str:
    return f'<h3 style="text-align:right; margin-bottom:0.5rem;">{text}</h3>'

def clean_text(text: str) -> str:
    return text.rstrip(" .…")

def info_box(text: str):
    text = clean_text(text)
    st.markdown(
        f"""
        <div style="
            background-color:#2b2b2b;
            color:white;
            padding:12px;
            border-radius:6px;
            text-align:right;
            border:1px solid #555;
        ">
            {text}
        </div>
        """,
        unsafe_allow_html=True,
    )

def success_box(text: str):
    text = clean_text(text)
    st.markdown(
        f"""
        <div style="
            background-color:#1f3d1f;
            color:white;
            padding:12px;
            border-radius:6px;
            text-align:right;
            border:1px solid #4caf50;
        ">
            {text}
        </div>
        """,
        unsafe_allow_html=True,
    )

def warning_box(text: str):
    text = clean_text(text)
    st.markdown(
        f"""
        <div style="
            background-color:#3d2b1f;
            color:white;
            padding:12px;
            border-radius:6px;
            text-align:right;
            border:1px solid #ff9800;
            margin-bottom:10px;
        ">
            {text}
        </div>
        """,
        unsafe_allow_html=True,
    )

def groups_hash(groups_list):
    """Создает хэш для групп, чтобы отслеживать изменения"""
    if not groups_list:
        return "empty"
    return hash(tuple(sorted(groups_list)))

# ---------- ФУНКЦИЯ СБРОСА ТОЛЬКО АВТОМАТИЧЕСКИХ ЗНАЧЕНИЙ ----------
def reset_auto_values_only():
    """Сбрасывает ТОЛЬКО автоматически рассчитанные значения и ручные рельсы"""
    
    # Увеличиваем счетчик расчетов для сброса виджетов
    st.session_state.calculation_counter = st.session_state.get("calculation_counter", 0) + 1
    
    # Сбрасываем версию для квотированных рельсов
    st.session_state.koshrot_boxes_version = st.session_state.get("koshrot_boxes_version", 0) + 1
    
    # Сбрасываем версию для ручных рельсов (הוספה ידנית)
    st.session_state.manual_rails_reset_version = st.session_state.get("manual_rails_reset_version", 0) + 1
    
    # Удаляем КЛЮЧИ ВИДЖЕТОВ для сброса интерфейса
    for key in list(st.session_state.keys()):
        # Удаляем ключи виджетов для сброса интерфейса
        if (key.startswith("fast_inc_") or 
            key.startswith("fastener_qty_") or
            key.startswith("koshrot_qty_") or
            key.startswith("m_len_") or  # Удаляем ключи ручных рельсов
            key.startswith("m_qty_")):
            del st.session_state[key]
    
    # Сбрасываем квотированные рельсы к ИСХОДНЫМ расчетным значениям
    if st.session_state.initial_calc_result:
        auto_rails = st.session_state.initial_calc_result.get("auto_rails", {})
        rails_base = {}
        for length, qty in auto_rails.items():
            klen = normalize_length_key(length)
            rails_base[klen] = rails_base.get(klen, 0) + int(qty)
        
        # Восстанавливаем только автоматические значения
        st.session_state.koshrot_qty = dict(rails_base)
    
    # Сбрасываем fasteners к ИСХОДНЫМ значениям расчета
    if st.session_state.initial_fasteners:
        st.session_state.fasteners = st.session_state.initial_fasteners.copy()
    
    # Сбрасываем галочки к ИСХОДНОМУ состоянию (все включены)
    if st.session_state.initial_fasteners_include:
        st.session_state.fasteners_include = st.session_state.initial_fasteners_include.copy()
    
    # Сбрасываем ручные рельсы (הוספה ידנית) - полностью очищаем
    st.session_state.manual_rows = 1
    st.session_state.manual_rails = {}
    
    # Удаляем все сохраненные значения ручных рельсов
    for key in list(st.session_state.keys()):
        if key.startswith("m_len_") or key.startswith("m_qty_"):
            del st.session_state[key]
    
    # Отметим, что отчет нужно обновить
    st.session_state.report_needs_update = True

# ---------- LOAD DATABASES ----------
panels = pd.read_csv("panels.csv")
channels = pd.read_csv("channels.csv")
parts = pd.read_csv("parts.csv")
panels["name"] = panels["name"].astype(str)

def round_up_to_tens(x: float) -> int:
    if x <= 0:
        return 0
    return int(math.ceil(x / 10.0) * 10)

def normalize_length_key(length) -> str:
    """Normalize a rail length key so 550, 550.0, '550', '550.0' map to '550'."""
    if length is None:
        return ""
    
    # Преобразуем в строку и убираем лишние символы
    s = str(length).strip().replace(",", ".")
    
    if s == "":
        return ""
    
    try:
        f = float(s)
        # Если это целое число, возвращаем как целое
        if f.is_integer():
            return str(int(f))
        # Иначе возвращаем как есть
        return str(f)
    except Exception:
        return s

def length_sort_key(length_key: str) -> float:
    """Sort helper: treat normalized length keys numerically (e.g., '30' < '295' < '300')."""
    try:
        return float(str(length_key).replace(",", "."))
    except Exception:
        return -1.0

def format_qty(q):
    try:
        qf = float(q)
        if qf.is_integer():
            return str(int(qf))
        s = f"{qf}".rstrip("0").rstrip(".")
        return s
    except Exception:
        return str(q)

def format_length_for_display(length):
    """Форматирует длину для отображения без лишних десятичных знаков"""
    try:
        f = float(length)
        if f.is_integer():
            return str(int(f))
        # Проверяем, заканчивается ли на .0
        s = str(f)
        if s.endswith('.0'):
            return s[:-2]
        return s
    except Exception:
        return str(length)

# ---------- PROJECT NAME ----------
st.markdown(right_label("שם פרויקט"), unsafe_allow_html=True)
project_name = st.text_input(
    "",
    value=st.session_state.project_name,
    key=f"project_name_input",
    label_visibility="collapsed",
)
st.session_state.project_name = project_name

# ---------- PANEL ADD / DELETE (SIDEBAR) ----------
st.sidebar.markdown(right_header("פאנל חדש"), unsafe_allow_html=True)
st.sidebar.markdown(right_label("שם פאנל"), unsafe_allow_html=True)
new_name = st.sidebar.text_input("", key="sidebar_panel_name", label_visibility="collapsed")
st.sidebar.markdown(right_label("רוחב (ס״מ)"), unsafe_allow_html=True)
new_w = st.sidebar.number_input(
    "",
    min_value=0.0,
    value=0.0,
    step=0.1,
    format="%.1f",
    key="panel_width",
    label_visibility="collapsed",
)
st.sidebar.markdown(right_label("אורך (ס״מ)"), unsafe_allow_html=True)
new_h = st.sidebar.number_input(
    "",
    min_value=0.0,
    value=0.0,
    step=0.1,
    format="%.1f",
    key="panel_height",
    label_visibility="collapsed",
)

if st.sidebar.button("להוסיף פאנל חדש"):
    panels.loc[len(panels)] = [str(new_name), new_w, new_h]
    panels.to_csv("panels.csv", index=False)
    st.sidebar.success("הפאנל נוסף")
    st.rerun()

if not panels.empty:
    for idx, row in panels.iterrows():
        c1, c2 = st.sidebar.columns([3, 1])
        c1.write(row["name"])
        if c2.button("❌", key=f"del_panel_{idx}"):
            panels = panels.drop(idx).reset_index(drop=True)
            panels.to_csv("panels.csv", index=False)
            if st.session_state.panel_name == row["name"]:
                st.session_state.panel_name = None
            st.rerun()
else:
    st.sidebar.write("אין פאנלים ברשימה.")

# ---------- PARTS LIBRARY (SIDEBAR) ----------
st.sidebar.markdown("&nbsp;", unsafe_allow_html=True)
st.sidebar.markdown(right_header("פריט חדש"), unsafe_allow_html=True)
st.sidebar.markdown(right_label("שם פריט"), unsafe_allow_html=True)
lib_new_name = st.sidebar.text_input("", key="lib_new_name", label_visibility="collapsed")
st.sidebar.markdown(right_label("יחידת מידה"), unsafe_allow_html=True)
st.sidebar.markdown('<div style="text-align:right;">', unsafe_allow_html=True)
unit = st.sidebar.radio(
    "",
    ["יח׳", "מטר", "ס״מ"],
    index=0,
    horizontal=True,
    key="lib_new_unit",
    label_visibility="collapsed",
)
st.sidebar.markdown("</div>", unsafe_allow_html=True)

if "unit" not in parts.columns:
    if "name" in parts.columns:
        parts = parts.reindex(columns=["name", "unit"])
    else:
        parts = pd.DataFrame(columns=["name", "unit"])

if st.sidebar.button("להוסיף פריט"):
    if lib_new_name:
        if lib_new_name in parts["name"].values:
            st.sidebar.warning("הפריט הזה כבר קיים, לא נוסף כפילוּל.")
        else:
            parts.loc[len(parts)] = [lib_new_name, unit]
            parts.to_csv("parts.csv", index=False)
            st.sidebar.success("הפריט נוסף")
            st.rerun()
    else:
        st.sidebar.warning("נא למלא שם פריט")

if not parts.empty:
    for idx, row in parts.iterrows():
        c1, c2 = st.sidebar.columns([3, 1])
        c1.write(f"{row['name']} ({row['unit']})")
        if c2.button("❌", key=f"del_lib_{idx}"):
            parts = parts.drop(idx).reset_index(drop=True)
            parts.to_csv("parts.csv", index=False)
            st.rerun()
else:
    st.sidebar.write("אין פריטים שמורים.")

# ---------- SELECT PANEL ----------
def panel_sort_key(n: str):
    if "640" in n:
        return (0, n)
    if "595" in n:
        return (1, n)
    return (2, n)

names = panels["name"].tolist()
panel_options = sorted(list(dict.fromkeys(names)), key=panel_sort_key)

if not panel_options:
    st.error("אין פאנלים בקובץ panels.csv")
    st.stop()

if st.session_state.panel_name in panel_options:
    default_index = panel_options.index(st.session_state.panel_name)
else:
    default_index = 0

st.markdown(right_label("סוג פאנל"), unsafe_allow_html=True)
panel_name = st.selectbox(
    "",
    panel_options,
    index=default_index,
    key=f"panel_select",
    label_visibility="collapsed",
)
st.session_state.panel_name = panel_name

panel_rows = panels[panels["name"] == panel_name]
if panel_rows.empty:
    st.error("הפאנל שנבחר לא נמצא בקובץ panels.csv")
    st.stop()

panel = panel_rows.iloc[0]

# ---------- ФУНКЦИИ ДЛЯ ДИАЛОГОВЫХ ОКОН ----------
def show_add_dialog(section_type):
    """Показывает диалог добавления панелей"""
    if section_type == "vertical":
        title = "הוספת פאנלים - עומדים"
        current_values = st.session_state.vertical_panel_values + [row["panel_value"] for row in st.session_state.vertical_custom_rows]
        show_dialog = st.session_state.show_add_dialog_vertical
        value_key = "new_panel_value_vertical"
    else:
        title = "הוספת פאנלים - שוכבים"
        current_values = st.session_state.horizontal_panel_values + [row["panel_value"] for row in st.session_state.horizontal_custom_rows]
        show_dialog = st.session_state.show_add_dialog_horizontal
        value_key = "new_panel_value_horizontal"
    
    if show_dialog:
        # Создаем контейнер для диалога
        dialog_html = f"""
        <div style="
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            background-color: white;
            padding: 25px;
            border-radius: 10px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.2);
            z-index: 1000;
            min-width: 300px;
            max-width: 90%;
            border: 2px solid #4a86e8;
        ">
            <h3 style="text-align: right; margin-top: 0; color: #2c3e50;">{title}</h3>
            <div style="text-align: right; margin-bottom: 20px; color: #555;">
                כמה פאנלים להוסיף?
            </div>
        """
        
        st.markdown(dialog_html, unsafe_allow_html=True)
        
        # Поле ввода
        col1, col2 = st.columns([3, 1])
        with col1:
            new_value = st.number_input(
                "",
                min_value=1,
                max_value=99,
                value=st.session_state[value_key],
                key=f"dialog_input_{section_type}",
                label_visibility="collapsed",
                help="הכנס מספר בין 1 ל-99"
            )
        
        # Проверка на дубликат
        error_message = None
        if new_value in current_values:
            error_message = "שורה עם ערך זה כבר קיימת"
        
        if error_message:
            warning_box(error_message)
        
        # Кнопки
        col1, col2, col3 = st.columns([1, 1, 2])
        with col1:
            if st.button("אישור", key=f"confirm_{section_type}", use_container_width=True, disabled=error_message is not None):
                if section_type == "vertical":
                    st.session_state.vertical_custom_rows.append({
                        "group_value": 1,
                        "panel_value": new_value
                    })
                    st.session_state.show_add_dialog_vertical = False
                else:
                    st.session_state.horizontal_custom_rows.append({
                        "group_value": 1,
                        "panel_value": new_value
                    })
                    st.session_state.show_add_dialog_horizontal = False
                st.rerun()
        
        with col2:
            if st.button("ביטול", key=f"cancel_{section_type}", use_container_width=True):
                if section_type == "vertical":
                    st.session_state.show_add_dialog_vertical = False
                else:
                    st.session_state.show_add_dialog_horizontal = False
                st.rerun()
        
        # Закрываем HTML div
        st.markdown("</div>", unsafe_allow_html=True)

def show_delete_confirm_dialog(row_index, section_type):
    """Показывает диалог подтверждения удаления"""
    if st.session_state.delete_row_confirm == f"{section_type}_{row_index}":
        dialog_html = """
        <div style="
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            background-color: white;
            padding: 25px;
            border-radius: 10px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.2);
            z-index: 1000;
            min-width: 300px;
            max-width: 90%;
            border: 2px solid #e74c3c;
        ">
            <h3 style="text-align: right; margin-top: 0; color: #c0392b;">מחיקת שורה</h3>
            <div style="text-align: right; margin-bottom: 20px; color: #555;">
                האם אתה בטוח שברצונך למחוק שורה זו?
            </div>
        """
        
        st.markdown(dialog_html, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 1, 2])
        with col1:
            if st.button("כן", key=f"delete_yes_{section_type}_{row_index}", use_container_width=True):
                if section_type == "vertical":
                    if row_index < 8:
                        st.session_state.vertical_group_values[row_index] = 0
                    else:
                        custom_index = row_index - 8
                        if custom_index < len(st.session_state.vertical_custom_rows):
                            st.session_state.vertical_custom_rows.pop(custom_index)
                else:
                    if row_index < 4:
                        st.session_state.horizontal_group_values[row_index] = 0
                    else:
                        custom_index = row_index - 4
                        if custom_index < len(st.session_state.horizontal_custom_rows):
                            st.session_state.horizontal_custom_rows.pop(custom_index)
                
                st.session_state.delete_row_confirm = None
                st.rerun()
        
        with col2:
            if st.button("לא", key=f"delete_no_{section_type}_{row_index}", use_container_width=True):
                st.session_state.delete_row_confirm = None
                st.rerun()
        
        st.markdown("</div>", unsafe_allow_html=True)

# ---------- GROUPS ----------
groups = []

st.markdown("""
    <style>
    .streamlit-expanderHeader svg {
        transform: rotate(0deg);
        transition: transform 0.3s;
    }
    .streamlit-expanderHeader[aria-expanded="true"] svg {
        transform: rotate(-90deg);
    }
    .streamlit-expanderHeader {
        text-align: right;
        direction: rtl;
    }
    .readonly-input {
        background-color: #f0f2f6;
        border: 1px solid #d0d0d0;
        border-radius: 4px;
        padding: 8px 12px;
        color: #31333F;
        font-family: inherit;
        font-size: 14px;
        width: 100%;
        box-sizing: border-box;
    }
    .delete-button {
        background-color: #ff6b6b;
        color: white;
        border: none;
        border-radius: 4px;
        padding: 4px 8px;
        cursor: pointer;
        font-size: 12px;
    }
    .delete-button:hover {
        background-color: #ff5252;
    }
    </style>
""", unsafe_allow_html=True)

# Секция вертикальных панелей - עומדים
with st.expander("**עומדים**", expanded=False):
    # Показываем диалог добавления если нужно
    show_add_dialog("vertical")
    
    # Показываем диалог удаления если нужно
    if st.session_state.delete_row_confirm and st.session_state.delete_row_confirm.startswith("vertical_"):
        row_index = int(st.session_state.delete_row_confirm.split("_")[1])
        show_delete_confirm_dialog(row_index, "vertical")
    
    vh = st.columns(2)
    vh[0].markdown(right_label("שורות"), unsafe_allow_html=True)
    vh[1].markdown(right_label("פאנלים"), unsafe_allow_html=True)
    
    # Предустановленные строки (1-8)
    for i in range(8):
        c0, c1 = st.columns(2)
        
        with c0:
            # Поле для ввода количества рядов
            group_key = f"g_g_vertical_{i}"
            current_value = st.session_state.vertical_group_values[i]
            
            # Проверяем, не установлено ли значение 0
            if current_value == 0 and f"prev_{group_key}" in st.session_state:
                # Пользователь попытался установить 0 - показываем диалог удаления
                if not st.session_state.delete_row_confirm:
                    st.session_state.delete_row_confirm = f"vertical_{i}"
                st.session_state[f"prev_{group_key}"] = 1
                current_value = 1
            
            g = st.number_input(
                "",
                0, 50, current_value,
                key=group_key,
                label_visibility="collapsed",
            )
            
            # Сохраняем предыдущее значение для отслеживания изменений
            if g != st.session_state.get(f"prev_{group_key}", current_value):
                st.session_state[f"prev_{group_key}"] = g
                st.session_state.vertical_group_values[i] = g
        
        with c1:
            # Не редактируемое поле для панелей (предустановленное значение)
            panel_value = i + 1
            st.markdown(
                f'<div class="readonly-input" style="padding: 8px 12px; text-align: center;">{panel_value}</div>',
                unsafe_allow_html=True
            )
        
        if g > 0:
            groups.append((panel_value, g, "עומד"))
    
    # Кастомные строки (добавленные пользователем)
    for i, row in enumerate(st.session_state.vertical_custom_rows):
        c0, c1 = st.columns(2)
        row_index = 8 + i
        
        with c0:
            group_key = f"g_g_vertical_custom_{i}"
            current_value = row["group_value"]
            
            # Проверяем, не установлено ли значение 0
            if current_value == 0 and f"prev_{group_key}" in st.session_state:
                # Пользователь попытался установить 0 - показываем диалог удаления
                if not st.session_state.delete_row_confirm:
                    st.session_state.delete_row_confirm = f"vertical_{row_index}"
                st.session_state[f"prev_{group_key}"] = 1
                current_value = 1
            
            g = st.number_input(
                "",
                0, 50, current_value,
                key=group_key,
                label_visibility="collapsed",
            )
            
            # Обновляем значение в списке
            if g != st.session_state.get(f"prev_{group_key}", current_value):
                st.session_state[f"prev_{group_key}"] = g
                st.session_state.vertical_custom_rows[i]["group_value"] = g
        
        with c1:
            # Не редактируемое поле для панелей (пользовательское значение)
            panel_value = row["panel_value"]
            st.markdown(
                f'<div class="readonly-input" style="padding: 8px 12px; text-align: center;">{panel_value}</div>',
                unsafe_allow_html=True
            )
        
        if g > 0:
            groups.append((panel_value, g, "עומד"))
    
    # Кнопка добавления
    if st.button("להוסיף פאנלים", key="add_panels_vertical"):
        st.session_state.show_add_dialog_vertical = True
        st.rerun()

# Секция горизонтальных панелей - שוכבים
with st.expander("**שוכבים**", expanded=False):
    # Показываем диалог добавления если нужно
    show_add_dialog("horizontal")
    
    # Показываем диалог удаления если нужно
    if st.session_state.delete_row_confirm and st.session_state.delete_row_confirm.startswith("horizontal_"):
        row_index = int(st.session_state.delete_row_confirm.split("_")[1])
        show_delete_confirm_dialog(row_index, "horizontal")
    
    hh = st.columns(2)
    hh[0].markdown(right_label("שורות"), unsafe_allow_html=True)
    hh[1].markdown(right_label("פאנלים"), unsafe_allow_html=True)
    
    # Предустановленные строки (1-4)
    for i in range(4):
        c0, c1 = st.columns(2)
        
        with c0:
            # Поле для ввода количества рядов
            group_key = f"g_g_horizontal_{i}"
            current_value = st.session_state.horizontal_group_values[i]
            
            # Проверяем, не установлено ли значение 0
            if current_value == 0 and f"prev_{group_key}" in st.session_state:
                # Пользователь попытался установить 0 - показываем диалог удаления
                if not st.session_state.delete_row_confirm:
                    st.session_state.delete_row_confirm = f"horizontal_{i}"
                st.session_state[f"prev_{group_key}"] = 1
                current_value = 1
            
            g = st.number_input(
                "",
                0, 50, current_value,
                key=group_key,
                label_visibility="collapsed",
            )
            
            # Сохраняем предыдущее значение для отслеживания изменений
            if g != st.session_state.get(f"prev_{group_key}", current_value):
                st.session_state[f"prev_{group_key}"] = g
                st.session_state.horizontal_group_values[i] = g
        
        with c1:
            # Не редактируемое поле для панелей (предустановленное значение)
            panel_value = i + 1
            st.markdown(
                f'<div class="readonly-input" style="padding: 8px 12px; text-align: center;">{panel_value}</div>',
                unsafe_allow_html=True
            )
        
        if g > 0:
            groups.append((panel_value, g, "שוכב"))
    
    # Кастомные строки (добавленные пользователем)
    for i, row in enumerate(st.session_state.horizontal_custom_rows):
        c0, c1 = st.columns(2)
        row_index = 4 + i
        
        with c0:
            group_key = f"g_g_horizontal_custom_{i}"
            current_value = row["group_value"]
            
            # Проверяем, не установлено ли значение 0
            if current_value == 0 and f"prev_{group_key}" in st.session_state:
                # Пользователь попытался установить 0 - показываем диалог удаления
                if not st.session_state.delete_row_confirm:
                    st.session_state.delete_row_confirm = f"horizontal_{row_index}"
                st.session_state[f"prev_{group_key}"] = 1
                current_value = 1
            
            g = st.number_input(
                "",
                0, 50, current_value,
                key=group_key,
                label_visibility="collapsed",
            )
            
            # Обновляем значение в списке
            if g != st.session_state.get(f"prev_{group_key}", current_value):
                st.session_state[f"prev_{group_key}"] = g
                st.session_state.horizontal_custom_rows[i]["group_value"] = g
        
        with c1:
            # Не редактируемое поле для панелей (пользовательское значение)
            panel_value = row["panel_value"]
            st.markdown(
                f'<div class="readonly-input" style="padding: 8px 12px; text-align: center;">{panel_value}</div>',
                unsafe_allow_html=True
            )
        
        if g > 0:
            groups.append((panel_value, g, "שוכב"))
    
    # Кнопка добавления
    if st.button("להוסיף פאנלים", key="add_panels_horizontal"):
        st.session_state.show_add_dialog_horizontal = True
        st.rerun()

# ---------- ENGINE ----------
def split_into_segments(total_length: int):
    if total_length <= 0:
        return []
    if total_length <= 550:
        return [total_length]
    
    full = total_length // 550
    remainder = total_length % 550
    
    if full == 1 and 0 < remainder < 100:
        half = total_length / 2.0
        a = round(half)
        b = total_length - a
        return [a, b]
    
    segs = []
    r = total_length
    while r > 550:
        segs.append(550)
        r -= 550
    segs.append(r)
    return segs

def calc_fixings(N: int):
    if N == 1:
        return 0, 0
    
    pairs = N // 2
    earthing = pairs
    middle = pairs
    
    if pairs > 1:
        middle += (pairs - 1) * 2
    
    if N % 2 == 1:
        earthing += 1
        middle += 1
    
    return earthing, middle

def calc_group(N, orientation, panel_row):
    name_str = str(panel_row["name"])
    if "640" in name_str and orientation == "שוכב" and N in (1, 2):
        if N == 1:
            final = 250
        else:
            final = 490
        segs = [final]
        connectors = 0
        earthing, middle = calc_fixings(N)
        edge = 4
        rails_per_row = 2
        return segs, connectors, earthing, middle, edge, rails_per_row
    
    if orientation == "עומד":
        base = panel_row["width"] * N
    else:
        base = panel_row["height"] * N
    
    fixings = N + 1
    raw = base + fixings * 2
    final = math.ceil((raw + 10) / 10) * 10
    final = int(final)
    
    segs = split_into_segments(final)
    connectors = (len(segs) - 1) * 2
    earthing, middle = calc_fixings(N)
    edge = 4
    rails_per_row = 2
    
    return segs, connectors, earthing, middle, edge, rails_per_row

def do_calculation(panel_row, groups_list):
    auto_rails = {}
    conn = ear = mid = edge = 0
    total_panels = 0
    
    for n, g, o in groups_list:
        total_panels += n * g
        for _ in range(g):
            segs, c, e, m, ed, rails_per_row = calc_group(n, o, panel_row)
            for s in segs:
                auto_rails[s] = auto_rails.get(s, 0) + rails_per_row
            conn += c
            ear += e
            mid += m
            edge += ed
    
    return {
        "auto_rails": auto_rails,
        "conn": conn,
        "ear": ear,
        "mid": mid,
        "edge": edge,
        "total_panels": total_panels,
    }

def build_html_report(calc_result, project_name, panel_name, channel_order, extra_parts, manual_rails):
    # Используем актуальные значения из koshrot_qty для автоматических рельсов
    # и manual_rails для ручных рельсов
    auto_rails_actual = {}
    
    # Получаем актуальные значения из koshrot_qty (включая ручные изменения)
    if st.session_state.koshrot_qty:
        for length_str, qty in st.session_state.koshrot_qty.items():
            try:
                # Используем форматированную длину для отображения
                length_display = format_length_for_display(length_str)
                auto_rails_actual[length_display] = qty
            except:
                auto_rails_actual[length_str] = qty
    
    rails_total = {}
    
    # Добавляем актуальные значения автоматических рельсов
    for length, qty in auto_rails_actual.items():
        rails_total[length] = rails_total.get(length, 0) + qty
    
    # Добавляем ручные рельсы
    for length, qty in manual_rails.items():
        length_display = format_length_for_display(length)
        rails_total[length_display] = rails_total.get(length_display, 0) + qty
    
    ear = calc_result.get("ear", 0)
    mid = calc_result.get("mid", 0)
    edge = calc_result.get("edge", 0)
    conn = calc_result.get("conn", 0)
    total_panels = calc_result.get("total_panels", 0)
    
    # Расчет общей длины для M8 болтов
    total_length_cm = 0
    # Используем числовые значения для расчета
    if st.session_state.koshrot_qty:
        for length_str, qty in st.session_state.koshrot_qty.items():
            try:
                length_num = float(length_str)
                total_length_cm += length_num * qty
            except:
                pass
    
    for length, qty in manual_rails.items():
        try:
            length_num = float(length)
            total_length_cm += length_num * qty
        except:
            pass
    
    screws_iso = round_up_to_tens(conn * 4 + total_panels)
    
    m8_count = 0
    if total_length_cm > 0:
        m8_base = total_length_cm / 140.0
        m8_count = round_up_to_tens(m8_base)
    
    html = """
    <html>
    <head>
        <meta charset="utf-8">
        <title>דו&quot;ח מערכת סולארית</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                margin: 30px;
                background-color: white;
                color: black;
                direction: rtl;
            }
            h1 {
                font-size: 22px;
            }
            h2 {
                font-size: 18px;
                margin-top: 24px;
            }
            p {
                margin: 2px 0;
            }
            table {
                border-collapse: collapse;
                border:none;
            }
            td {
                padding: 0 0 2px 0;
            }
        </style>
    </head>
    <body>
    """
    
    html += f"<h1>{project_name}</h1>"
    
    html += "<h2>קושרות (כמות × אורך)</h2>"
    if rails_total:
        for length in sorted(rails_total.keys(), key=lambda x: float(str(x).replace(",", ".")) if str(x).replace(",", ".").replace(".", "").isdigit() else 0, reverse=True):
            html += f"<p dir='rtl' style='text-align:right;'>{rails_total[length]} × {length}</p>"
    
    # --- פרזול בסקירה ---
    fasteners = [
        ("מהדק הארקה", ear),
        ("מהדק אמצע", mid),
        ("מהדק קצה", edge),
        ("פקק לקושרות", edge),
        ("מחברי קושרות", conn),
        ("בורג איסכורית 3,5", screws_iso),
        ("M8 בורג", m8_count),
        ("M8 אום", m8_count),
    ]
    
    overrides = st.session_state.get("fasteners")
    if overrides:
        # Обновляем только те значения, которые были изменены
        updated_fasteners = []
        for lbl, base_val in fasteners:
            if lbl in overrides:
                updated_fasteners.append((lbl, overrides[lbl]))
            else:
                updated_fasteners.append((lbl, base_val))
        fasteners = updated_fasteners
    
    inc_map = st.session_state.get('fasteners_include', {})
    visible_fasteners = [(lbl, val) for lbl, val in fasteners if val > 0 and bool(inc_map.get(lbl, True))]
    
    html += "<h2>פרזול</h2>"
    if visible_fasteners:
        html += "<table style='direction:rtl; text-align:right; border:none;'><tbody>"
        for lbl, val in visible_fasteners:
            html += (
                "<tr style='border:none;'>"
                f"<td style='text-align:right; white-space:nowrap; border:none;'>{lbl}</td>"
                f"<td style='text-align:left; white-space:nowrap; border:none;'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;{val}</td>"
                "</tr>"
            )
        html += "</tbody></table>"
    
    if channel_order:
        html += "<h2>תעלות עם מכסים (מטר)</h2>"
        html += "<table style='direction:rtl; text-align:right; border:none;'><tbody>"
        for name, qty in channel_order.items():
            html += (
                "<tr style='border:none;'>"
                f"<td style='text-align:right; white-space:nowrap; border:none;'>{name}</td>"
                f"<td style='text-align:left; white-space:nowrap; border:none;'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;{format_qty(qty)}</td>"
                "</tr>"
            )
        html += "</tbody></table>"
    
    if extra_parts:
        html += "<h2>פריטים נוספים</h2>"
        html += "<table style='direction:rtl; text-align:right; border:none;'><tbody>"
        for p in extra_parts:
            name = p["name"]
            qty = p["qty"]
            unit = ""
            row = parts[parts["name"] == name]
            if not row.empty:
                unit = row.iloc[0].get("unit", "")
            
            qty_text = f"{qty} {unit}" if unit else str(qty)
            html += (
                "<tr style='border:none;'>"
                f"<td style='text-align:right; white-space:nowrap; border:none;'>{name}</td>"
                f"<td style='text-align:left; white-space:nowrap; border=none;'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;{qty_text}</td>"
                "</tr>"
            )
        html += "</tbody></table>"
    
    html += "</body></html>"
    return html

# ---------- BUTTON: CALCULATE ----------
if st.button("חשב", type="primary", use_container_width=True):
    # 1. Вычисляем хэш текущих групп
    current_groups_hash = groups_hash(groups)
    
    # 2. Сохраняем текущий расчет
    if groups:
        new_calc_result = do_calculation(panel, groups)
    else:
        new_calc_result = {
            "auto_rails": {},
            "conn": 0,
            "ear": 0,
            "mid": 0,
            "edge": 0,
            "total_panels": 0,
        }
    
    # 3. Проверяем, изменились ли группы
    groups_changed = st.session_state.previous_groups_hash != current_groups_hash
    
    # 4. Если группы изменились ИЛИ это первый расчет
    if groups_changed or st.session_state.initial_calc_result is None:
        # Сохраняем как исходный расчет
        st.session_state.initial_calc_result = new_calc_result.copy()
        
        # Создаем исходные значения для fasteners
        ear = new_calc_result["ear"]
        mid = new_calc_result["mid"]
        edge = new_calc_result["edge"]
        conn = new_calc_result["conn"]
        total_panels = new_calc_result["total_panels"]
        
        auto_rails = new_calc_result.get("auto_rails", {})
        total_length_cm = 0
        for length, qty in auto_rails.items():
            total_length_cm += float(length) * qty
        
        screws_iso = round_up_to_tens(conn * 4 + total_panels)
        m8_count = 0
        if total_length_cm > 0:
            m8_base = total_length_cm / 140.0
            m8_count = round_up_to_tens(m8_base)
        
        fasteners_base = [
            ("מהדק הארקה", ear),
            ("מהדק אמצע", mid),
            ("מהדק קצה", edge),
            ("פקק לקושרות", edge),
            ("מחברי קושרות", conn),
            ("בורג איסכורית 3,5", screws_iso),
            ("M8 בורג", m8_count),
            ("M8 אום", m8_count),
        ]
        
        st.session_state.initial_fasteners = {lbl: int(val) for (lbl, val) in fasteners_base}
        st.session_state.initial_fasteners_include = {lbl: True for (lbl, _) in fasteners_base}
        
        # Инициализируем текущие значения
        st.session_state.fasteners = st.session_state.initial_fasteners.copy()
        st.session_state.fasteners_include = st.session_state.initial_fasteners_include.copy()
        
        # Инициализируем koshrot_qty ТОЛЬКО автоматическими значениями
        auto_rails = new_calc_result.get("auto_rails", {})
        rails_base = {}
        for length, qty in auto_rails.items():
            klen = normalize_length_key(length)
            rails_base[klen] = rails_base.get(klen, 0) + int(qty)
        st.session_state.koshrot_qty = dict(rails_base)
    
    # 5. Сохраняем хэш групп
    st.session_state.previous_groups_hash = current_groups_hash
    
    # 6. Обновляем текущий результат расчета
    st.session_state.calc_result = new_calc_result
    
    # 7. Сбрасываем ТОЛЬКО автоматические значения + רועי ידנית
    reset_auto_values_only()
    
    # 8. Устанавливаем флаг
    st.session_state.just_calculated = True
    st.session_state.report_needs_update = True
    st.rerun()

if st.session_state.get("just_calculated"):
    success_box("החישוב עודכן")
    st.session_state.just_calculated = False

calc_result = st.session_state.calc_result

# ---------- SHOW CALC RESULT ----------
if calc_result is not None:
    auto_rails = calc_result["auto_rails"]
    manual_rails = st.session_state.manual_rails
    
    st.write(f"סה\"כ פאנלים: {calc_result['total_panels']}")
    
    # ----- קושרות -----
    with st.expander("**קושרות**", expanded=False):
        # Важно: В этом разделе должны быть ТОЛЬКО автоматически рассчитанные значения
        # НЕ добавляем ручные рельсы (manual_rails)!
        rails_base = {}
        for length, qty in auto_rails.items():
            klen = normalize_length_key(length)
            rails_base[klen] = rails_base.get(klen, 0) + int(qty)
        
        # Инициализируем koshrot_qty если нужно (ТОЛЬКО авто значения)
        if not st.session_state.koshrot_qty:
            st.session_state.koshrot_qty = dict(rails_base)
        else:
            # Проверяем, что в koshrot_qty только авто значения
            # Если есть какие-то длины, которых нет в авто расчете, удаляем их
            current_keys = set(st.session_state.koshrot_qty.keys())
            auto_keys = set(rails_base.keys())
            
            # Удаляем длины, которых нет в авто расчете
            for key in current_keys - auto_keys:
                del st.session_state.koshrot_qty[key]
            
            # Обновляем существующие авто значения
            for length, qty in rails_base.items():
                # Обновляем только если значение не было изменено пользователем
                # или если это новый расчет
                if length not in st.session_state.koshrot_qty:
                    st.session_state.koshrot_qty[length] = qty
        
        # Создаем временный словарь для хранения значений из виджетов
        temp_koshrot_qty = {}
        
        if st.session_state.koshrot_qty:
            for length in sorted(st.session_state.koshrot_qty.keys(), key=length_sort_key, reverse=True):
                # Форматируем длину для отображения
                display_length = format_length_for_display(length)
                st.markdown(right_label(f"אורך: {display_length} ס״מ"), unsafe_allow_html=True)
                
                # Используем уникальный ключ
                qty_key = f"koshrot_qty_{length}_{st.session_state.koshrot_boxes_version}_{st.session_state.calculation_counter}"
                default_val = int(st.session_state.koshrot_qty.get(length, 0))
                
                # Получаем значение из виджета
                qty_val = st.number_input(
                    "",
                    min_value=0,
                    value=default_val,
                    step=1,
                    key=qty_key,
                    label_visibility="collapsed",
                )
                
                # Сохраняем во временный словарь
                temp_koshrot_qty[length] = int(qty_val)
        
        # Обновляем основной koshrot_qty значениями из виджетов
        for length, qty in temp_koshrot_qty.items():
            if st.session_state.koshrot_qty.get(length) != qty:
                st.session_state.koshrot_qty[length] = qty
                st.session_state.report_needs_update = True
        
        if not st.session_state.koshrot_qty:
            st.write("אין קושרות מחושבות")
    
    # ----- קושרות (הוספה ידנית) -----
    with st.expander("**קושרות (הוספה ידנית)**", expanded=False):
        mh = st.columns(2)
        mh[0].markdown(right_label("אורך (ס״מ)"), unsafe_allow_html=True)
        mh[1].markdown(right_label("כמות"), unsafe_allow_html=True)
        
        manual_rows = st.session_state.manual_rows
        for j in range(1, manual_rows + 1):
            cols = st.columns(2)
            
            # Уникальный ключ с версией сброса
            length_key = f"m_len_{j}_{st.session_state.manual_rails_reset_version}"
            qty_key = f"m_qty_{j}_{st.session_state.manual_rails_reset_version}"
            
            # Начинаем с нулевых значений (форма сброшена)
            length = cols[0].number_input(
                "",
                min_value=0,
                max_value=10000,
                step=10,
                value=0,  # Всегда начинаем с 0 после сброса
                key=length_key,
                label_visibility="collapsed",
            )
            qty = cols[1].number_input(
                "",
                min_value=0,
                max_value=1000,
                step=1,
                value=0,  # Всегда начинаем с 0 после сброса
                key=qty_key,
                label_visibility="collapsed",
            )
        
        if st.button("להוסיף עוד קושרות", key="add_manual_rails"):
            st.session_state.manual_rows += 1
            st.rerun()
        
        # Собираем ручные рельсы и проверяем изменения
        manual_rails_dict = {}
        manual_rails_changed = False
        
        for j in range(1, st.session_state.manual_rows + 1):
            length_key = f"m_len_{j}_{st.session_state.manual_rails_reset_version}"
            qty_key = f"m_qty_{j}_{st.session_state.manual_rails_reset_version}"
            
            length = st.session_state.get(length_key, 0)
            qty = st.session_state.get(qty_key, 0)
            
            if length and qty:
                manual_rails_dict[length] = manual_rails_dict.get(length, 0) + qty
        
        # Проверяем, изменились ли ручные рельсы
        if manual_rails_dict != st.session_state.manual_rails:
            st.session_state.manual_rails = manual_rails_dict
            st.session_state.report_needs_update = True
        else:
            st.session_state.manual_rails = manual_rails_dict
    
    # ----- פרזול -----
    with st.expander("**פרזול**", expanded=False):
        # Базовые значения из расчета
        ear = calc_result["ear"]
        mid = calc_result["mid"]
        edge = calc_result["edge"]
        conn = calc_result["conn"]
        total_panels = calc_result["total_panels"]
        
        # Расчет для M8: учитываем и авто и ручные рельсы
        rails_total = {}
        
        # Используем актуальные значения из koshrot_qty
        if st.session_state.koshrot_qty:
            for length_str, qty in st.session_state.koshrot_qty.items():
                try:
                    length = float(length_str)
                    rails_total[length] = rails_total.get(length, 0) + qty
                except:
                    rails_total[length_str] = rails_total.get(length_str, 0) + qty
        
        # Добавляем ручные рельсы
        for length, qty in manual_rails.items():
            rails_total[length] = rails_total.get(length, 0) + qty
        
        total_length_cm = 0
        for length, qty in rails_total.items():
            try:
                total_length_cm += float(length) * qty
            except Exception:
                pass
        
        screws_iso = round_up_to_tens(conn * 4 + total_panels)
        m8_count = 0
        if total_length_cm > 0:
            m8_base = total_length_cm / 140.0
            m8_count = round_up_to_tens(m8_base)
        
        # Базовые значения (обновляются всегда при расчете)
        fasteners_base = [
            ("מהדק הארקה", ear),
            ("מהדק אמצע", mid),
            ("מהדק קצה", edge),
            ("פקק לקושרות", edge),
            ("מחברי קושרות", conn),
            ("בורג איסכורית 3,5", screws_iso),
            ("M8 בורג", m8_count),
            ("M8 אום", m8_count),
        ]
        
        # Создаем базовые значения для текущего расчета
        current_base_fasteners = {lbl: int(val) for (lbl, val) in fasteners_base}
        
        # Если fasteners не инициализированы или расчет изменился, используем новые значения
        if not st.session_state.fasteners or st.session_state.fasteners.keys() != current_base_fasteners.keys():
            # Проверяем, есть ли уже сохраненные значения пользователя
            if st.session_state.fasteners:
                # Сохраняем пользовательские изменения, если они есть
                updated_fasteners = {}
                for lbl, base_val in current_base_fasteners.items():
                    if lbl in st.session_state.fasteners:
                        # Сохраняем пользовательское значение, если оно было изменено
                        user_val = st.session_state.fasteners[lbl]
                        if user_val != 0:  # Сохраняем ненулевые пользовательские значения
                            updated_fasteners[lbl] = user_val
                        else:
                            updated_fasteners[lbl] = base_val
                    else:
                        updated_fasteners[lbl] = base_val
                st.session_state.fasteners = updated_fasteners
            else:
                st.session_state.fasteners = current_base_fasteners
        
        # Инициализируем fasteners_include если нужно
        if not st.session_state.fasteners_include:
            st.session_state.fasteners_include = {lbl: True for lbl in current_base_fasteners.keys()}
        else:
            # Добавляем новые позиции, если они появились
            for lbl in current_base_fasteners.keys():
                if lbl not in st.session_state.fasteners_include:
                    st.session_state.fasteners_include[lbl] = True
        
        # UI для каждого fastener - ИЗМЕНЕННЫЙ LAYOUT
        new_fasteners = {}
        fasteners_changed = False
        
        for i, (lbl, base_val) in enumerate(fasteners_base):
            # Получаем текущее значение
            current_val = st.session_state.fasteners.get(lbl, base_val)
            current_val = int(current_val) if current_val is not None else int(base_val)
            
            # Показываем только если значение > 0 или если пользователь уже изменял его
            if int(base_val) == 0 and current_val == 0 and lbl not in st.session_state.fasteners:
                continue
            
            # НОВЫЙ LAYOUT: [Поле ввода] [Чекбокс с подписью]
            col1, col2 = st.columns([1, 3])
            
            with col1:
                # Поле ввода количества - СЛЕВА
                val_key = f"fastener_qty_{lbl}_{st.session_state.calculation_counter}"
                v = st.number_input(
                    "",
                    min_value=0,
                    value=current_val,
                    step=1,
                    key=val_key,
                    label_visibility="collapsed",
                )
            
            with col2:
                # Чекбокс с подписью - СПРАВА
                # Используем HTML для правильного отображения текста справа от чекбокса
                inc_key = f"fast_inc_{lbl}_{st.session_state.calculation_counter}"
                inc_default = st.session_state.fasteners_include.get(lbl, True)
                
                # Создаем контейнер для чекбокса с текстом
                st.markdown(
                    f"""
                    <div style="display: flex; align-items: center; justify-content: flex-end; direction: rtl;">
                        <span style="margin-right: 8px; font-weight: normal;">{lbl}</span>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                
                # Чекбокс без видимой метки (метка уже в HTML выше)
                inc_val = st.checkbox(
                    "",
                    value=inc_default,
                    key=inc_key,
                    label_visibility="collapsed"
                )
            
            if inc_val != st.session_state.fasteners_include.get(lbl, True):
                st.session_state.fasteners_include[lbl] = bool(inc_val)
                st.session_state.report_needs_update = True
            else:
                st.session_state.fasteners_include[lbl] = bool(inc_val)
            
            if v != current_val:
                fasteners_changed = True
            
            new_fasteners[lbl] = int(v)
        
        # Обновляем fasteners если были изменения
        if fasteners_changed:
            st.session_state.fasteners = new_fasteners
            st.session_state.report_needs_update = True
        else:
            st.session_state.fasteners = new_fasteners

# ---------- CHANNELS ----------
with st.expander("**תעלות עם מכסים (מטר)**", expanded=False):
    channel_order = {}
    for i, r in channels.iterrows():
        name = r["name"]
        if "רשת" in name:
            step_value = 3.0
        elif "פח" in name:
            step_value = 2.5
        else:
            step_value = 1.0
        
        st.markdown(right_label(name), unsafe_allow_html=True)
        current_value = st.session_state.channel_order.get(name, 0.0)
        q = st.number_input(
            "",
            min_value=0.0,
            value=float(current_value),
            step=step_value,
            format="%g",
            key=f"channel_{i}",
            label_visibility="collapsed",
        )
        if q > 0:
            channel_order[name] = q
        elif name in st.session_state.channel_order:
            channel_order[name] = 0
    
    # Проверяем изменения в каналах
    new_channel_order = {k: v for k, v in channel_order.items() if v > 0}
    if new_channel_order != st.session_state.channel_order:
        st.session_state.channel_order = new_channel_order
        st.session_state.report_needs_update = True
    else:
        st.session_state.channel_order = new_channel_order

# ---------- EXTRA PARTS ----------
with st.expander("**הוסף פריט**", expanded=False):
    if not parts.empty:
        extra_rows = st.session_state.extra_rows
        chosen_entries = []
        names_list = parts["name"].tolist()
        
        for i in range(1, extra_rows + 1):
            st.markdown(right_label("פריט"), unsafe_allow_html=True)
            prev_extra = None
            if i-1 < len(st.session_state.extra_parts):
                prev_extra = st.session_state.extra_parts[i-1]["name"]
            
            index = 0
            if prev_extra and prev_extra in names_list:
                index = names_list.index(prev_extra)
            
            part = st.selectbox(
                "",
                names_list,
                index=index,
                key=f"extra_name_{i}",
                label_visibility="collapsed",
            )
            
            st.markdown(right_label("כמות"), unsafe_allow_html=True)
            prev_qty = 0
            if i-1 < len(st.session_state.extra_parts):
                prev_qty = st.session_state.extra_parts[i-1]["qty"]
            
            qty = st.number_input(
                "",
                min_value=0,
                value=int(prev_qty),
                step=1,
                key=f"extra_qty_{i}",
                label_visibility="collapsed",
            )
            
            if qty > 0:
                chosen_entries.append((part, qty))
        
        if st.button("להוסיף עוד פריט", key="add_extra"):
            st.session_state.extra_rows += 1
            st.rerun()
        
        agg = {}
        for name, qty in chosen_entries:
            agg[name] = agg.get(name, 0) + qty
        
        new_extra_parts = [{"name": n, "qty": q} for n, q in agg.items()]
        
        # Проверяем изменения в дополнительных частях
        if new_extra_parts != st.session_state.extra_parts:
            st.session_state.extra_parts = new_extra_parts
            st.session_state.report_needs_update = True
        else:
            st.session_state.extra_parts = new_extra_parts
    else:
        info_box("אין פריטים בקובץ parts.csv – נא להוסיף פריט חדש בצד שמאל")

success_box("מוכן לייצוא (HTML → PDF דרך הדפסה)")

# ---------- EXPORT ----------
with st.expander("**ייצוא (HTML להדפסה ל-PDF)**", expanded=False):
    if "show_report" not in st.session_state:
        st.session_state.show_report = False
    
    calc_result = st.session_state.calc_result
    if calc_result is not None:
        # Автоматически обновляем отчет при любых изменениях
        if st.session_state.get("report_needs_update", True):
            # Генерируем новый отчет
            html_report = build_html_report(
                calc_result=calc_result,
                project_name=st.session_state.project_name,
                panel_name=panel_name,
                channel_order=st.session_state.channel_order,
                extra_parts=st.session_state.extra_parts,
                manual_rails=st.session_state.manual_rails,
            )
            # Сохраняем сгенерированный отчет
            st.session_state.last_html_report = html_report
            st.session_state.report_needs_update = False
        
        # Используем сохраненный отчет
        html_report = st.session_state.get("last_html_report", "")
        
        c_left, c_right = st.columns(2)
        with c_left:
            if st.button('לייצא דו"ח', use_container_width=True, key="export"):
                st.session_state.show_report = True
                st.rerun()
        
        with c_right:
            if st.button("פתח בטאב חדש", use_container_width=True, key="new_tab"):
                js = f"""<script>
                    const w = window.open('', '_blank');
                    if (w) {{
                        w.document.open();
                        w.document.write({json.dumps(html_report)});
                        w.document.close();
                    }}
                </script>"""
                components.html(js, height=0)
        
        if st.session_state.show_report:
            st.markdown("<div style='height:10px;'></div>", unsafe_allow_html=True)
            components.html(html_report, height=950, scrolling=True)
    else:
        info_box('קודם יש לחשב, ואז ניתן לייצא דו"ח')

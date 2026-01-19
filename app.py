import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import math
import json
import urllib.parse

# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="סולארי - חישוב חומרים",
    page_icon="📐",
    layout="centered",
    initial_sidebar_state="collapsed"  # Скрываем sidebar на телефоне
)

# ---------- CUSTOM STYLES ----------
st.markdown("""
<style>
    /* Основные стили */
    .main {
        padding: 20px;
        max-width: 800px;
        margin: 0 auto;
        background: white;
    }
    
    /* Заголовки разделов */
    .section-header {
        font-size: 18px;
        font-weight: 600;
        color: #2d3748;
        margin: 28px 0 16px 0;
        text-align: right;
        padding-bottom: 8px;
        border-bottom: 2px solid #f0f4f8;
    }
    
    /* Тонкие разделители */
    .divider {
        border-top: 1px solid #e2e8f0;
        margin: 24px 0;
    }
    
    /* Поля ввода */
    .stTextInput input, .stNumberInput input, .stSelectbox select {
        border: 1px solid #e2e8f0;
        border-radius: 6px;
        padding: 12px 16px;
        font-size: 16px;
        color: #2d3748;
        background: white;
        transition: border-color 0.2s;
    }
    
    .stTextInput input:focus, .stNumberInput input:focus, .stSelectbox select:focus {
        border-color: #4b75c9;
        outline: none;
        box-shadow: 0 0 0 2px rgba(75, 117, 201, 0.1);
    }
    
    /* Кнопки */
    .stButton > button {
        background-color: #4b75c9;
        color: white;
        border: none;
        border-radius: 6px;
        padding: 14px 24px;
        font-size: 16px;
        font-weight: 500;
        width: 100%;
        transition: background-color 0.2s;
    }
    
    .stButton > button:hover {
        background-color: #3a62b5;
    }
    
    /* Акцентная кнопка */
    .primary-btn > button {
        background-color: #4b75c9;
        font-size: 17px;
        font-weight: 600;
        padding: 16px;
        margin: 20px 0;
    }
    
    /* Строки данных */
    .data-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 12px 0;
        border-bottom: 1px solid #f7fafc;
    }
    
    /* Адаптивность для телефона */
    @media (max-width: 768px) {
        .main {
            padding: 16px;
        }
        
        .section-header {
            font-size: 17px;
            margin: 24px 0 12px 0;
        }
        
        .stButton > button {
            padding: 16px;
            margin: 12px 0;
        }
        
        .stNumberInput input, .stSelectbox select {
            min-height: 48px;
            font-size: 16px !important;
        }
        
        /* Увеличиваем чекбоксы */
        .stCheckbox label {
            font-size: 15px;
            padding: 4px 0;
        }
        
        /* Горизонтальные разделители */
        .divider {
            margin: 20px 0;
        }
    }
    
    /* Скрываем элементы на мобильных */
    @media (max-width: 768px) {
        .mobile-hide {
            display: none;
        }
    }
    
    /* Уведомления */
    .stAlert {
        border-radius: 6px;
        border: 1px solid #e2e8f0;
        margin: 12px 0;
    }
    
    /* Улучшаем таблицы на мобильных */
    @media (max-width: 768px) {
        .stDataFrame {
            font-size: 14px;
        }
    }
    
    /* Плавные переходы */
    * {
        transition: all 0.2s ease;
    }
</style>
""", unsafe_allow_html=True)

# ---------- SESSION STATE ----------
if "calc_result" not in st.session_state:
    st.session_state.calc_result = None
if "just_calculated" not in st.session_state:
    st.session_state.just_calculated = False
if "project_name" not in st.session_state:
    st.session_state.project_name = ""
if "panel_name" not in st.session_state:
    st.session_state.panel_name = None
if "groups" not in st.session_state:
    st.session_state.groups = [(4, "עומד")]  # Начальная группа
if "fasteners" not in st.session_state:
    st.session_state.fasteners = {}
if "channels" not in st.session_state:
    st.session_state.channels = {}
if "extra_parts" not in st.session_state:
    st.session_state.extra_parts = []
if "koshrot_qty" not in st.session_state:
    st.session_state.koshrot_qty = {}
if "koshrot_boxes_version" not in st.session_state:
    st.session_state.koshrot_boxes_version = 0
if "fasteners_version" not in st.session_state:
    st.session_state.fasteners_version = 0

# ---------- LOAD DATABASES ----------
@st.cache_data
def load_data():
    panels = pd.read_csv("panels.csv")
    channels = pd.read_csv("channels.csv")
    parts = pd.read_csv("parts.csv")
    panels["name"] = panels["name"].astype(str)
    return panels, channels, parts

panels, channels_df, parts = load_data()

# ---------- HELPER FUNCTIONS ----------
def right_label(text: str) -> str:
    return f'<div style="text-align:right; font-weight:500; margin-bottom:8px;">{text}</div>'

def format_whatsapp_message(project_name, panel_name, groups, materials_text):
    """Форматирует сообщение для WhatsApp"""
    message = f"""דו״ח חומרים למערכת סולארית

פרויקט: {project_name}
סוג פאנל: {panel_name}

קבוצות פאנלים:
"""
    
    # Добавляем группы
    for i, (num, direction) in enumerate(groups, 1):
        if num > 0:
            message += f"שורה {i}: {num} פאנלים {direction}\n"
    
    message += f"\nחומרים:\n{materials_text}\n\n"
    message += "הדו״ח נוצר באפליקציית סולארי"
    
    return message

# ---------- ENGINE FUNCTIONS ----------
def round_up_to_tens(x: float) -> int:
    if x <= 0:
        return 0
    return int(math.ceil(x / 10.0) * 10)

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

def do_calculation(panel_row, groups_list):
    """Основная функция расчета"""
    total_panels = sum(num for num, _ in groups_list if num > 0)
    
    # Простой расчет для примера
    conn = total_panels * 2
    ear, mid = calc_fixings(total_panels)
    edge = total_panels * 2
    
    rails = {}
    if total_panels > 0:
        rails[250] = total_panels * 2
        rails[300] = total_panels
    
    return {
        "rails": rails,
        "conn": conn,
        "ear": ear,
        "mid": mid,
        "edge": edge,
        "total_panels": total_panels,
    }

# ---------- UI: PROJECT NAME ----------
st.markdown('<div class="section-header">שם פרויקט</div>', unsafe_allow_html=True)
project_name = st.text_input(
    "",
    value=st.session_state.project_name,
    key="project_name_input",
    label_visibility="collapsed",
    placeholder="הזן שם פרויקט"
)
st.session_state.project_name = project_name

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# ---------- UI: PANEL SELECTION ----------
st.markdown('<div class="section-header">סוג פאנל</div>', unsafe_allow_html=True)

# Сортируем панели
panel_options = sorted(panels["name"].unique().tolist())
default_index = 0
if st.session_state.panel_name in panel_options:
    default_index = panel_options.index(st.session_state.panel_name)

panel_name = st.selectbox(
    "",
    panel_options,
    index=default_index,
    key="panel_select",
    label_visibility="collapsed",
    help="בחר את סוג הפאנל"
)
st.session_state.panel_name = panel_name

# Получаем данные выбранной панели
panel_row = panels[panels["name"] == panel_name].iloc[0] if not panels.empty else None

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# ---------- UI: GROUPS ----------
st.markdown('<div class="section-header">קבוצות פאנלים</div>', unsafe_allow_html=True)

# Отображаем текущие группы
groups = st.session_state.groups
for i, (num, direction) in enumerate(groups):
    col1, col2, col3 = st.columns([3, 3, 1])
    
    with col1:
        new_num = st.number_input(
            "כמות פאנלים",
            min_value=0,
            value=num,
            key=f"group_num_{i}",
            label_visibility="collapsed",
            placeholder="כמות"
        )
    
    with col2:
        new_dir = st.selectbox(
            "כיוון",
            ["עומד", "שוכב"],
            index=0 if direction == "עומד" else 1,
            key=f"group_dir_{i}",
            label_visibility="collapsed"
        )
    
    with col3:
        if st.button("✕", key=f"del_{i}", help="מחק שורה"):
            if len(groups) > 1:
                groups.pop(i)
                st.session_state.groups = groups
                st.rerun()

    # Обновляем группу
    if i < len(groups):
        groups[i] = (new_num, new_dir)

# Кнопка добавления группы
if st.button("+ הוסף שורה", use_container_width=True):
    groups.append((0, "עומד"))
    st.session_state.groups = groups
    st.rerun()

st.session_state.groups = groups

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# ---------- CALCULATE BUTTON ----------
st.markdown('<div class="primary-btn"></div>', unsafe_allow_html=True)
if st.button("חשב", type="primary", use_container_width=True):
    # Выполняем расчет
    if panel_row is not None:
        # Фильтруем пустые группы
        valid_groups = [(num, dir) for num, dir in groups if num > 0]
        
        if valid_groups:
            st.session_state.calc_result = do_calculation(panel_row, valid_groups)
            st.session_state.just_calculated = True
            st.rerun()
        else:
            st.warning("אנא הזן לפחות קבוצה אחת עם פאנלים")
    else:
        st.error("לא נמצא פאנל נבחר")

# Показываем сообщение об успехе
if st.session_state.get("just_calculated"):
    st.success("החישוב הושלם!")
    st.session_state.just_calculated = False

# ---------- DISPLAY RESULTS ----------
calc_result = st.session_state.calc_result
if calc_result is not None:
    st.markdown('<div class="section-header">תוצאות החישוב</div>', unsafe_allow_html=True)
    
    # Показываем общее количество панелей
    st.info(f"סה״כ פאנלים: **{calc_result['total_panels']}**")
    
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    
    # ---------- RAILS ----------
    st.markdown('<div style="font-weight:600; text-align:right; margin:16px 0 8px 0;">קושרות</div>', unsafe_allow_html=True)
    
    rails = calc_result.get("rails", {})
    if rails:
        for length in sorted(rails.keys(), reverse=True):
            qty = rails[length]
            col1, col2 = st.columns([3, 1])
            with col1:
                st.markdown(f"<div style='text-align:right; padding:8px 0;'>{length} ס״מ</div>", unsafe_allow_html=True)
            with col2:
                new_qty = st.number_input(
                    "",
                    min_value=0,
                    value=int(qty),
                    key=f"rail_{st.session_state.koshrot_boxes_version}_{length}",
                    label_visibility="collapsed"
                )
                # Сохраняем изменения
                if length in st.session_state.koshrot_qty:
                    st.session_state.koshrot_qty[length] = new_qty
    else:
        st.markdown("<div style='text-align:right; color:#718096; padding:12px 0;'>אין קושרות מחושבות</div>", unsafe_allow_html=True)
    
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    
    # ---------- FASTENERS ----------
    st.markdown('<div style="font-weight:600; text-align:right; margin:16px 0 8px 0;">פרזול</div>', unsafe_allow_html=True)
    
    # Базовые значения
    fasteners_base = [
        ("מהדק הארקה", calc_result.get("ear", 0)),
        ("מהדק אמצע", calc_result.get("mid", 0)),
        ("מהדק קצה", calc_result.get("edge", 0)),
        ("פקק לקושרות", calc_result.get("edge", 0)),
        ("מחברי קושרות", calc_result.get("conn", 0)),
    ]
    
    # Инициализируем если нужно
    if not st.session_state.fasteners:
        st.session_state.fasteners = {name: qty for name, qty in fasteners_base if qty > 0}
    
    # Отображаем
    for i, (name, base_qty) in enumerate(fasteners_base):
        if base_qty > 0 or name in st.session_state.fasteners:
            current_qty = st.session_state.fasteners.get(name, base_qty)
            
            col1, col2 = st.columns([3, 1])
            with col1:
                st.markdown(f"<div style='text-align:right; padding:8px 0;'>{name}</div>", unsafe_allow_html=True)
            with col2:
                new_qty = st.number_input(
                    "",
                    min_value=0,
                    value=int(current_qty),
                    key=f"fast_{st.session_state.fasteners_version}_{i}",
                    label_visibility="collapsed"
                )
                st.session_state.fasteners[name] = new_qty
    
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    
    # ---------- CHANNELS ----------
    st.markdown('<div style="font-weight:600; text-align:right; margin:16px 0 8px 0;">תעלות עם מכסים (מטר)</div>', unsafe_allow_html=True)
    
    for i, row in channels_df.iterrows():
        name = row["name"]
        current_qty = st.session_state.channels.get(name, 0.0)
        
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown(f"<div style='text-align:right; padding:8px 0;'>{name}</div>", unsafe_allow_html=True)
        with col2:
            new_qty = st.number_input(
                "",
                min_value=0.0,
                value=float(current_qty),
                step=1.0,
                format="%.1f",
                key=f"channel_{i}",
                label_visibility="collapsed"
            )
            if new_qty > 0:
                st.session_state.channels[name] = new_qty
            elif name in st.session_state.channels:
                del st.session_state.channels[name]
    
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    
    # ---------- EXPORT BUTTONS ----------
    st.markdown('<div style="font-weight:600; text-align:right; margin:16px 0 8px 0;">ייצוא דו״ח</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("שמור PDF", use_container_width=True, help="שמירת הדו״ח כקובץ PDF"):
            st.info("פונקציה זו תתווסף בגרסה הבאה")
    
    with col2:
        if st.button("שלח דו״ח", type="primary", use_container_width=True, help="שליחת הדו״ח בוואטסאפ"):
            # Формируем текст отчета
            materials_text = "חומרים מחושבים:\n"
            
            # Добавляем рейки
            if rails:
                materials_text += "\nקושרות:\n"
                for length, qty in sorted(rails.items(), reverse=True):
                    materials_text += f"• {qty} × {length} ס״מ\n"
            
            # Добавляем крепеж
            if st.session_state.fasteners:
                materials_text += "\nפרזול:\n"
                for name, qty in st.session_state.fasteners.items():
                    if qty > 0:
                        materials_text += f"• {name}: {qty}\n"
            
            # Добавляем каналы
            if st.session_state.channels:
                materials_text += "\nתעלות:\n"
                for name, qty in st.session_state.channels.items():
                    if qty > 0:
                        materials_text += f"• {name}: {qty} מ׳\n"
            
            # Формируем сообщение для WhatsApp
            whatsapp_msg = format_whatsapp_message(
                project_name=project_name,
                panel_name=panel_name,
                groups=[(num, dir) for num, dir in groups if num > 0],
                materials_text=materials_text
            )
            
            # Кодируем для URL
            encoded_msg = urllib.parse.quote(whatsapp_msg)
            whatsapp_url = f"https://wa.me/?text={encoded_msg}"
            
            # Показываем ссылку
            st.markdown(f"""
            <div style='background:#f0f9ff; padding:16px; border-radius:8px; border:1px solid #e0f2fe; margin:12px 0;'>
                <div style='text-align:right; font-weight:500; margin-bottom:12px;'>הדו״ח מוכן לשליחה</div>
                <a href='{whatsapp_url}' target='_blank' style='
                    display: block;
                    background: #25D366;
                    color: white;
                    text-align: center;
                    padding: 14px;
                    border-radius: 6px;
                    text-decoration: none;
                    font-weight: 500;
                    margin: 8px 0;
                '>
                    פתח בוואטסאפ
                </a>
                <div style='text-align:right; font-size:14px; color:#475569; margin-top:12px;'>
                    או העתק קישור:
                </div>
                <div style='
                    background: white;
                    border: 1px solid #e2e8f0;
                    border-radius: 6px;
                    padding: 12px;
                    margin: 8px 0;
                    font-size: 14px;
                    color: #475569;
                    word-break: break-all;
                    text-align: right;
                '>
                    {whatsapp_url[:60]}...
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Автоматическое открытие WhatsApp на мобильных
            components.html(f"""
            <script>
            if (window.innerWidth <= 768) {{
                window.open("{whatsapp_url}", "_blank");
            }}
            </script>
            """, height=0)

# ---------- FOOTER ----------
st.markdown("""
<div style='
    margin-top: 40px;
    padding-top: 20px;
    border-top: 1px solid #e2e8f0;
    text-align: center;
    color: #718096;
    font-size: 14px;
'>
    סולארי - חישוב חומרים למערכות סולאריות
</div>
""", unsafe_allow_html=True)

# ---------- PWA CONFIG ----------
# Добавляем PWA манифест
components.html("""
<link rel="manifest" href="/manifest.json">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="theme-color" content="#4b75c9">
""", height=0)
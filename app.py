import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import math
import json
import urllib.parse
import os

# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="סולארי - חישוב חומרים",
    page_icon="📐",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ---------- CUSTOM STYLES ----------
st.markdown("""
<style>
    .main {
        padding: 20px;
        max-width: 800px;
        margin: 0 auto;
    }
    
    .section-header {
        font-size: 18px;
        font-weight: 600;
        color: var(--text-color);
        margin: 24px 0 12px 0;
        text-align: right;
        padding-bottom: 6px;
        border-bottom: 2px solid var(--secondary-background-color);
    }
    
    .divider {
        border-top: 1px solid var(--border-color);
        margin: 20px 0;
    }
    
    /* ВЕСЕЛОЕ СООБЩЕНИЕ С АНИМАЦИЕЙ */
    .funny-message {
        background-color: #fffbeb;
        border: 2px solid #fbbf24;
        border-radius: 10px;
        padding: 12px 16px;
        margin: 10px 0;
        text-align: right;
        font-size: 15px;
        color: #92400e;
        font-weight: 500;
        animation: bounce 0.8s ease;
        box-shadow: 0 4px 12px rgba(251, 191, 36, 0.2);
    }
    
    @keyframes bounce {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-5px); }
    }
    
    /* CSS переменные */
    :root {
        --background-color: #ffffff;
        --text-color: #31333F;
        --border-color: #DCDCDC;
        --secondary-bg: #F0F2F6;
        --primary-color: #FF4B4B;
        --hover-color: #EC5953;
        --radius: 8px;
    }
    
    @media (prefers-color-scheme: dark) {
        :root {
            --background-color: #0E1117;
            --text-color: #FAFAFA;
            --border-color: #2D3748;
            --secondary-bg: #1E293B;
        }
    }
</style>
""", unsafe_allow_html=True)

# ---------- SESSION STATE INIT ----------
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
if "manual_rails_prev" not in st.session_state:
    st.session_state.manual_rails_prev = {}
if "fasteners_version" not in st.session_state:
    st.session_state.fasteners_version = 0
if "fasteners" not in st.session_state:
    st.session_state.fasteners = None
if "fasteners_include" not in st.session_state:
    st.session_state.fasteners_include = None
if "koshrot_qty" not in st.session_state:
    st.session_state.koshrot_qty = None
if "show_report" not in st.session_state:
    st.session_state.show_report = False
if "show_funny_message" not in st.session_state:
    st.session_state.show_funny_message = {"rows": False, "panels": False}
if "funny_message_text" not in st.session_state:
    st.session_state.funny_message_text = ""
if "groups_data" not in st.session_state:
    st.session_state.groups_data = {"standing": [], "laying": []}

# ---------- LOAD DATABASES ----------
@st.cache_data
def load_data():
    if not os.path.exists("panels.csv"):
        with open("panels.csv", "w", encoding="utf-8") as f:
            f.write("name,width,height\nTadiran 595,113.4,227.8\nJinko 640,113.4,238.2")
    
    if not os.path.exists("channels.csv"):
        with open("channels.csv", "w", encoding="utf-8") as f:
            f.write("unit,name\nמטר,רשת 50\nמטר,רשת 100\nמטר,פח 60*40 לבן\nמטר,פח 100*60 לבן\nמטר,פח 60*40\nמטר,פח 100*60")
    
    if not os.path.exists("parts.csv"):
        with open("parts.csv", "w", encoding="utf-8") as f:
            f.write("name,unit\nאומגה לגג איסכורית,יח׳\nתעלת פלסטיק 40*40,מטר")
    
    panels = pd.read_csv("panels.csv")
    channels = pd.read_csv("channels.csv")
    parts = pd.read_csv("parts.csv")
    panels["name"] = panels["name"].astype(str)
    return panels, channels, parts

panels, channels_df, parts = load_data()

# ---------- HELPER FUNCTIONS ----------
def right_label(text: str) -> str:
    return f'<div style="text-align:right; font-weight:500; margin-bottom:8px;">{text}</div>'

def right_header(text: str) -> str:
    return f'<h3 style="text-align:right; margin-bottom:0.5rem;">{text}</h3>'

def round_up_to_tens(x: float) -> int:
    if x <= 0:
        return 0
    return int(math.ceil(x / 10.0) * 10)

def normalize_length_key(length) -> str:
    if length is None:
        return ""
    s = str(length).strip().replace(",", ".")
    if s == "":
        return ""
    try:
        f = float(s)
        if f.is_integer():
            return str(int(f))
        return f"{f}".rstrip("0").rstrip(".")
    except Exception:
        return ""

def length_sort_key(length_key: str) -> float:
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

def check_and_show_funny_message(value: int, field_type: str):
    if value > 99:
        if field_type == "rows":
            message = f"אל תגזים אחי, איזה [{value}] שורות במערכת ביתית? 😅"
        else:
            message = f"וואי [{value}] פאנלים בשורה אחת? אולי תפצל לשתי שורות? 😄"
        
        st.session_state.show_funny_message[field_type] = True
        st.session_state.funny_message_text = message
        return True
    return False

# ---------- ENGINE FUNCTIONS ----------
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

def format_whatsapp_message(project_name, panel_name, groups, materials_text):
    message = f"""דו״ח חומרים למערכת סולארית

פרויקט: {project_name}
סוג פאנל: {panel_name}

קבוצות פאנלים:
"""
    
    for i, (n, g, o) in enumerate(groups, 1):
        if n > 0 and g > 0:
            message += f"שורה {i}: {n} פאנלים {o} (x{g})\n"
    
    message += f"\n{materials_text}\n"
    message += "הדו״ח נוצר באפליקציית סולארי"
    
    return message

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
)
st.session_state.panel_name = panel_name

panel_rows = panels[panels["name"] == panel_name]
if panel_rows.empty:
    st.error("הפאנל שנבחר לא נמצא")
    st.stop()
panel = panel_rows.iloc[0]

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# ---------- GROUPS SECTION ----------
st.markdown(right_header("קבוצות פאנלים"), unsafe_allow_html=True)

if st.session_state.show_funny_message.get("rows") or st.session_state.show_funny_message.get("panels"):
    st.markdown(f'<div class="funny-message">{st.session_state.funny_message_text}</div>', unsafe_allow_html=True)

# HTML компонент с localStorage
groups_component = """
<!DOCTYPE html>
<html dir="rtl">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }
        
        :root {
            --bg: #F0F2F6;
            --text: #31333F;
            --border: #DCDCDC;
            --hover: #EC5953;
            --radius: 8px;
            --height: 38px;
        }
        
        @media (prefers-color-scheme: dark) {
            :root {
                --bg: #1E293B;
                --text: #FAFAFA;
                --border: #2D3748;
            }
        }
        
        .container {
            width: 100%;
            max-width: 800px;
            margin: 0 auto;
            padding: 0 8px;
        }
        
        .spoiler-section {
            margin-bottom: 20px;
        }
        
        .spoiler-header {
            font-size: 16px;
            font-weight: 600;
            color: var(--text);
            margin-bottom: 12px;
            padding-bottom: 4px;
            border-bottom: 1px solid var(--border);
        }
        
        .columns-header {
            display: flex;
            width: 100%;
            margin-bottom: 6px;
            font-size: 13px;
            font-weight: 500;
            color: var(--text);
            opacity: 0.7;
        }
        
        .column-label {
            flex: 1;
            text-align: center;
            padding: 0 4px;
        }
        
        .row {
            display: flex;
            width: 100%;
            margin-bottom: 8px;
            gap: 6px;
        }
        
        .input-wrapper {
            flex: 1;
            position: relative;
            min-width: 0;
        }
        
        .input-group {
            display: flex;
            width: 100%;
            height: var(--height);
            background: var(--bg);
            border-radius: var(--radius);
            overflow: hidden;
        }
        
        .number-input {
            flex: 1;
            min-width: 0;
            width: 100%;
            border: none;
            background: transparent;
            color: var(--text);
            font-size: 14px;
            text-align: center;
            padding: 0 8px;
            outline: none;
            font-family: inherit;
        }
        
        .number-input::-webkit-inner-spin-button,
        .number-input::-webkit-outer-spin-button {
            -webkit-appearance: none;
            margin: 0;
        }
        
        .btn-group {
            display: flex;
            border-left: 1px solid var(--border);
        }
        
        .btn {
            width: 32px;
            height: 100%;
            background: var(--bg);
            border: none;
            color: var(--text);
            font-size: 16px;
            font-weight: bold;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            transition: background 0.2s;
            user-select: none;
        }
        
        .btn:hover {
            background: var(--hover) !important;
            color: white !important;
        }
        
        .btn:active {
            opacity: 0.9;
        }
        
        .add-row-btn {
            background: #4b75c9;
            color: white;
            border: none;
            border-radius: var(--radius);
            padding: 8px 16px;
            font-size: 14px;
            cursor: pointer;
            margin-top: 8px;
            transition: background 0.2s;
        }
        
        .add-row-btn:hover {
            background: #3a62b5;
        }
        
        .save-btn {
            background: #4b75c9;
            color: white;
            border: none;
            border-radius: var(--radius);
            padding: 12px 24px;
            font-size: 16px;
            font-weight: 500;
            cursor: pointer;
            width: 100%;
            margin: 20px 0;
            transition: background 0.2s;
        }
        
        .save-btn:hover {
            background: #3a62b5;
        }
        
        @media (max-width: 768px) {
            .row {
                gap: 4px;
                margin-bottom: 6px;
            }
            
            .number-input {
                font-size: 13px;
                padding: 0 6px;
            }
            
            .btn {
                width: 28px;
                font-size: 14px;
            }
            
            :root {
                --height: 36px;
            }
        }
        
        @media (max-width: 480px) {
            .row {
                gap: 3px;
            }
            
            .number-input {
                font-size: 12px;
                padding: 0 4px;
            }
            
            .btn {
                width: 26px;
            }
            
            :root {
                --height: 34px;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <!-- СПОЙЛЕР 1: СТОЯЧИЕ ПАНЕЛИ -->
        <div class="spoiler-section">
            <div class="spoiler-header">עומד</div>
            <div class="columns-header">
                <div class="column-label">פאנלים</div>
                <div class="column-label">שורות</div>
            </div>
            <div id="standing-rows"></div>
            <button class="add-row-btn" onclick="addRow('standing')">עוד שורה</button>
        </div>
        
        <!-- СПОЙЛЕР 2: ЛЕЖАЧИЕ ПАНЕЛИ -->
        <div class="spoiler-section">
            <div class="spoiler-header">שוכב</div>
            <div class="columns-header">
                <div class="column-label">פאנלים</div>
                <div class="column-label">שורות</div>
            </div>
            <div id="laying-rows"></div>
            <button class="add-row-btn" onclick="addRow('laying')">עוד שורה</button>
        </div>
        
        <button class="save-btn" onclick="saveAllData()">שמור וחשב</button>
    </div>

    <script>
        // Инициализация данных
        let standingRows = 8;
        let layingRows = 4;
        const data = {
            standing: {},
            laying: {}
        };
        
        // Загружаем из localStorage
        function loadFromStorage() {
            const saved = localStorage.getItem('solar_groups_data');
            if (saved) {
                const parsed = JSON.parse(saved);
                if (parsed.standingRows) standingRows = parsed.standingRows;
                if (parsed.layingRows) layingRows = parsed.layingRows;
                if (parsed.data) {
                    Object.assign(data.standing, parsed.data.standing || {});
                    Object.assign(data.laying, parsed.data.laying || {});
                }
            }
            
            // Предустановленные значения для стоячих (1-8)
            for (let i = 1; i <= standingRows; i++) {
                if (!data.standing[`n_${i}`]) {
                    data.standing[`n_${i}`] = i <= 8 ? i : 0;
                }
                if (!data.standing[`g_${i}`]) {
                    data.standing[`g_${i}`] = 0;
                }
            }
            
            // Предустановленные значения для лежачих (1-4)
            for (let i = 1; i <= layingRows; i++) {
                if (!data.laying[`n_${i}`]) {
                    data.laying[`n_${i}`] = i <= 4 ? i : 0;
                }
                if (!data.laying[`g_${i}`]) {
                    data.laying[`g_${i}`] = 0;
                }
            }
        }
        
        // Сохраняем в localStorage
        function saveToStorage() {
            localStorage.setItem('solar_groups_data', JSON.stringify({
                standingRows,
                layingRows,
                data
            }));
        }
        
        // Создаем строку с двумя инпутами
        function createRow(type, index, nValue, gValue) {
            return `
                <div class="row">
                    <div class="input-wrapper">
                        <div class="input-group">
                            <input type="number" 
                                   id="${type}_n_${index}" 
                                   class="number-input" 
                                   value="${nValue}" 
                                   min="0" 
                                   max="99"
                                   oninput="updateValue('${type}', 'n', ${index}, this.value)">
                            <div class="btn-group">
                                <button class="btn" onclick="updateNumber('${type}_n_${index}', -1)">−</button>
                                <button class="btn" onclick="updateNumber('${type}_n_${index}', 1)">+</button>
                            </div>
                        </div>
                    </div>
                    <div class="input-wrapper">
                        <div class="input-group">
                            <input type="number" 
                                   id="${type}_g_${index}" 
                                   class="number-input" 
                                   value="${gValue}" 
                                   min="0" 
                                   max="99"
                                   oninput="updateValue('${type}', 'g', ${index}, this.value)">
                            <div class="btn-group">
                                <button class="btn" onclick="updateNumber('${type}_g_${index}', -1)">−</button>
                                <button class="btn" onclick="updateNumber('${type}_g_${index}', 1)">+</button>
                            </div>
                        </div>
                    </div>
                </div>
            `;
        }
        
        // Отображаем строки
        function renderRows() {
            const standingContainer = document.getElementById('standing-rows');
            const layingContainer = document.getElementById('laying-rows');
            
            let standingHtml = '';
            for (let i = 1; i <= standingRows; i++) {
                const nValue = data.standing[`n_${i}`] || (i <= 8 ? i : 0);
                const gValue = data.standing[`g_${i}`] || 0;
                standingHtml += createRow('standing', i, nValue, gValue);
            }
            
            let layingHtml = '';
            for (let i = 1; i <= layingRows; i++) {
                const nValue = data.laying[`n_${i}`] || (i <= 4 ? i : 0);
                const gValue = data.laying[`g_${i}`] || 0;
                layingHtml += createRow('laying', i, nValue, gValue);
            }
            
            standingContainer.innerHTML = standingHtml;
            layingContainer.innerHTML = layingHtml;
        }
        
        // Обновление значения
        function updateValue(type, field, index, value) {
            const numValue = parseInt(value) || 0;
            const clampedValue = Math.min(Math.max(numValue, 0), 99);
            
            data[type][`${field}_${index}`] = clampedValue;
            saveToStorage();
            
            // Обновляем отображаемое значение
            const input = document.getElementById(`${type}_${field}_${index}`);
            if (input) {
                input.value = clampedValue;
            }
        }
        
        // Обновление числа с кнопок
        function updateNumber(fieldId, delta) {
            const input = document.getElementById(fieldId);
            if (!input) return;
            
            const [type, field, index] = fieldId.split('_');
            let value = parseInt(input.value) || 0;
            value += delta;
            
            updateValue(type, field, parseInt(index), value);
        }
        
        // Добавление строки
        function addRow(type) {
            if (type === 'standing') {
                standingRows++;
                data.standing[`n_${standingRows}`] = 0;
                data.standing[`g_${standingRows}`] = 0;
            } else {
                layingRows++;
                data.laying[`n_${layingRows}`] = 0;
                data.laying[`g_${layingRows}`] = 0;
            }
            
            saveToStorage();
            renderRows();
        }
        
        // Сохранение всех данных и отправка в Streamlit
        function saveAllData() {
            saveToStorage();
            
            // Подготавливаем данные для отправки
            const groups = [];
            
            // Стоячие группы
            for (let i = 1; i <= standingRows; i++) {
                const n = data.standing[`n_${i}`] || 0;
                const g = data.standing[`g_${i}`] || 0;
                if (n > 0 && g > 0) {
                    groups.push({n, g, o: 'עומד'});
                }
            }
            
            // Лежачие группы
            for (let i = 1; i <= layingRows; i++) {
                const n = data.laying[`n_${i}`] || 0;
                const g = data.laying[`g_${i}`] || 0;
                if (n > 0 && g > 0) {
                    groups.push({n, g, o: 'שוכב'});
                }
            }
            
            // Отправляем в Streamlit через postMessage
            if (window.parent) {
                window.parent.postMessage({
                    type: 'streamlit:setComponentValue',
                    value: groups
                }, '*');
            }
            
            // Показываем сообщение
            alert('הנתונים נשמרו! לחץ על "חשב" כדי לעדכן את החישוב.');
        }
        
        // Инициализация
        function init() {
            loadFromStorage();
            renderRows();
            
            // Отправляем сообщение о готовности
            setTimeout(() => {
                if (window.parent) {
                    window.parent.postMessage({
                        type: 'streamlit:componentReady',
                        value: true
                    }, '*');
                }
            }, 100);
        }
        
        // Запускаем при загрузке
        document.addEventListener('DOMContentLoaded', init);
    </script>
</body>
</html>
"""

# Отображаем компонент
components.html(groups_component, height=600)

# Компонент для получения данных
components.html("""
<script>
// Обработчик сообщений от компонента
window.addEventListener('message', function(event) {
    if (event.data.type === 'streamlit:setComponentValue') {
        // Сохраняем данные в sessionStorage для передачи в Streamlit
        sessionStorage.setItem('groups_data', JSON.stringify(event.data.value));
        
        // Отправляем команду на обновление
        window.parent.postMessage({
            type: 'streamlit:setComponentValue',
            value: event.data.value
        }, '*');
    }
});
</script>
""", height=0)

# Получаем данные из sessionStorage через JavaScript
get_data_js = """
<script>
// Проверяем есть ли сохраненные данные
const savedData = sessionStorage.getItem('groups_data');
if (savedData) {
    // Отправляем в Streamlit
    window.parent.postMessage({
        type: 'streamlit:setComponentValue',
        value: JSON.parse(savedData)
    }, '*');
    
    // Очищаем storage
    sessionStorage.removeItem('groups_data');
}
</script>
"""

st.markdown(get_data_js, unsafe_allow_html=True)

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# ---------- BUTTON: CALCULATE ----------
st.markdown('<div style="background-color: #4b75c9; font-size: 17px; font-weight: 600; padding: 16px; margin: 20px 0; text-align: center; color: white; border-radius: 6px;">חשב</div>', unsafe_allow_html=True)

if st.button("חשב", type="primary", use_container_width=True, key="calculate_main"):
    # Пытаемся получить данные из компонента
    groups_data = []
    
    # Проверяем session_state
    if 'component_groups' in st.session_state:
        groups_data = st.session_state.component_groups
    
    # Если нет данных, используем предустановленные
    if not groups_data:
        # Стоячие группы
        for i in range(1, 9):
            groups_data.append({"n": i, "g": 0, "o": "עומד"})
        # Лежачие группы
        for i in range(1, 5):
            groups_data.append({"n": i, "g": 0, "o": "שוכב"})
    
    # Фильтруем только группы с данными
    valid_groups = [(item["n"], item["g"], item["o"]) for item in groups_data if item["n"] > 0 and item["g"] > 0]
    
    # Сброс состояния
    st.session_state.koshrot_qty = None
    st.session_state.koshrot_boxes_version += 1
    st.session_state.manual_rows = 1
    st.session_state.manual_deleted_rows = set()
    st.session_state.manual_rails = {}
    st.session_state.manual_rails_prev = {}
    st.session_state.manual_form_version += 1
    
    if valid_groups:
        st.session_state.calc_result = do_calculation(panel, valid_groups)
    else:
        st.session_state.calc_result = {
            "auto_rails": {},
            "conn": 0,
            "ear": 0,
            "mid": 0,
            "edge": 0,
            "total_panels": 0,
        }
    
    st.session_state.koshrot_qty = None
    st.session_state["fasteners"] = None
    st.session_state["fasteners_include"] = None
    st.session_state.fasteners_version += 1
    
    st.session_state.just_calculated = True
    st.rerun()

if st.session_state.get("just_calculated"):
    st.success("החישוב עודכן!")
    st.session_state.just_calculated = False

calc_result = st.session_state.calc_result

# ---------- MANUAL RAILS ----------
st.markdown(right_header("קושרות (הוספה ידנית)"), unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)
col1.markdown('<div style="font-size: 12px; text-align: center;">אורך (ס״מ)</div>', unsafe_allow_html=True)
col2.markdown('<div style="font-size: 12px; text-align: center;">כמות</div>', unsafe_allow_html=True)
col3.markdown('<div style="font-size: 12px; text-align: center;">&nbsp;</div>', unsafe_allow_html=True)

manual_rows = st.session_state.manual_rows
for j in range(1, manual_rows + 1):
    col1, col2, col3 = st.columns(3)
    
    with col1:
        length = st.number_input(
            "אורך",
            min_value=0,
            max_value=10000,
            step=10,
            key=f"m_len_{st.session_state.manual_form_version}_{j}",
            label_visibility="collapsed",
            placeholder="ס״מ"
        )
    
    with col2:
        qty = st.number_input(
            "כמות",
            min_value=0,
            max_value=1000,
            step=1,
            key=f"m_qty_{st.session_state.manual_form_version}_{j}",
            label_visibility="collapsed",
            placeholder="מספר"
        )
    
    with col3:
        if j == 1:
            st.markdown('<div style="font-size: 12px; text-align: right;">להוסיף קושרות</div>', unsafe_allow_html=True)

if st.button("להוסיף עוד קושרות", key="add_manual_rails"):
    st.session_state.manual_rows += 1
    st.rerun()

# Собираем ручные рейки
manual_rails_dict = {}
for j in range(1, st.session_state.manual_rows + 1):
    if j in st.session_state.manual_deleted_rows:
        continue
    length = st.session_state.get(f"m_len_{st.session_state.manual_form_version}_{j}", 0)
    qty = st.session_state.get(f"m_qty_{st.session_state.manual_form_version}_{j}", 0)
    if length and qty:
        manual_rails_dict[length] = manual_rails_dict.get(length, 0) + qty

st.session_state.manual_rails = manual_rails_dict

prev_manual = st.session_state.get("manual_rails_prev", {})
curr_manual = st.session_state.manual_rails

if st.session_state.get("koshrot_qty") is not None:
    for length in set(list(prev_manual.keys()) + list(curr_manual.keys())):
        prev_q = int(prev_manual.get(length, 0) or 0)
        curr_q = int(curr_manual.get(length, 0) or 0)
        d = curr_q - prev_q
        if d == 0:
            continue
        k = normalize_length_key(length)
        new_val = max(int(st.session_state.koshrot_qty.get(k, 0) or 0) + d, 0)
        st.session_state.koshrot_qty[k] = new_val
        st.session_state[f"koshrot_qty_{st.session_state.koshrot_boxes_version}_{k}"] = new_val

st.session_state.manual_rails_prev = dict(curr_manual)

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# ---------- SHOW CALC RESULT ----------
if calc_result is not None:
    auto_rails = calc_result["auto_rails"]
    manual_rails = st.session_state.manual_rails
    
    st.write(f"סה\"כ פאנלים: {calc_result['total_panels']}")
    
    # קושרות
    with st.expander("קושרות", expanded=True):
        rails_base = {}
        for length, qty in auto_rails.items():
            klen = normalize_length_key(length)
            rails_base[klen] = rails_base.get(klen, 0) + int(qty)
        for length, qty in manual_rails.items():
            klen = normalize_length_key(length)
            rails_base[klen] = rails_base.get(klen, 0) + int(qty)
        
        if st.session_state.koshrot_qty is None:
            st.session_state.koshrot_qty = dict(rails_base)
        else:
            for length, qty in rails_base.items():
                if length not in st.session_state.koshrot_qty:
                    st.session_state.koshrot_qty[length] = qty
        
        if st.session_state.koshrot_qty:
            for length in sorted(st.session_state.koshrot_qty.keys(), key=length_sort_key, reverse=True):
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.markdown(f"**{length} ס״מ**")
                with col2:
                    qty_key = f"koshrot_qty_{st.session_state.koshrot_boxes_version}_{length}"
                    default_val = int(st.session_state.koshrot_qty.get(length, 0))
                    qty_val = st.number_input(
                        "",
                        min_value=0,
                        value=default_val,
                        step=1,
                        key=qty_key,
                        label_visibility="collapsed"
                    )
                    st.session_state.koshrot_qty[length] = int(qty_val)
    
    # פרזול
    with st.expander("פרזול", expanded=True):
        ear = calc_result["ear"]
        mid = calc_result["mid"]
        edge = calc_result["edge"]
        conn = calc_result["conn"]
        total_panels = calc_result["total_panels"]
        
        rails_total = {}
        for length, qty in auto_rails.items():
            rails_total[length] = rails_total.get(length, 0) + qty
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
        
        fasteners_base = [
            ("מהדק הארקה", ear),
            ("מהדק אמצע", mid),
            ("מהדק קצה", edge),
            ("פקק לקושרות", edge),
            ("מחברי קושרות", conn),
            ("בורג איסכורית 3,5", screws_iso),
            ("M8 בורג", m8_count),
            ("אום M8", m8_count),
        ]
        
        if st.session_state.get("fasteners_include") is None:
            st.session_state["fasteners_include"] = {name: True for name, _ in fasteners_base}
        
        if st.session_state.get("fasteners") is None:
            st.session_state["fasteners"] = {lbl: int(val) for (lbl, val) in fasteners_base}
        
        for i, (lbl, base_val) in enumerate(fasteners_base):
            current_val = int(st.session_state["fasteners"].get(lbl, base_val) or 0)
            if int(base_val) == 0 and current_val == 0:
                continue
            
            c_chk, c_val, c_name = st.columns([0.8, 1.6, 5])
            
            with c_chk:
                inc_key = f"fast_inc_{st.session_state.fasteners_version}_{lbl}"
                inc_default = bool(st.session_state["fasteners_include"].get(lbl, True))
                inc_val = st.checkbox("", value=inc_default, key=inc_key, label_visibility="collapsed")
                st.session_state["fasteners_include"][lbl] = bool(inc_val)
            
            with c_val:
                v = st.number_input(
                    "",
                    min_value=0,
                    value=int(current_val),
                    step=1,
                    key=f"fastener_qty_{st.session_state.fasteners_version}_{i}_{lbl}",
                    label_visibility="collapsed",
                )
            
            with c_name:
                st.markdown(f'<div style="text-align: right; font-weight: 500;"><strong>{lbl}</strong></div>', unsafe_allow_html=True)
            
            st.session_state["fasteners"][lbl] = int(v)
    
    # תעלות
    with st.expander("תעלות עם מכסים", expanded=False):
        channel_order = {}
        for i, r in channels_df.iterrows():
            name = r["name"]
            unit = r.get("unit", "מטר")
            
            if "רשת" in name:
                step_value = 3.0
            elif "פח" in name:
                step_value = 2.5
            else:
                step_value = 1.0
            
            col1, col2 = st.columns([3, 1])
            with col1:
                st.markdown(f"**{name}**")
            with col2:
                saved_value = 0.0
                if name in st.session_state.channel_order:
                    if isinstance(st.session_state.channel_order[name], dict):
                        saved_value = st.session_state.channel_order[name].get("qty", 0.0)
                    else:
                        saved_value = float(st.session_state.channel_order[name])
                
                q = st.number_input(
                    "",
                    min_value=0.0,
                    value=float(saved_value),
                    step=step_value,
                    format="%g",
                    key=f"channel_{i}",
                    label_visibility="collapsed",
                )
            
            if q > 0:
                channel_order[name] = {"qty": q, "unit": unit}
            elif name in st.session_state.channel_order:
                channel_order[name] = {"qty": 0.0, "unit": unit}
        
        st.session_state.channel_order = channel_order
    
    # פריטים נוספים
    with st.expander("פריטים נוספים", expanded=False):
        if not parts.empty:
            extra_rows = st.session_state.extra_rows
            chosen_entries = []
            names_list = parts["name"].tolist()
            
            for i in range(1, extra_rows + 1):
                col1, col2 = st.columns([3, 1])
                with col1:
                    part = st.selectbox(
                        "",
                        names_list,
                        key=f"extra_name_{i}",
                        label_visibility="collapsed",
                    )
                with col2:
                    qty = st.number_input(
                        "",
                        min_value=0,
                        step=1,
                        key=f"extra_qty_{i}",
                        label_visibility="collapsed",
                        placeholder="כמות"
                    )
                if qty > 0:
                    chosen_entries.append((part, qty))
            
            if st.button("להוסיף עוד פריט", key="add_extra"):
                st.session_state.extra_rows += 1
                st.rerun()
            
            agg = {}
            for name, qty in chosen_entries:
                agg[name] = agg.get(name, 0) + qty
            st.session_state.extra_parts = [
                {"name": n, "qty": q} for n, q in agg.items()
            ]
    
    # ---------- EXPORT ----------
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown(right_header('ייצוא דו״ח'), unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("שמור PDF", use_container_width=True):
            st.info("פונקציית PDF תתווסף בגרסה הבאה")
    
    with col2:
        if st.button("שלח דו״ח", type="primary", use_container_width=True):
            materials_text = ""
            
            if st.session_state.koshrot_qty:
                materials_text += "קושרות:\n"
                for length in sorted(st.session_state.koshrot_qty.keys(), key=length_sort_key, reverse=True):
                    qty = st.session_state.koshrot_qty[length]
                    if qty > 0:
                        materials_text += f"• {qty} × {length} ס״מ\n"
            
            fasteners_list = []
            if st.session_state.get("fasteners"):
                for lbl, val in st.session_state["fasteners"].items():
                    if val > 0 and st.session_state["fasteners_include"].get(lbl, True):
                        fasteners_list.append((lbl, val))
            
            if fasteners_list:
                materials_text += "\nפרזול:\n"
                for lbl, val in fasteners_list:
                    materials_text += f"• {lbl}: {val}\n"
            
            if st.session_state.channel_order:
                materials_text += "\nתעלות:\n"
                for name, data in st.session_state.channel_order.items():
                    if isinstance(data, dict):
                        qty = data.get("qty", 0)
                        unit = data.get("unit", "מטר")
                    else:
                        qty = data
                        unit = "מטר"
                    
                    if qty > 0:
                        materials_text += f"• {name}: {format_qty(qty)} {unit}\n"
            
            if st.session_state.extra_parts:
                materials_text += "\nפריטים נוספים:\n"
                for p in st.session_state.extra_parts:
                    unit = "יח׳"
                    part_row = parts[parts["name"] == p["name"]]
                    if not part_row.empty:
                        unit = part_row.iloc[0].get("unit", "יח׳")
                    
                    materials_text += f"• {p['name']}: {p['qty']} {unit}\n"
            
            # Используем предустановленные группы для примера
            valid_groups = []
            for i in range(1, 9):
                valid_groups.append((i, 0, "עומד"))
            for i in range(1, 5):
                valid_groups.append((i, 0, "שוכב"))
            
            valid_groups = [(n, g, o) for n, g, o in valid_groups if n > 0 and g > 0]
            
            whatsapp_msg = format_whatsapp_message(
                project_name=project_name,
                panel_name=panel_name,
                groups=valid_groups,
                materials_text=materials_text
            )
            
            encoded_msg = urllib.parse.quote(whatsapp_msg)
            whatsapp_url = f"https://wa.me/?text={encoded_msg}"
            
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
                    {whatsapp_url[:80]}...
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            components.html(f"""
            <script>
            if (window.innerWidth <= 768) {{
                window.open("{whatsapp_url}", "_blank");
            }}
            </script>
            """, height=0)

# ---------- AUTO CREATE FILES ----------
if not os.path.exists("manifest.json"):
    with open("manifest.json", "w", encoding="utf-8") as f:
        f.write("""{
  "name": "סולארי - חישוב חומרים",
  "short_name": "סולארי",
  "description": "חישוב חומרים למערכת סולארית",
  "start_url": "/",
  "display": "standalone",
  "background_color": "#ffffff",
  "theme_color": "#4b75c9",
  "icons": [
    {
      "src": "https://img.icons8.com/color/96/000000/sun--v1.png",
      "sizes": "96x96",
      "type": "image/png"
    },
    {
      "src": "https://img.icons8.com/color/192/000000/sun--v1.png",
      "sizes": "192x192",
      "type": "image/png"
    },
    {
      "src": "https://img.icons8.com/color/512/000000/sun--v1.png",
      "sizes": "512x512",
      "type": "image/png"
    }
  ]
}""")

components.html("""
<link rel="manifest" href="/manifest.json">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="theme-color" content="#4b75c9">
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
    סולארי © 2024 - חישוב חומרים למערכות סולאריות
</div>
""", unsafe_allow_html=True)

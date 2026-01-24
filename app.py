import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import math
import json

# ---------- SESSION STATE INIT (required) ----------
st.session_state.setdefault("fasteners", None)
# Инициализация для групп панелей
st.session_state.setdefault("vertical_rows", 8)  # Для вертикальных панелей
st.session_state.setdefault("horizontal_rows", 4)  # Для горизонтальных панелей

# ---------- ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ ----------

def right_label(text: str) -> str:
    return f'<div style="text-align:right; font-weight:bold;">{text}</div>'


def right_header(text: str) -> str:
    # крупный заголовок h3 по правому краю
    return f'<h3 style="text-align:right; margin-bottom:0.5rem;">{text}</h3>'


def clean_text(text: str) -> str:
    # убираем точки / троеточия в конце подсказок
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


# ---------- LOAD DATABASES ----------
panels = pd.read_csv("panels.csv")
channels = pd.read_csv("channels.csv")
parts = pd.read_csv("parts.csv")

panels["name"] = panels["name"].astype(str)

# ---------- SESSION STATE ----------
if "calc_result" not in st.session_state:
    st.session_state.calc_result = None

if "just_calculated" not in st.session_state:
    st.session_state.just_calculated = False

# Эти ключи уже инициализированы выше с помощью setdefault
# if "vertical_rows" not in st.session_state:
#     st.session_state.vertical_rows = 8
# 
# if "horizontal_rows" not in st.session_state:
#     st.session_state.horizontal_rows = 4

if "channel_order" not in st.session_state:
    st.session_state.channel_order = {}

if "extra_parts" not in st.session_state:
    st.session_state.extra_parts = []  # [{name, qty}]

if "manual_rows" not in st.session_state:
    st.session_state.manual_rows = 1

# bump this to force manual rails widgets to reset
if "manual_form_version" not in st.session_state:
    st.session_state.manual_form_version = 0

# bump this to force קושרות quantity boxes to reset
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

# snapshot of manual rails to compute deltas
if "manual_rails_prev" not in st.session_state:
    st.session_state.manual_rails_prev = {}


def round_up_to_tens(x: float) -> int:
    if x <= 0:
        return 0
    return int(math.ceil(x / 10.0) * 10)



def normalize_length_key(length) -> str:
    """Normalize a rail length key so 550, 550.0, '550', '550.0' map to '550'."""
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
        return s

def length_sort_key(length_key: str) -> float:
    """Sort helper: treat normalized length keys numerically (e.g., '30' < '295' < '300')."""
    try:
        return float(str(length_key).replace(",", "."))
    except Exception:
        return -1.0

def format_qty(q):
    # формат числа для отчёта (без .0 у целых)
    try:
        qf = float(q)
        if qf.is_integer():
            return str(int(qf))
        s = f"{qf}".rstrip("0").rstrip(".")
        return s
    except Exception:
        return str(q)


# ---------- PROJECT NAME ----------
st.markdown(right_label("שם פרויקט"), unsafe_allow_html=True)
project_name = st.text_input(
    "",
    value=st.session_state.project_name,
    key="project_name_input",
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

# список панелей с ❌
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
    key="panel_select",
    label_visibility="collapsed",
)
st.session_state.panel_name = panel_name

panel_rows = panels[panels["name"] == panel_name]
if panel_rows.empty:
    st.error("הפאנל שנבחר לא נמצא בקובץ panels.csv")
    st.stop()

panel = panel_rows.iloc[0]


# ---------- GROUPS ----------
# Удаляем основной заголовок, так как теперь секции будут в спойлерах
# st.markdown(right_header("קבוצות פאנלים"), unsafe_allow_html=True)

groups = []

# CSS для стрелок спойлера (добавляем глобально)
st.markdown("""
    <style>
    /* Стрелки для expander: закрыт - вниз, открыт - влево */
    .streamlit-expanderHeader svg {
        transform: rotate(0deg);
        transition: transform 0.3s;
    }
    .streamlit-expanderHeader[aria-expanded="true"] svg {
        transform: rotate(-90deg);
    }
    /* Выравнивание заголовка по правому краю */
    .streamlit-expanderHeader {
        text-align: right;
        direction: rtl;
    }
    </style>
""", unsafe_allow_html=True)

# Секция вертикальных панелей (первые 8 строк) - עומדים
with st.expander("**עומדים**", expanded=True):
    
    # Добавляем заголовки колонок внутри спойлера
    vh = st.columns(2)
    vh[0].markdown(right_label("שורות"), unsafe_allow_html=True)
    vh[1].markdown(right_label("פאנלים"), unsafe_allow_html=True)
    
    vertical_rows = st.session_state.vertical_rows
    for i in range(1, vertical_rows + 1):
        c0, c1 = st.columns(2)
        
        # Определяем предустановленные значения
        if i <= 8:
            default_g = 1
            default_n = i
        else:
            default_g = 0
            default_n = 0
        
        g = c0.number_input(
            "",
            0,
            50,
            default_g,
            key=f"g_g_vertical_{i}",
            label_visibility="collapsed",
        )

        n = c1.number_input(
            "",
            0,
            100,
            default_n,
            key=f"g_n_vertical_{i}",
            label_visibility="collapsed",
        )

        if n > 0 and g > 0:
            groups.append((n, g, "עומד"))  # ориентация фиксирована

    # Кнопка "להוסיף פאנלים" в конце секции вертикальных панелей
    if st.button("להוסיף פאנלים", key="add_panels_vertical"):
        st.session_state.vertical_rows += 1
        st.rerun()

# Секция горизонтальных панелей (последние 4 строки) - שוכבים
with st.expander("**שוכבים**", expanded=True):
    # Добавляем заголовки колонок внутри спойлера
    hh = st.columns(2)
    hh[0].markdown(right_label("שורות"), unsafe_allow_html=True)
    hh[1].markdown(right_label("פאנלים"), unsafe_allow_html=True)
    
    horizontal_rows = st.session_state.horizontal_rows
    for i in range(1, horizontal_rows + 1):
        c0, c1 = st.columns(2)
        
        # Определяем предустановленные значения
        if i <= 4:
            default_g = 1
            default_n = i
        else:
            default_g = 0
            default_n = 0
        
        g = c0.number_input(
            "",
            0,
            50,
            default_g,
            key=f"g_g_horizontal_{i}",
            label_visibility="collapsed",
        )

        n = c1.number_input(
            "",
            0,
            100,
            default_n,
            key=f"g_n_horizontal_{i}",
            label_visibility="collapsed",
        )

        if n > 0 and g > 0:
            groups.append((n, g, "שוכב"))  # ориентация фиксирована

    # Кнопка "להוסיף פאנלים" в конце секции горизонтальных панелей
    if st.button("להוסיף פאנלים", key="add_panels_horizontal"):
        st.session_state.horizontal_rows += 1
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
    auto_rails = calc_result.get("auto_rails", {})
    rails_total = {}
    for length, qty in auto_rails.items():
        rails_total[length] = rails_total.get(length, 0) + qty
    for length, qty in manual_rails.items():
        rails_total[length] = rails_total.get(length, 0) + qty

    # применяем пользовательские правки из интерфейса (если есть)
    try:
        k_over = getattr(st.session_state, "koshrot_qty", None)
    except Exception:
        k_over = None

    if k_over:
        # приводим ключи к строке как в UI
        rails_total = {normalize_length_key(k): int(v) for k, v in k_over.items() if int(v) > 0}

    ear = calc_result.get("ear", 0)
    mid = calc_result.get("mid", 0)
    edge = calc_result.get("edge", 0)
    conn = calc_result.get("conn", 0)
    total_panels = calc_result.get("total_panels", 0)

    total_length_cm = 0
    for length, qty in rails_total.items():
        total_length_cm += float(length) * qty

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
            h1 { font-size: 22px; }
            h2 { font-size: 18px; margin-top: 24px; }
            p { margin: 2px 0; }
            table { border-collapse: collapse; border:none; }
            td { padding: 0 0 2px 0; }
        </style>
    </head>
    <body>
    """

    html += f"<h1>{project_name}</h1>"

    html += "<h2>קושרות (כמות × אורך)</h2>"
    if rails_total:
        for length in sorted(rails_total.keys(), key=length_sort_key, reverse=True):
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
    # apply user overrides from UI (if any)
    overrides = None
    try:
        overrides = st.session_state.get("fasteners")
    except Exception:
        overrides = None
    if overrides:
        fasteners = [(lbl, overrides.get(lbl, val)) for (lbl, val) in fasteners]

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
                f"<td style='text-align:left; white-space:nowrap; border:none;'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;{qty_text}</td>"
                "</tr>"
            )
        html += "</tbody></table>"

    html += "</body></html>"
    return html


# ---------- BUTTON: CALCULATE ----------
# Кнопка расчета вне спойлера
if st.button("חשב", type="primary"):
    # reset editable קושרות boxes to automatic values on each calculation
    st.session_state.koshrot_qty = None
    st.session_state.koshrot_boxes_version += 1

    # reset קושרות (הוספה ידנית) completely on each new calculation (like page reload)
    st.session_state.manual_rows = 1
    st.session_state.manual_deleted_rows = set()
    st.session_state.manual_rails = {}
    st.session_state.manual_rails_prev = {}
    # bump version to force Streamlit to create fresh widgets with default values
    st.session_state.manual_form_version += 1

    st.session_state['m_len_1'] = 0
    st.session_state['m_qty_1'] = 0

    if groups:
        st.session_state.calc_result = do_calculation(panel, groups)
    else:
        st.session_state.calc_result = {
            "auto_rails": {},
            "conn": 0,
            "ear": 0,
            "mid": 0,
            "edge": 0,
            "total_panels": 0,
        }
    # reset קושרות quantities (recalc overrides each time)
    st.session_state.koshrot_qty = None

    # --- reset פרזול completely on each new calculation ---
    st.session_state["fasteners"] = None
    st.session_state["fasteners_include"] = None

    # reset קושרות (הוספה ידנית) section completely
    # (rows, deleted rows, stored widget values, aggregated dict, snapshot)
    st.session_state.manual_rows = 1
    st.session_state.manual_deleted_rows = set()
    st.session_state.manual_rails = {}
    st.session_state.manual_rails_prev = {}
    # clear widget keys for previous rows
    for j in range(1, 51):
        st.session_state.pop(f"m_len_{st.session_state.manual_form_version}_{j}", None)
        st.session_state.pop(f"m_qty_{st.session_state.manual_form_version}_{j}", None)
    st.session_state.just_calculated = True
    st.rerun()

    # success message shown after rerun

if st.session_state.get("just_calculated"):
    success_box("החישוב עודכן")
    st.session_state.just_calculated = False


calc_result = st.session_state.calc_result

# ---------- MANUAL RAILS ----------
# Секция ручного добавления рельс в спойлере
with st.expander("**קושרות (הוספה ידנית)**", expanded=True):
    # Добавляем заголовки колонок внутри спойлера
    mh = st.columns(2)  # теперь только 2 колонки
    mh[0].markdown(right_label("אורך (ס״מ)"), unsafe_allow_html=True)
    mh[1].markdown(right_label("כמות"), unsafe_allow_html=True)
    
    manual_rows = st.session_state.manual_rows

    for j in range(1, manual_rows + 1):
        cols = st.columns(2)  # только 2 колонки
        length = cols[0].number_input(
            "",
            min_value=0,
            max_value=10000,
            step=10,
            key=f"m_len_{st.session_state.manual_form_version}_{j}",
            label_visibility="collapsed",
        )
        qty = cols[1].number_input(
            "",
            min_value=0,
            max_value=1000,
            step=1,
            key=f"m_qty_{st.session_state.manual_form_version}_{j}",
            label_visibility="collapsed",
        )

    # Кнопка для добавления строк в конце секции
    # Используем form_submit_button чтобы предотвратить закрытие спойлера
    if st.button("להוסיף עוד קושרות", key="add_manual_rails"):
        st.session_state.manual_rows += 1
        st.rerun()

# Обработка данных ручного добавления (остается вне спойлера)
manual_rails_dict = {}
for j in range(1, st.session_state.manual_rows + 1):
    if j in st.session_state.manual_deleted_rows:
        continue
    length = st.session_state.get(f"m_len_{st.session_state.manual_form_version}_{j}", 0)
    qty = st.session_state.get(f"m_qty_{st.session_state.manual_form_version}_{j}", 0)
    if length and qty:
        manual_rails_dict[length] = manual_rails_dict.get(length, 0) + qty
st.session_state.manual_rails = manual_rails_dict

# --- sync manual additions into the editable קושרות boxes (koshrot_qty) ---
prev_manual = st.session_state.get("manual_rails_prev", {})
curr_manual = st.session_state.manual_rails

# only if the editable boxes are already initialized (i.e., after at least one חשב)
if st.session_state.get("koshrot_qty") is not None:
    # apply per-length delta: new_manual - prev_manual
    # keys in manual rails are numbers; we use string keys in koshrot_qty
    for length in set(list(prev_manual.keys()) + list(curr_manual.keys())):
        prev_q = int(prev_manual.get(length, 0) or 0)
        curr_q = int(curr_manual.get(length, 0) or 0)
        d = curr_q - prev_q
        if d == 0:
            continue
        k = normalize_length_key(length)
        new_val = max(int(st.session_state.koshrot_qty.get(k, 0) or 0) + d, 0)
        # update both the backing dict and the widget state (otherwise Streamlit keeps old widget value)
        st.session_state.koshrot_qty[k] = new_val
        st.session_state[f"koshrot_qty_{st.session_state.koshrot_boxes_version}_{k}"] = new_val

# update snapshot
st.session_state.manual_rails_prev = dict(curr_manual)



# ---------- SHOW CALC RESULT ----------
if calc_result is not None:
    auto_rails = calc_result["auto_rails"]
    manual_rails = st.session_state.manual_rails

    st.write(f"סה\"כ פאנלים: {calc_result['total_panels']}")

    # ----- קושרות -----
    with st.expander("**קושרות**", expanded=True):
        # базовые количества = авто + ручные (ручные не теряются при пересчёте)
        rails_base = {}
        for length, qty in auto_rails.items():
            klen = normalize_length_key(length)
            rails_base[klen] = rails_base.get(klen, 0) + int(qty)
        for length, qty in manual_rails.items():
            klen = normalize_length_key(length)
            rails_base[klen] = rails_base.get(klen, 0) + int(qty)

        # инициализация/синхронизация пользовательских правок:
        # сохраняем уже введённые значения, добавляем новые длины, убираем исчезнувшие
        if st.session_state.koshrot_qty is None:
            st.session_state.koshrot_qty = dict(rails_base)
        else:
            # добавить новые длины
            for length, qty in rails_base.items():
                if length not in st.session_state.koshrot_qty:
                    st.session_state.koshrot_qty[length] = qty
            # убрать длины, которых больше нет в базе
            for length in list(st.session_state.koshrot_qty.keys()):
                if length not in rails_base:
                    del st.session_state.koshrot_qty[length]

        if st.session_state.koshrot_qty:
            # Визуально как תעלות/פרזול: название (жирно, справа), под ним бокс количества
            for length in sorted(st.session_state.koshrot_qty.keys(), key=length_sort_key, reverse=True):
                st.markdown(right_label(f"אורך: {length} ס״מ"), unsafe_allow_html=True)

                qty_key = f"koshrot_qty_{st.session_state.koshrot_boxes_version}_{length}"
                default_val = int(st.session_state.koshrot_qty.get(length, 0))

                qty_val = st.number_input(
                    "",
                    min_value=0,
                    value=default_val,
                    step=1,
                    key=qty_key,
                    label_visibility="collapsed",
                )

                # сохраняем обратно в общий словарь, чтобы отчёт брал актуальное
                st.session_state.koshrot_qty[length] = int(qty_val)
        else:
            st.write("אין קושרות מחושבות")

    # ----- פרזול -----
    with st.expander("**פרזול**", expanded=True):
        ear = calc_result["ear"]
        mid = calc_result["mid"]
        edge = calc_result["edge"]
        conn = calc_result["conn"]
        total_panels = calc_result["total_panels"]

        # --- расчёт M8 и прочего зависит от суммарной длины קושרות ---
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

        # Базовые (авто) значения
        fasteners_base = [
            ("מהדק הארקה", ear),
            ("מהדק אמצע", mid),
            ("מהדק קצה", edge),
            ("פקק לקושרות", edge),
            ("מחברי קושרות", conn),
            ("בורג איסכורית 3,5", screws_iso),
            ("בורג M8 ראש משושה", m8_count),
            ("אום M8 נירוסטה", m8_count),
        ]
        # init include flags for report (default: all True)
        if st.session_state.get("fasteners_include") is None:
            st.session_state["fasteners_include"] = {name: True for name, _ in fasteners_base}
        else:
            for name, _ in fasteners_base:
                if name not in st.session_state["fasteners_include"]:
                    st.session_state["fasteners_include"][name] = True

        # Инициализация значений (после нового расчёта fasteners сбрасывается в None)
        if st.session_state.get("fasteners") is None:
            st.session_state["fasteners"] = {lbl: int(val) for (lbl, val) in fasteners_base}

        # UI как в "תעלות עם מכסים (מטר)": название + input со встроенными − / +
        new_fasteners = {}
        for i, (lbl, base_val) in enumerate(fasteners_base):
            current_val = int(st.session_state["fasteners"].get(lbl, base_val) or 0)

            # не показываем позиции, которые по умолчанию 0 и остались 0
            if int(base_val) == 0 and current_val == 0:
                continue
            c_chk, c_val, c_name = st.columns([0.8, 1.6, 5])
            with c_chk:
                inc_key = f"fast_inc_{lbl}"
                inc_default = bool(st.session_state["fasteners_include"].get(lbl, True))
                inc_val = st.checkbox("", value=inc_default, key=inc_key, label_visibility="collapsed")
                st.session_state["fasteners_include"][lbl] = bool(inc_val)
            with c_val:
                v = st.number_input(
                    "",
                    min_value=0,
                    value=int(current_val),
                    step=1,
                    key=f"fastener_qty_{i}_{lbl}",
                    label_visibility="collapsed",
                )
            with c_name:
                st.markdown(right_label(lbl), unsafe_allow_html=True)
            new_fasteners[lbl] = int(v)

        st.session_state["fasteners"] = new_fasteners

# ---------- CHANNELS ----------
with st.expander("**תעלות עם מכסים (מטר)**", expanded=True):
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
        q = st.number_input(
            "",
            min_value=0.0,
            value=0.0,
            step=step_value,
            format="%g",
            key=f"channel_{i}",
            label_visibility="collapsed",
        )
        if q > 0:
            channel_order[name] = q
    st.session_state.channel_order = channel_order


# ---------- EXTRA PARTS ----------
with st.expander("**הוסף פריט**", expanded=True):
    if not parts.empty:
        extra_rows = st.session_state.extra_rows
        chosen_entries = []
        names_list = parts["name"].tolist()

        for i in range(1, extra_rows + 1):
            st.markdown(right_label("פריט"), unsafe_allow_html=True)
            part = st.selectbox(
                "",
                names_list,
                key=f"extra_name_{i}",
                label_visibility="collapsed",
            )
            st.markdown(right_label("כמות"), unsafe_allow_html=True)
            qty = st.number_input(
                "",
                min_value=0,
                step=1,
                key=f"extra_qty_{i}",
                label_visibility="collapsed",
            )
            if qty > 0:
                chosen_entries.append((part, qty))

        if st.button("להוסיף עוד פריט"):
            st.session_state.extra_rows += 1
            st.rerun()

        agg = {}
        for name, qty in chosen_entries:
            agg[name] = agg.get(name, 0) + qty
        st.session_state.extra_parts = [
            {"name": n, "qty": q} for n, q in agg.items()
        ]
    else:
        info_box("אין פריטים בקובץ parts.csv – נא להוסיף פריט חדש בצד שמאל")

success_box("מוכן לייצוא (HTML → PDF דרך הדפסה)")


# ---------- EXPORT ----------
with st.expander("**ייצוא (HTML להדפסה ל-PDF)**", expanded=True):
    # сохраняем состояние показа отчёта, чтобы после rerun он оставался видимым
    if "show_report" not in st.session_state:
        st.session_state.show_report = False

    calc_result = st.session_state.calc_result
    if calc_result is not None:
        html_report = build_html_report(
            calc_result=calc_result,
            project_name=st.session_state.project_name,
            panel_name=panel_name,
            channel_order=st.session_state.channel_order,
            extra_parts=st.session_state.extra_parts,
            manual_rails=st.session_state.manual_rails,
        )

        c_left, c_right = st.columns(2)
        with c_left:
            if st.button('לייצא דו"ח', use_container_width=True):
                st.session_state.show_report = True

        with c_right:
            if st.button("פתח בטאב חדש", use_container_width=True):
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

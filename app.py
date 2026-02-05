import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import math
import json

# ---------- SESSION STATE INIT ----------
st.session_state.setdefault("fasteners", None)
st.session_state.setdefault("vertical_rows", 8)
st.session_state.setdefault("horizontal_rows", 4)

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
    </style>
""", unsafe_allow_html=True)

# Секция вертикальных панелей - עומדים
with st.expander("**עומדים**", expanded=True):
    
    vh = st.columns(2)
    vh[0].markdown(right_label("שורות"), unsafe_allow_html=True)
    vh[1].markdown(right_label("פאנלים"), unsafe_allow_html=True)
    
    vertical_rows = st.session_state.vertical_rows
    for i in range(1, vertical_rows + 1):
        c0, c1 = st.columns(2)
        
        default_g = 0
        if i <= 8:
            default_n = i
        else:
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
            groups.append((n, g, "עומד"))

    if st.button("להוסיף פאנלים", key="add_panels_vertical"):
        st.session_state.vertical_rows += 1
        st.rerun()

# Секция горизонтальных панелей - שוכבים
with st.expander("**שוכבים**", expanded=True):
    hh = st.columns(2)
    hh[0].markdown(right_label("שורות"), unsafe_allow_html=True)
    hh[1].markdown(right_label("פאנלים"), unsafe_allow_html=True)
    
    horizontal_rows = st.session_state.horizontal_rows
    for i in range(1, horizontal_rows + 1):
        c0, c1 = st.columns(2)
        
        default_g = 0
        if i <= 4:
            default_n = i
        else:
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
            groups.append((n, g, "שוכב"))

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
    
    overrides = st.session_state.get("fasteners")
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
                f"<td style='text-align:left; white-space:nowrap; border=none;'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;{qty_text}</td>"
                "</tr>"
            )
        html += "</tbody></table>"

    html += "</body></html>"
    return html


# ---------- BUTTON: CALCULATE ----------
if st.button("חשב", type="primary", use_container_width=True):

    # 🔥 СБРОС ВСЕХ WIDGET-КЛЮЧЕЙ פרזול
    for key in list(st.session_state.keys()):
        if key.startswith("fast_inc_") or key.startswith("fast_val_"):
            del st.session_state[key]

    # сброс данных פרזול
    st.session_state["fasteners"] = None
    st.session_state["fasteners_include"] = None

    
    # Сбрасываем קושרות (הוספה ידנית)
    st.session_state.manual_rows = 1
    st.session_state.manual_deleted_rows = set()
    st.session_state.manual_rails = {}
    st.session_state.manual_form_version += 1
    
    # Удаляем старые ключи ручных рельсов
    for j in range(1, 51):
        st.session_state.pop(f"m_len_{st.session_state.manual_form_version}_{j}", None)
        st.session_state.pop(f"m_qty_{st.session_state.manual_form_version}_{j}", None)
    
    # Расчет
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
    
    # Сбрасываем קושרות
    st.session_state.koshrot_qty = None
    st.session_state.koshrot_boxes_version += 1

    # Сбрасываем פרזול ПОЛНОСТЬЮ
    st.session_state["fasteners"] = None
    st.session_state["fasteners_include"] = None

    st.session_state.just_calculated = True
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
    with st.expander("**קושרות**", expanded=True):
        # Базовые значения: авто + ручные
        rails_base = {}
        for length, qty in auto_rails.items():
            klen = normalize_length_key(length)
            rails_base[klen] = rails_base.get(klen, 0) + int(qty)
        for length, qty in manual_rails.items():
            klen = normalize_length_key(length)
            rails_base[klen] = rails_base.get(klen, 0) + int(qty)

        # Инициализируем или обновляем koshrot_qty
        if st.session_state.koshrot_qty is None:
            st.session_state.koshrot_qty = dict(rails_base)
        else:
            # Обновляем существующие значения
            for length, qty in rails_base.items():
                st.session_state.koshrot_qty[length] = qty
            # Удаляем устаревшие длины
            for length in list(st.session_state.koshrot_qty.keys()):
                if length not in rails_base:
                    del st.session_state.koshrot_qty[length]

        if st.session_state.koshrot_qty:
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

                st.session_state.koshrot_qty[length] = int(qty_val)
        else:
            st.write("אין קושרות מחושבות")

    # ----- קושרות (הוספה ידנית) -----
    with st.expander("**קושרות (הוספה ידנית)**", expanded=True):
        mh = st.columns(2)
        mh[0].markdown(right_label("אורך (ס״מ)"), unsafe_allow_html=True)
        mh[1].markdown(right_label("כמות"), unsafe_allow_html=True)
        
        manual_rows = st.session_state.manual_rows

        for j in range(1, manual_rows + 1):
            cols = st.columns(2)
            length = cols[0].number_input(
                "",
                min_value=0,
                max_value=10000,
                step=10,
                value=0,
                key=f"m_len_{st.session_state.manual_form_version}_{j}",
                label_visibility="collapsed",
            )
            qty = cols[1].number_input(
                "",
                min_value=0,
                max_value=1000,
                step=1,
                value=0,
                key=f"m_qty_{st.session_state.manual_form_version}_{j}",
                label_visibility="collapsed",
            )

        if st.button("להוסיף עוד קושרות", key="add_manual_rails"):
            st.session_state.manual_rows += 1
            st.rerun()
    
    # Собираем ручные рельсы
    manual_rails_dict = {}
    for j in range(1, st.session_state.manual_rows + 1):
        if j in st.session_state.manual_deleted_rows:
            continue
        length = st.session_state.get(f"m_len_{st.session_state.manual_form_version}_{j}", 0)
        qty = st.session_state.get(f"m_qty_{st.session_state.manual_form_version}_{j}", 0)
        if length and qty:
            manual_rails_dict[length] = manual_rails_dict.get(length, 0) + qty
    
    # ОБЯЗАТЕЛЬНО обновляем manual_rails
    st.session_state.manual_rails = manual_rails_dict

# --- SAFE INIT ---
calc_result = st.session_state.get("calc_result")

if not calc_result:
    calc_result = {
        "auto_rails": {},
        "conn": 0,
        "ear": 0,
        "mid": 0,
        "edge": 0,
        "total_panels": 0,
    }

auto_rails = calc_result.get("auto_rails", {})
manual_rails = st.session_state.get("manual_rails", {})

# ----- פרזול -----
with st.expander("**פרזול**", expanded=True):
    ear = calc_result["ear"]
    mid = calc_result["mid"]
    edge = calc_result["edge"]
    conn = calc_result["conn"]
    total_panels = calc_result["total_panels"]

    # расчет длины для M8: авто + ручные
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

    # базовые значения
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

    # инициализация
    if st.session_state.get("fasteners") is None:
        st.session_state["fasteners"] = {lbl: int(val) for lbl, val in fasteners_base}

    if st.session_state.get("fasteners_include") is None:
        st.session_state["fasteners_include"] = {lbl: True for lbl, _ in fasteners_base}

    overrides = st.session_state["fasteners"]
    include_map = st.session_state["fasteners_include"]

    new_fasteners = {}
    new_include = {}

    for i, (lbl, base_val) in enumerate(fasteners_base):
        current_val = int(overrides.get(lbl, base_val))

        # не показываем нули
        if base_val == 0 and current_val == 0:
            continue

        c_chk, c_val, c_name = st.columns([0.8, 1.6, 5])

        with c_chk:
            inc = st.checkbox(
                "",
                value=bool(include_map.get(lbl, True)),
                key=f"fast_inc_{i}",
                label_visibility="collapsed",
            )

        with c_val:
            val = st.number_input(
                "",
                min_value=0,
                value=int(current_val),
                step=1,
                key=f"fast_val_{i}",
                label_visibility="collapsed",
            )

        with c_name:
            st.markdown(right_label(lbl), unsafe_allow_html=True)

        new_fasteners[lbl] = int(val)
        new_include[lbl] = bool(inc)

    st.session_state["fasteners"] = new_fasteners
    st.session_state["fasteners_include"] = new_include


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
    st.session_state.channel_order = {k: v for k, v in channel_order.items() if v > 0}


# ---------- EXTRA PARTS ----------
with st.expander("**הוסף פריט**", expanded=True):
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

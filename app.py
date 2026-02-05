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
        <div style=" background-color:#2b2b2b; color:white; padding:12px; border-radius:6px; text-align:right; border:1px solid #555; ">
            {text}
        </div>
        """,
        unsafe_allow_html=True,
    )

def success_box(text: str):
    text = clean_text(text)
    st.markdown(
        f"""
        <div style=" background-color:#1f3d1f; color:white; padding:12px; border-radius:6px; text-align:right; border:1px solid #4caf50; ">
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
for key, default in [
    ("calc_result", None), ("just_calculated", False), ("channel_order", {}),
    ("extra_parts", []), ("manual_rows", 1), ("manual_form_version", 0),
    ("koshrot_boxes_version", 0), ("manual_rails", {}), ("panel_name", None),
    ("extra_rows", 1), ("project_name", ""), ("manual_deleted_rows", set()),
    ("fasteners_reset_version", 0)
]:
    st.session_state.setdefault(key, default)

# ---------- HELPERS ----------
def round_up_to_tens(x: float) -> int:
    return int(math.ceil(x / 10.0) * 10) if x > 0 else 0

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
        return s

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
        return f"{qf}".rstrip("0").rstrip(".")
    except Exception:
        return str(q)

# ---------- PROJECT NAME ----------
st.markdown(right_label("שם פרויקט"), unsafe_allow_html=True)
project_name = st.text_input(
    "", value=st.session_state.project_name, key="project_name_input", label_visibility="collapsed"
)
st.session_state.project_name = project_name

# ---------- PANEL ADD / DELETE (SIDEBAR) ----------
st.sidebar.markdown(right_header("פאנל חדש"), unsafe_allow_html=True)
st.sidebar.markdown(right_label("שם פאנל"), unsafe_allow_html=True)
new_name = st.sidebar.text_input("", key="sidebar_panel_name", label_visibility="collapsed")
st.sidebar.markdown(right_label("רוחב (ס״מ)"), unsafe_allow_html=True)
new_w = st.sidebar.number_input("", min_value=0.0, value=0.0, step=0.1, format="%.1f", key="panel_width", label_visibility="collapsed")
st.sidebar.markdown(right_label("אורך (ס״מ)"), unsafe_allow_html=True)
new_h = st.sidebar.number_input("", min_value=0.0, value=0.0, step=0.1, format="%.1f", key="panel_height", label_visibility="collapsed")

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
unit = st.sidebar.radio("", ["יח׳", "מטר", "ס״מ"], index=0, horizontal=True, key="lib_new_unit", label_visibility="collapsed")
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
    if "640" in n: return (0, n)
    if "595" in n: return (1, n)
    return (2, n)

names = panels["name"].tolist()
panel_options = sorted(list(dict.fromkeys(names)), key=panel_sort_key)
if not panel_options:
    st.error("אין פאנלים בקובץ panels.csv")
    st.stop()
default_index = panel_options.index(st.session_state.panel_name) if st.session_state.panel_name in panel_options else 0

st.markdown(right_label("סוג פאנל"), unsafe_allow_html=True)
panel_name = st.selectbox("", panel_options, index=default_index, key="panel_select", label_visibility="collapsed")
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
.streamlit-expanderHeader svg { transform: rotate(0deg); transition: transform 0.3s; }
.streamlit-expanderHeader[aria-expanded="true"] svg { transform: rotate(-90deg); }
.streamlit-expanderHeader { text-align: right; direction: rtl; }
</style>
""", unsafe_allow_html=True)

# --- Vertical Panels
with st.expander("**עומדים**", expanded=True):
    vh = st.columns(2)
    vh[0].markdown(right_label("שורות"), unsafe_allow_html=True)
    vh[1].markdown(right_label("פאנלים"), unsafe_allow_html=True)
    vertical_rows = st.session_state.vertical_rows
    for i in range(1, vertical_rows + 1):
        c0, c1 = st.columns(2)
        default_g = 0
        default_n = i if i <= 8 else 0
        g = c0.number_input("", 0, 50, default_g, key=f"g_g_vertical_{i}", label_visibility="collapsed")
        n = c1.number_input("", 0, 100, default_n, key=f"g_n_vertical_{i}", label_visibility="collapsed")
        if n > 0 and g > 0: groups.append((n, g, "עומד"))
    if st.button("להוסיף פאנלים", key="add_panels_vertical"):
        st.session_state.vertical_rows += 1
        st.rerun()

# --- Horizontal Panels
with st.expander("**שוכבים**", expanded=True):
    hh = st.columns(2)
    hh[0].markdown(right_label("שורות"), unsafe_allow_html=True)
    hh[1].markdown(right_label("פאנלים"), unsafe_allow_html=True)
    horizontal_rows = st.session_state.horizontal_rows
    for i in range(1, horizontal_rows + 1):
        c0, c1 = st.columns(2)
        default_g = 0
        default_n = i if i <= 4 else 0
        g = c0.number_input("", 0, 50, default_g, key=f"g_g_horizontal_{i}", label_visibility="collapsed")
        n = c1.number_input("", 0, 100, default_n, key=f"g_n_horizontal_{i}", label_visibility="collapsed")
        if n > 0 and g > 0: groups.append((n, g, "שוכב"))
    if st.button("להוסיף פאנלים", key="add_panels_horizontal"):
        st.session_state.horizontal_rows += 1
        st.rerun()

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
    if N == 1: return 0, 0
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
        final = 250 if N == 1 else 490
        segs = [final]
        connectors = 0
        earthing, middle = calc_fixings(N)
        edge = 4
        rails_per_row = 2
        return segs, connectors, earthing, middle, edge, rails_per_row
    base = panel_row["width"] * N if orientation == "עומד" else panel_row["height"] * N
    fixings = N + 1
    raw = base + fixings * 2
    final = int(math.ceil((raw + 10) / 10) * 10)
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

# ---------- HTML REPORT ----------
def build_html_report(calc_result, project_name, panel_name, channel_order, extra_parts, manual_rails):
    auto_rails = calc_result.get("auto_rails", {})
    rails_total = {}
    for length, qty in auto_rails.items():
        rails_total[length] = rails_total.get(length, 0) + qty
    # add manual rails
    for length, qty in manual_rails.items():
        rails_total[length] = rails_total.get(length, 0) + qty
    try:
        k_over = getattr(st.session_state, "koshrot_qty", None)
    except Exception:
        k_over = None
    if k_over:
        rails_total = {normalize_length_key(k): int(v) for k, v in k_over.items() if int(v) > 0}

    ear = calc_result.get("ear", 0)
    mid = calc_result.get("mid", 0)
    edge = calc_result.get("edge", 0)
    conn = calc_result.get("conn", 0)
    total_panels = calc_result.get("total_panels", 0)
    total_length_cm = sum(float(length)*qty for length, qty in rails_total.items())
    screws_iso = round_up_to_tens(conn*4 + total_panels)
    m8_count = round_up_to_tens(total_length_cm / 140.0) if total_length_cm > 0 else 0

    html = """<html><head><meta charset="utf-8"><title>דו"ח מערכת סולארית</title>
    <style>
    body { font-family: Arial, sans-serif; margin:30px; background-color:white; color:black; direction:rtl; }
    h1 { font-size:22px; }
    h2 { font-size:18px; margin-top:24px; }
    p { margin:2px 0; }
    table { border-collapse: collapse; border:none; }
    td { padding:0 0 2px 0; }
    </style></head><body>"""
    html += f"<h1>{project_name}</h1>"
    html += "<h2>קושרות (כמות × אורך)</h2>"
    if rails_total:
        for length in sorted(rails_total.keys(), key=length_sort_key, reverse=True):
            html += f"<p dir='rtl' style='text-align:right;'>{rails_total[length]} × {length}</p>"
    # fasteners
    fasteners = [
        ("מהדק הארקה", ear),
        ("מהדק אמצע", mid),
        ("מהדק קצה", edge),
        ("פקק לקושרות", edge),
        ("מחברי קושרות", conn),
        ("בורג איסכורית 3,5", screws_iso),
        ("M8 בורג", m8_count),
        ("M8 אום", m8_count)
    ]
    overrides = st.session_state.get("fasteners")
    if overrides:
        fasteners = [(lbl, overrides.get(lbl, val)) for (lbl, val) in fasteners]
    inc_map = st.session_state.get("fasteners_include", {})
    visible_fasteners = [(lbl, val) for lbl, val in fasteners if val > 0 and bool(inc_map.get(lbl, True))]
    html += "<h2>פרזול</h2>"
    if visible_fasteners:
        html += "<table style='direction:rtl; text-align:right; border:none;'><tbody>"
        for lbl, val in visible_fasteners:
            html += f"<tr style='border:none;'><td style='text-align:right; white-space:nowrap; border:none;'>{lbl}</td>" \
                    f"<td style='text-align:left; white-space:nowrap; border:none;'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;{val}</td></tr>"
        html += "</tbody></table>"
    if channel_order:
        html += "<h2>תעלות עם מכסים (מטר)</h2><table style='direction:rtl; text-align:right; border:none;'><tbody>"
        for name, qty in channel_order.items():
            html += f"<tr style='border:none;'><td style='text-align:right; white-space:nowrap; border:none;'>{name}</td>" \
                    f"<td style

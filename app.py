# Минимальный рабочий пример
import streamlit as st

st.markdown("""
<div style="display: flex; align-items: center; gap: 10px;">
    <button onclick="window.parent.postMessage({type: 'setComponentValue', value: 'dec'}, '*')">-</button>
    <span id="value">10</span>
    <button onclick="window.parent.postMessage({type: 'setComponentValue', value: 'inc'}, '*')">+</button>
</div>
""", unsafe_allow_html=True)

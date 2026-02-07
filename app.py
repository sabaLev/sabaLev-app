import streamlit as st

st.markdown("""
<div style="width:100%;">
<table style="width:100%; border-collapse:collapse;">
<tr style="font-weight:bold; text-align:right;">
<td style="width:50%; padding:5px;">שורות</td>
<td style="width:50%; padding:5px;">פאנלים</td>
</tr>
<tr>
<td style="width:50%; padding:5px;">
""", unsafe_allow_html=True)

# Поле ввода ПРЯМО в таблице
st.number_input("", 0, 50, 0, key="tab1", label_visibility="collapsed")

st.markdown("""
</td>
<td style="width:50%; padding:5px; text-align:right; font-size:16px;">
1
</td>
</tr>
<tr>
<td style="width:50%; padding:5px;">
""", unsafe_allow_html=True)

st.number_input("", 0, 50, 0, key="tab2", label_visibility="collapsed")

st.markdown("""
</td>
<td style="width:50%; padding:5px; text-align:right; font-size:16px;">
2
</td>
</tr>
</table>
</div>
""", unsafe_allow_html=True)

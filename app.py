import streamlit as st

st.title("Таблица с кнопками рядом")

# Данные
data = [[10, 20], [30, 40]]

# Отображение
for i in range(2):
    cols = st.columns([3, 1, 3, 1])  # значение1, кнопки1, значение2, кнопки2
    
    with cols[0]:
        st.write(f"**{data[i][0]}**")
    
    with cols[1]:
        col1, col2 = st.columns(2)
        with col1:
            if st.button("➖", key=f"a_dec_{i}"):
                data[i][0] -= 1
                st.rerun()
        with col2:
            if st.button("➕", key=f"a_inc_{i}"):
                data[i][0] += 1
                st.rerun()
    
    with cols[2]:
        st.write(f"**{data[i][1]}**")
    
    with cols[3]:
        col3, col4 = st.columns(2)
        with col3:
            if st.button("➖", key=f"b_dec_{i}"):
                data[i][1] -= 1
                st.rerun()
        with col4:
            if st.button("➕", key=f"b_inc_{i}"):
                data[i][1] += 1
                st.rerun()
    
    if i == 0:
        st.divider()

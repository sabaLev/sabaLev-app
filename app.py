import streamlit as st

st.title("Таблица 2x2")

# Данные
data = [[0, 0], [0, 0]]

# Отображение
for i in range(2):
    cols = st.columns(2)
    for j in range(2):
        with cols[j]:
            st.write(f"**Ячейка [{i},{j}]**")
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("➖", key=f"dec_{i}_{j}"):
                    data[i][j] -= 1
                    st.rerun()
            with col2:
                st.write(f"**{data[i][j]}**")
            with col3:
                if st.button("➕", key=f"inc_{i}_{j}"):
                    data[i][j] += 1
                    st.rerun()
    if i == 0:
        st.divider()

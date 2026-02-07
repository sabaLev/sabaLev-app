import streamlit as st

st.title("Простая таблица 2x2")

# Инициализация данных
if 'table' not in st.session_state:
    st.session_state.table = [[0, 0], [0, 0]]

# Заголовки
col1, col2 = st.columns(2)
with col1:
    st.write("**Колонка 1**")
with col2:
    st.write("**Колонка 2**")

st.divider()

# Первая строка
row1_col1, row1_col2 = st.columns(2)

with row1_col1:
    st.write("**Строка 1**")
    col1_1, col1_2, col1_3 = st.columns(3)
    with col1_1:
        if st.button("➖", key="r1c1_dec"):
            st.session_state.table[0][0] -= 1
            st.rerun()
    with col1_2:
        st.write(f"**{st.session_state.table[0][0]}**")
    with col1_3:
        if st.button("➕", key="r1c1_inc"):
            st.session_state.table[0][0] += 1
            st.rerun()

with row1_col2:
    col2_1, col2_2, col2_3 = st.columns(3)
    with col2_1:
        if st.button("➖", key="r1c2_dec"):
            st.session_state.table[0][1] -= 1
            st.rerun()
    with col2_2:
        st.write(f"**{st.session_state.table[0][1]}**")
    with col2_3:
        if st.button("➕", key="r1c2_inc"):
            st.session_state.table[0][1] += 1
            st.rerun()

st.divider()

# Вторая строка
row2_col1, row2_col2 = st.columns(2)

with row2_col1:
    st.write("**Строка 2**")
    col3_1, col3_2, col3_3 = st.columns(3)
    with col3_1:
        if st.button("➖", key="r2c1_dec"):
            st.session_state.table[1][0] -= 1
            st.rerun()
    with col3_2:
        st.write(f"**{st.session_state.table[1][0]}**")
    with col3_3:
        if st.button("➕", key="r2c1_inc"):
            st.session_state.table[1][0] += 1
            st.rerun()

with row2_col2:
    col4_1, col4_2, col4_3 = st.columns(3)
    with col4_1:
        if st.button("➖", key="r2c2_dec"):
            st.session_state.table[1][1] -= 1
            st.rerun()
    with col4_2:
        st.write(f"**{st.session_state.table[1][1]}**")
    with col4_3:
        if st.button("➕", key="r2c2_inc"):
            st.session_state.table[1][1] += 1
            st.rerun()

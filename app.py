st.title("Тест лазейки №3: st.empty() как плейсхолдер")

# Создаем "дырки" для наших элементов
placeholder1 = st.empty()
placeholder2 = st.empty()

# Заполняем их ВРУЧНУЮ
with placeholder1.container():
    col1, col2 = st.columns([1, 3])
    with col1:
        st.checkbox("", key="cb_empty1", label_visibility="collapsed")
    with col2:
        st.markdown("מהדק הארקה")

with placeholder2.container():
    col1, col2 = st.columns([1, 3])
    with col1:
        st.checkbox("", key="cb_empty2", label_visibility="collapsed")
    with col2:
        st.markdown("מהדק אמצע")

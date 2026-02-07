st.header("10. Интерактивный пример")

col1, col2 = st.columns(2)

with col1:
    # Слайдер для настройки параметров другого слайдера
    min_val = st.slider("Минимальное значение", -100, 0, -50)
    max_val = st.slider("Максимальное значение", 0, 100, 50)
    step_val = st.slider("Шаг", 1, 20, 5)

with col2:
    # Динамический слайдер
    dynamic_slider = st.slider(
        "Динамический слайдер",
        min_value=min_val,
        max_value=max_val,
        value=(min_val + max_val) // 2,
        step=step_val
    )
    st.metric("Результат", dynamic_slider)

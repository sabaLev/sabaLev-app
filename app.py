st.title("Тест лазейки №2: container с высотой")

# Создаем контейнер
container = st.container()

# Заполняем контейнер
with container:
    # Пытаемся сделать свою разметку внутри
    html_code = """
    <div style="
        display: flex !important;
        width: 100% !important;
        border: 2px solid blue;
        padding: 10px;
        height: 60px !important;  # ФИКСИРОВАННАЯ высота
        overflow: hidden !important;
    ">
        <div style="width:50px; background:lightgreen; text-align:center;">✓</div>
        <div style="flex:1; text-align:right; padding-right:15px;">טקסט בעברית</div>
    </div>
    """
    st.markdown(html_code, unsafe_allow_html=True)
    
    # Пробуем вставить нативный элемент
    st.checkbox("Чекбокс в контейнере", key="cb_container")

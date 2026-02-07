import streamlit as st

st.markdown("""
<style>
/* Сбрасываем ВСЕ стили Streamlit */
div.row-widget.stHorizontalBlock {
    display: flex !important;
    flex-direction: row !important;
    width: 100% !important;
}

div[data-testid="column"] {
    display: block !important;
    position: relative !important;
    min-width: 0px !important;
    padding: 0px !important;
    margin: 0px !important;
}

/* ВИДИМАЯ граница посередине */
.middle-boundary-visible {
    position: absolute !important;
    left: 50% !important;
    top: 0 !important;
    bottom: 0 !important;
    width: 3px !important;
    background: red !important;
    pointer-events: none !important;
    z-index: 9999 !important;
}

/* Контейнер для всей строки */
.row-container {
    display: flex !important;
    width: 100% !important;
    position: relative !important;
    border: 1px solid blue !important; /* Синяя рамка вокруг строки */
    margin-bottom: 15px !important;
    padding: 5px !important;
}

/* Левая часть - поле ввода */
.left-part {
    width: 50% !important;
    flex: 0 0 50% !important;
    max-width: 50% !important;
    padding-right: 10px !important;
    border: 1px solid green !important; /* Зеленая рамка */
    box-sizing: border-box !important;
}

/* Правая часть - текст */
.right-part {
    width: 50% !important;
    flex: 0 0 50% !important;
    max-width: 50% !important;
    padding-left: 10px !important;
    border: 1px solid orange !important; /* Оранжевая рамка */
    box-sizing: border-box !important;
    text-align: right !important;
    display: flex !important;
    align-items: center !important;
    justify-content: flex-end !important;
}

/* Контейнер для заголовков */
.header-row {
    display: flex !important;
    width: 100% !important;
    border: 1px solid purple !important; /* Фиолетовая рамка */
    margin-bottom: 10px !important;
    padding: 5px !important;
    font-weight: bold !important;
}

.header-left {
    width: 50% !important;
    flex: 0 0 50% !important;
    padding-right: 10px !important;
    text-align: right !important;
    border: 1px solid pink !important; /* Розовая рамка */
    box-sizing: border-box !important;
}

.header-right {
    width: 50% !important;
    flex: 0 0 50% !important;
    padding-left: 10px !important;
    text-align: right !important;
    border: 1px solid yellow !important; /* Желтая рамка */
    box-sizing: border-box !important;
}

/* Тестовый div чтобы увидеть реальные границы */
.test-box {
    border: 2px dashed black !important;
    padding: 10px !important;
    margin: 5px !important;
    background: rgba(255,0,0,0.1) !important;
}
</style>
""", unsafe_allow_html=True)

st.title("Тест с ВИДИМЫМИ границами")

st.markdown("""
<div style="margin-bottom:20px; padding:10px; background:#f0f0f0; border-radius:5px;">
<strong>Обозначения цветов:</strong><br>
• Синий = граница строки<br>
• Красный = центральная граница (50%)<br>
• Зеленый = левая колонка (поле ввода)<br>
• Оранжевый = правая колонка (текст)<br>
• Фиолетовый = заголовок строки<br>
• Розовый = заголовок левой колонки<br>
• Желтый = заголовок правой колонки
</div>
""", unsafe_allow_html=True)

# Заголовки
st.markdown('<div class="header-row">', unsafe_allow_html=True)
st.markdown('<div class="header-left">שורות</div>', unsafe_allow_html=True)
st.markdown('<div class="header-right">פאנלים</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Тестовый div для понимания что видит Streamlit
st.markdown('<div class="test-box">Этот div показывает реальные границы контейнера</div>', unsafe_allow_html=True)

# Строка 1
st.markdown('<div class="row-container">', unsafe_allow_html=True)

# ВИДИМАЯ красная граница посередине
st.markdown('<div class="middle-boundary-visible"></div>', unsafe_allow_html=True)

# Левая часть
st.markdown('<div class="left-part">', unsafe_allow_html=True)
# Помещаем поле ввода ВНУТРИ div
st.markdown('<div style="width:100%;">', unsafe_allow_html=True)
st.number_input("Строка 1", 0, 50, 0, key="visible1", label_visibility="collapsed")
st.markdown('</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Правая часть
st.markdown('<div class="right-part">', unsafe_allow_html=True)
st.markdown('<div style="font-size:16px; padding:10px;">1</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# Строка 2
st.markdown('<div class="row-container">', unsafe_allow_html=True)
st.markdown('<div class="middle-boundary-visible"></div>', unsafe_allow_html=True)

st.markdown('<div class="left-part">', unsafe_allow_html=True)
st.markdown('<div style="width:100%;">', unsafe_allow_html=True)
st.number_input("Строка 2", 0, 50, 0, key="visible2", label_visibility="collapsed")
st.markdown('</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="right-part">', unsafe_allow_html=True)
st.markdown('<div style="font-size:16px; padding:10px;">2</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

st.markdown("---")
st.write("**Что мы должны видеть:**")
st.write("1. Красная линия ровно посередине")
st.write("2. Левая и правая части внутри своих границ (зеленой и оранжевой)")
st.write("3. Поле ввода должно быть внутри зеленой рамки")
st.write("4. Текст '1' и '2' внутри оранжевой рамки")

import streamlit as st

# Если нужно показать и плейсхолдер, и введенный текст
st.markdown("""
<style>
.dual-display { border: 1px solid #ccc; padding: 10px; border-radius: 5px; }
.hint-text { color: #888; font-size: 0.9em; margin-top: 5px; }
</style>
""", unsafe_allow_html=True)

input_container = st.container()

with input_container:
    user_input = st.text_input("Введите текст", label_visibility="collapsed")
    
    # Подсказка всегда под полем
    st.markdown(
        '<div class="hint-text">Пример: Иван Иванов (эта подсказка не исчезнет)</div>',
        unsafe_allow_html=True
    )
    
    # Отображаем введенные данные
    if user_input:
        st.info(f"Вы ввели: **{user_input}**")

import streamlit as st

def text_input_with_constant_hint(label, hint_text, key):
    """Поле ввода с подсказкой, которая всегда видна"""
    col1, col2 = st.columns([3, 1])
    
    with col1:
        value = st.text_input(label, key=key, label_visibility="collapsed")
    
    with col2:
        # Подсказка всегда видна
        st.markdown(f"""
        <div style="color: #666; font-size: 0.9em; padding-top: 0.5rem;">
            {hint_text}
        </div>
        """, unsafe_allow_html=True)
    
    return value

# Использование в форме
st.title("Регистрация")

email = text_input_with_constant_hint(
    "Email адрес", 
    "name@domain.com", 
    "reg_email"
)

phone = text_input_with_constant_hint(
    "Телефон", 
    "+7 XXX XXX-XX-XX", 
    "reg_phone"
)

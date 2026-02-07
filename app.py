import streamlit as st
from streamlit.components.v1 import html

def inline_text_input(label, key, placeholder=""):
    html_code = f"""
    <div style="display: flex; align-items: center; margin-bottom: 1rem;">
        <label style="margin-right: 10px; min-width: 80px;">{label}</label>
        <input type="text" 
               id="{key}" 
               placeholder="{placeholder}"
               style="flex-grow: 1; padding: 0.5rem; border: 1px solid #ccc; border-radius: 0.25rem;">
    </div>
    <script>
        document.getElementById('{key}').addEventListener('input', function(e) {{
            window.parent.postMessage({{
                type: 'streamlit:setComponentValue',
                value: e.target.value
            }}, '*');
        }});
    </script>
    """
    return html(html_code, height=100)

# Использование
value = inline_text_input("Имя:", "name_input", "Введите ваше имя")
st.write(f"Введено: {value}")

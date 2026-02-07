import streamlit as st

def text_input_with_static_hint(label, hint, key):
    html_code = f"""
    <div style="position: relative; margin-bottom: 1rem;">
        <label style="display: block; margin-bottom: 0.25rem; font-weight: 500;">{label}</label>
        <div style="position: relative;">
            <input type="text" 
                   id="{key}"
                   style="width: 100%; padding: 0.5rem; padding-left: 150px; 
                          border: 1px solid #ccc; border-radius: 0.25rem;"
                   oninput="this.style.color = this.value ? '#000' : '#999'">
            <div style="position: absolute; left: 10px; top: 50%; transform: translateY(-50%); 
                       color: #999; pointer-events: none;">
                {hint}
            </div>
        </div>
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
    return st.components.v1.html(html_code, height=120)

# Использование
value = text_input_with_static_hint("Email", "example@gmail.com", "email_field")

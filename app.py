import streamlit as st

# CSS для стилизации
st.markdown("""
<style>
.prefix-input-container {
    display: flex;
    align-items: center;
    border: 1px solid #ccc;
    border-radius: 0.25rem;
    padding: 0;
    background: white;
}
.prefix-input-container .prefix {
    padding: 0.5rem;
    background: #f0f0f0;
    border-right: 1px solid #ccc;
    color: #666;
    white-space: nowrap;
}
.prefix-input-container input {
    border: none;
    padding: 0.5rem;
    width: 100%;
    outline: none;
}
</style>
""", unsafe_allow_html=True)

# Функция для создания поля с префиксом
def text_input_with_prefix(prefix, placeholder, key):
    html_code = f"""
    <div class="prefix-input-container">
        <div class="prefix">{prefix}</div>
        <input type="text" 
               placeholder="{placeholder}"
               id="{key}"
               style="flex-grow: 1;">
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
    return st.components.v1.html(html_code, height=50)

# Использование
st.write("**Пример с постоянным префиксом:**")
value1 = text_input_with_prefix("https://", "example.com", "url_input")
value2 = text_input_with_prefix("+7", "900 000-00-00", "phone_input")

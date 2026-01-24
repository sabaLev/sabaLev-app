import streamlit.components.v1 as components
import streamlit as st

def dual_number_input(label_n, label_g, default_n=0, default_g=0, min_val=0, max_val=99, key=None):
    """Кастомная компонента с двумя инпутами в одной строке"""
    
    if key is None:
        key = f"dual_input_{label_n}_{label_g}"
    
    if f"{key}_n" not in st.session_state:
        st.session_state[f"{key}_n"] = default_n
    if f"{key}_g" not in st.session_state:
        st.session_state[f"{key}_g"] = default_g
    
    component_code = f'''
    <div style="display: flex; gap: 10px; margin-bottom: 10px; align-items: center;">
        <!-- Поле N -->
        <div style="flex: 1;">
            <div style="font-size: 12px; color: #666; margin-bottom: 4px; text-align: center;">{label_n}</div>
            <div style="display: flex; border: 1px solid #ccc; border-radius: 6px; overflow: hidden; background: #f8f9fa;">
                <button style="border: none; background: #e9ecef; padding: 8px 12px; cursor: pointer; font-size: 16px; width: 40px;" 
                        onclick="changeValue('{key}_n', -1)">−</button>
                <input type="number" id="{key}_n" value="{st.session_state[f"{key}_n"]}" 
                       style="flex: 1; border: none; text-align: center; padding: 8px 0; font-size: 16px; background: white;" 
                       min="{min_val}" max="{max_val}"
                       onchange="sendValue('{key}_n', this.value)">
                <button style="border: none; background: #e9ecef; padding: 8px 12px; cursor: pointer; font-size: 16px; width: 40px;" 
                        onclick="changeValue('{key}_n', 1)">+</button>
            </div>
        </div>
        
        <!-- Поле G -->
        <div style="flex: 1;">
            <div style="font-size: 12px; color: #666; margin-bottom: 4px; text-align: center;">{label_g}</div>
            <div style="display: flex; border: 1px solid #ccc; border-radius: 6px; overflow: hidden; background: #f8f9fa;">
                <button style="border: none; background: #e9ecef; padding: 8px 12px; cursor: pointer; font-size: 16px; width: 40px;" 
                        onclick="changeValue('{key}_g', -1)">−</button>
                <input type="number" id="{key}_g" value="{st.session_state[f"{key}_g"]}" 
                       style="flex: 1; border: none; text-align: center; padding: 8px 0; font-size: 16px; background: white;" 
                       min="{min_val}" max="{max_val}"
                       onchange="sendValue('{key}_g', this.value)">
                <button style="border: none; background: #e9ecef; padding: 8px 12px; cursor: pointer; font-size: 16px; width: 40px;" 
                        onclick="changeValue('{key}_g', 1)">+</button>
            </div>
        </div>
    </div>
    
    <script>
    function sendValue(key, value) {{
        const numValue = parseInt(value) || 0;
        window.parent.postMessage({{
            type: 'streamlit',
            key: key,
            value: numValue
        }}, '*');
    }}
    
    function changeValue(key, delta) {{
        const input = document.getElementById(key);
        let value = parseInt(input.value) || 0;
        value += delta;
        
        // Проверка границ
        if (value < {min_val}) value = {min_val};
        if (value > {max_val}) value = {max_val};
        
        input.value = value;
        sendValue(key, value);
    }}
    
    // Инициализация
    document.addEventListener('DOMContentLoaded', function() {{
        sendValue('{key}_n', document.getElementById('{key}_n').value);
        sendValue('{key}_g', document.getElementById('{key}_g').value);
    }});
    </script>
    '''
    
    components.html(component_code, height=130)
    
    # JavaScript для получения сообщений
    components.html(f'''
    <script>
    window.addEventListener('message', function(event) {{
        if (event.data.type === 'streamlit') {{
            window.parent.postMessage({{
                type: 'streamlit:setComponentValue',
                key: event.data.key,
                value: event.data.value
            }}, '*');
        }}
    }});
    </script>
    ''', height=0)
    
    return st.session_state[f"{key}_n"], st.session_state[f"{key}_g"]

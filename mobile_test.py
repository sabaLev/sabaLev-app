import streamlit as st
import streamlit.components.v1 as components

st.title("📱 Тест мобильной верстки")

st.write("**Откройте эту страницу на телефоне**")

# HTML с двумя колонками
html = '''
<div style="
    display: flex; 
    gap: 10px; 
    margin: 30px 0;
">
    <div style="
        flex: 1;
        background: #4b75c9;
        color: white;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
    ">
        <h3>פאנלים</h3>
        <div style="font-size: 32px; font-weight: bold;">3</div>
    </div>
    
    <div style="
        flex: 1;
        background: #25D366;
        color: white;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
    ">
        <h3>שורות</h3>
        <div style="font-size: 32px; font-weight: bold;">2</div>
    </div>
</div>

<div style="
    background: #f0f9ff;
    padding: 20px;
    border-radius: 10px;
    margin-top: 20px;
    border: 2px solid #bae6fd;
">
    <h4>🎯 Результат теста:</h4>
    <p><strong>Если видите два цветных блока РЯДОМ</strong> → ✅ Успех</p>
    <p><strong>Если блоки друг под другом</strong> → ❌ Провал</p>
</div>
'''

components.html(html, height=300)

st.write("---")
st.write("**Скажите мне:**")
st.write("1. Видите два цветных блока (синий и зеленый)?")
st.write("2. Они рядом или друг под другом?")

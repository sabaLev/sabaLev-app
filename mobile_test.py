import streamlit as st

st.title("Проверка мобильного")

st.write("Если видите этот текст на телефоне — ✅ работает")

# Простейший HTML для теста двух колонок
html = '''
<div style="
    display: flex; 
    gap: 10px; 
    margin: 20px 0;
    flex-direction: row;
">
    <div style="
        flex: 1;
        background: blue;
        color: white;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
    ">
        LEFT
    </div>
    <div style="
        flex: 1;
        background: green;
        color: white;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
    ">
        RIGHT
    </div>
</div>

<div style="
    background: yellow;
    padding: 15px;
    margin: 20px 0;
    border-radius: 10px;
">
    <strong>Результат:</strong>
    <div id="result">Проверяю...</div>
</div>

<script>
// Проверка на мобильном
function checkMobile() {
    const width = window.innerWidth;
    const result = document.getElementById('result');
    
    if (width < 768) {
        // Мобильный
        const flexDiv = document.querySelector('div[style*="display: flex"]');
        if (flexDiv && getComputedStyle(flexDiv).flexDirection === 'row') {
            result.innerHTML = "✅ УСПЕХ! На мобильном две колонки РЯДОМ";
            result.style.color = "green";
        } else {
            result.innerHTML = "❌ ПРОВАЛ! На мобильном колонки друг под другом";
            result.style.color = "red";
        }
    } else {
        result.innerHTML = "📱 Откройте на телефоне для теста";
        result.style.color = "blue";
    }
}

checkMobile();
window.addEventListener('resize', checkMobile);
</script>
'''

st.components.v1.html(html, height=300)

st.write("---")
st.write("**Скажите:**")
st.write("1. Видите синий и зеленый блок?")
st.write("2. Они рядом или друг под другом?")
st.write("3. Что написано в желтом блоке?")

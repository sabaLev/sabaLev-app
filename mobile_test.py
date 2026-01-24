import streamlit as st

st.markdown("""
<style>
/* Стиль как у колеса но с selectbox */
div[data-testid="stSelectbox"] > div {
    border-radius: 12px;
    border: 2px solid #007AFF;
    padding: 10px;
}

/* Для мобильных - увеличенные кнопки */
@media (max-width: 768px) {
    .stSelectbox > div {
        font-size: 20px;
        padding: 15px;
    }
    
    /* Скрываем стрелку выбора */
    .stSelectbox svg {
        display: none;
    }
}
</style>
""", unsafe_allow_html=True)

# Выпадающий список который выглядит как колесо
panels = st.selectbox(
    "פאנלים",
    options=[f"🔘 {i}" for i in range(1, 9)],
    format_func=lambda x: x.replace("🔘 ", "")
)

rows = st.selectbox(
    "שורות", 
    options=[f"📊 {i}" for i in range(0, 21)],
    format_func=lambda x: x.replace("📊 ", "")
)

st.write(f"בחרת: {panels.replace('🔘 ', '')} פאנלים, {rows.replace('📊 ', '')} שורות")

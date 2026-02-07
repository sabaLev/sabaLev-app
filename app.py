st.title("Тест лазейки №4: Beta-функции")

try:
    # Пробуем использовать vertical_alignment
    col1, col2 = st.columns([1, 3], vertical_alignment="center")
    
    with col1:
        cb = st.checkbox("", key="cb_beta", label_visibility="collapsed")
    
    with col2:
        st.markdown('<div style="text-align:right; padding:10px 0;">מהדק קצה</div>', unsafe_allow_html=True)
        
except Exception as e:
    st.error(f"Не поддерживается: {e}")

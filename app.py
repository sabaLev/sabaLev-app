import streamlit as st

st.title("➕➖ Простой счетчик в таблице")

# Инициализация
if 'counter' not in st.session_state:
    st.session_state.counter = 50

# Таблица с одной строкой
st.markdown("""
<style>
.simple-table {
    width: 300px;
    border-collapse: collapse;
    margin: 20px 0;
}
.simple-table td {
    padding: 15px;
    text-align: center;
    border: 2px solid #ddd;
    font-size: 18px;
}
.counter-btn {
    width: 40px;
    height: 40px;
    font-size: 20px;
    border: none;
    border-radius: 5px;
    cursor: pointer;
}
</style>

<table class="simple-table">
    <tr>
        <td>
            <button class="counter-btn" style="background:#ff6b6b; color:white;"
                    onclick="window.parent.postMessage({type: 'streamlit:setComponentValue', value: 'decrement'}, '*')">
                -
            </button>
        </td>
        <td style="font-weight:bold; font-size:24px;">
            <span id="counter-value">%d</span>
        </td>
        <td>
            <button class="counter-btn" style="background:#4ecdc4; color:white;"
                    onclick="window.parent.postMessage({type: 'streamlit:setComponentValue', value: 'increment'}, '*')">
                +
            </button>
        </td>
    </tr>
</table>

<script>
// Обновляем значение при изменении
function updateCounter() {
    document.getElementById('counter-value').textContent = %d;
}
updateCounter();
</script>
""" % (st.session_state.counter, st.session_state.counter))

# Обработка нажатий
action = st.text_input("", label_visibility="collapsed", key="action_input")
if action:
    if action == "increment":
        st.session_state.counter += 1
    elif action == "decrement":
        st.session_state.counter = max(0, st.session_state.counter - 1)
    st.rerun()

st.write(f"Текущее значение: **{st.session_state.counter}**")

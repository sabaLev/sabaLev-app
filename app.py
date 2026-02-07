import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode

st.title("🎯 Продвинутая таблица с Ag-Grid")

# Инициализация данных
if 'grid_data' not in st.session_state:
    st.session_state.grid_data = pd.DataFrame({
        'id': [1, 2, 3],
        'product': ['Ноутбук', 'Смартфон', 'Планшет'],
        'stock': [15, 42, 28],
        'price': [50000, 25000, 15000]
    })

# Настройка Ag-Grid
gb = GridOptionsBuilder.from_dataframe(st.session_state.grid_data)

# Настраиваем колонку "stock" с кнопками
gb.configure_column(
    'stock',
    headerName='На складе',
    cellRenderer='''
    function(params) {
        const container = document.createElement('div');
        container.style.display = 'flex';
        container.style.alignItems = 'center';
        container.style.justifyContent = 'center';
        container.style.gap = '10px';
        
        const minusBtn = document.createElement('button');
        minusBtn.innerText = '-';
        minusBtn.style.cssText = 'width: 25px; height: 25px; border-radius: 50%; border: none; background: #ff6b6b; color: white; cursor: pointer;';
        minusBtn.onclick = () => {
            params.data.stock = Math.max(0, params.data.stock - 1);
            params.api.applyTransaction({update: [params.data]});
        };
        
        const valueSpan = document.createElement('span');
        valueSpan.innerText = params.value;
        valueSpan.style.cssText = 'font-weight: bold; min-width: 30px; text-align: center;';
        
        const plusBtn = document.createElement('button');
        plusBtn.innerText = '+';
        plusBtn.style.cssText = 'width: 25px; height: 25px; border-radius: 50%; border: none; background: #4ecdc4; color: white; cursor: pointer;';
        plusBtn.onclick = () => {
            params.data.stock += 1;
            params.api.applyTransaction({update: [params.data]});
        };
        
        container.appendChild(minusBtn);
        container.appendChild(valueSpan);
        container.appendChild(plusBtn);
        
        return container;
    }
    ''',
    editable=False,
    width=150
)

# Настраиваем другие колонки
gb.configure_column('id', headerName='ID', width=80)
gb.configure_column('product', headerName='Товар', width=150)
gb.configure_column('price', headerName='Цена (₽)', width=120)

# Включаем обновление данных
gb.configure_grid_options(
    enableCellChangeFlash=True,
    animateRows=True
)

grid_options = gb.build()

# Отображаем таблицу
grid_response = AgGrid(
    st.session_state.grid_data,
    gridOptions=grid_options,
    update_mode=GridUpdateMode.VALUE_CHANGED,
    theme='streamlit',
    height=250,
    allow_unsafe_jscode=True
)

# Получаем обновленные данные
if grid_response['data'] is not None:
    updated_df = pd.DataFrame(grid_response['data'])
    
    # Сравниваем с исходными данными
    if not updated_df.equals(st.session_state.grid_data):
        st.session_state.grid_data = updated_df
        st.rerun()

# Показываем итоги
st.write("### 📊 Итоговая информация")
total_stock = st.session_state.grid_data['stock'].sum()
total_value = (st.session_state.grid_data['stock'] * st.session_state.grid_data['price']).sum()

col1, col2 = st.columns(2)
with col1:
    st.metric("Всего товаров на складе", f"{total_stock} шт.")
with col2:
    st.metric("Общая стоимость", f"{total_value:,.0f} ₽")

# Кнопка сброса
if st.button("🔄 Сбросить к исходным значениям"):
    st.session_state.grid_data['stock'] = [15, 42, 28]
    st.rerun()

# 1. Самый простой
value = st.slider("Выберите", 0, 100)

# 2. С диапазоном
range_val = st.slider("Диапазон", 0, 100, (25, 75))

# 3. С временем
from datetime import time
time_val = st.slider("Время", value=time(12, 0))

# 4. Select слайдер
select_val = st.select_slider("Выбор", options=[1, 2, 3, 4, 5])

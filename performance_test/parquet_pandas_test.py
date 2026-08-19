import pandas as pd
import time

start_time = time.time()

df = pd.read_parquet('datos/flights/flight_data_2024.parquet')
df = df[(df['month'] == 5) & 
        (df['origin'] == 'SFO') &
        (df['dest'] == 'SEA')][['month', 'origin','dest']]

print(df)
print(f"""\n\t *********************************\n\t
                 TIEMPO DE EJECUCION 
         --- {time.time() - start_time} segundos ---
        \n\t *********************************\n\t
        """)

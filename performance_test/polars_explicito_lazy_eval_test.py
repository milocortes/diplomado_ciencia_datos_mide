import polars as pl
import time

start_time = time.time()

q = (
    pl.read_csv('datos/flights/flight_data_2024.csv')
    .lazy()
    .select(['month', 'origin','dest'])
    .filter(
        (pl.col('month') == 5) & 
        (pl.col('origin') == 'SFO') &
        (pl.col('dest') == 'SEA'))
    )
df = q.collect()
print(df)
print(f"""\n\t *********************************\n\t
                 TIEMPO DE EJECUCION 
         --- {time.time() - start_time} segundos ---
        \n\t *********************************\n\t
        """)

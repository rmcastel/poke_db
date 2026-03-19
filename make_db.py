import pandas as pd
import numpy as np
import sqlite3
import os

conn=sqlite3.connect('pokemon.db')

for folder in os.listdir('./data'):
    print(folder)
    file=os.listdir(f'./data/{folder}')[-1]
    print(file)
    _df_=pd.read_csv(f'./data/{folder}/' + file,)
    print(_df_.shape)
    # print(file.split('_')[:2])

    _df_.to_sql(folder, conn, if_exists='replace', index=False,)
    print(f'WROTE: {folder}')
    print('='*100)

conn.close()

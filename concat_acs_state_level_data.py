
# -*- coding: utf-8 -*-

import os
import glob
import pandas as pd


base_dir = '/Users/Ikkei/columbia/capstone/data/ACS_Files'

data = {}
data_state = {}
states = glob.glob(os.path.join(base_dir, '*'))

for state_dir in states:
    files = [file for file in os.listdir(state_dir) if file.endswith('_with_ann.csv')]

    for file_nm in files:
        data_id = file_nm.split('_')[3]
        file_path = os.path.join(state_dir, file_nm)
        df = pd.read_csv(file_path, engine='python', header=[0, 1], dtype={1: str})

        cols = []
        for col in df.columns.get_level_values(1):
            new_name = (col.replace(' -', '_') 
                           .replace(' ', '_')
                           .replace(";", "")
                           .replace(":", "")
                           .replace(",", "")
                           .replace("'", "")
                           .replace('-', "_")
                           .replace('/', "_")
                           .replace('(', "")
                           .replace(')', "")
                           .replace('Id2', 'block_group_code')
                           .lower())
            cols.append(new_name)
        df.columns = cols

        state = state_dir.split('/')[-1]

        if data_id not in data:
            data[data_id] = [df]
            data_state[data_id] = [state]
        else:
            data[data_id].append(df)
            data_state[data_id].append(state)

tables = pd.read_csv('ACS Table Names.csv')

for k, v in data.items():
    try:
        df = pd.concat(data[k])
        table = tables[tables.table_id == k].table_name.iloc[0]
    except Exception:
        continue

    print(table, k, len(data[k]))
    path = os.path.join('/Users/Ikkei/columbia/capstone/data/combined', '{}.csv'.format(table))
    df.to_csv(path, index=False)

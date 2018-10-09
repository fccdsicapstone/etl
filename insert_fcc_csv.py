# -*- coding: utf-8 -*-

import io
import os

import calendar
import pandas as pd
import psycopg2


dsn = os.environ['DSN']
conn = psycopg2.connect(dsn)
curs = conn.cursor()

path_to_fcc = '/Users/Ikkei/columbia/capstone'
files = [f for f in os.listdir(path_to_fcc) if f.endswith('.csv')]

month_dict = dict((v.lower(), k) for k, v in enumerate(calendar.month_abbr))


def extract_file_date(filename):
    file_date = filename.split('_')[-2]

    month = month_dict[file_date[:-4]]
    year = file_date[-4:]

    return '{year}{month:02}'.format(year=year, month=month)


cols = ['log_rec_no',
        'provider_id',
        'frn',
        'provider_name',
        'dba_name',
        'holding_company_name',
        'hoco_num',
        'hoco_final',
        'state_abbr',
        'block_code',
        'tech_code',
        'consumer',
        'max_ad_down',
        'max_ad_up',
        'business',
        'max_cir_down',
        'max_cir_up']

chunksize = 10 ** 6

for file in files:
    print(file)

    for chunk in pd.read_csv(file, chunksize=chunksize, encoding='ISO-8859-1'):
        chunk.columns = cols
        chunk.insert(0, 'file_date', extract_file_date(file))

        print(chunk.shape)

        str_buf = io.StringIO()
        chunk.to_csv(str_buf, index=False, header=False, sep='\t')
        str_buf.seek(0)
        curs.copy_from(str_buf, 'raw.fcc', sep='\t')
        conn.commit()

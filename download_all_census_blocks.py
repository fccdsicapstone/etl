import requests
from bs4 import BeautifulSoup
import zipfile
import io
import os
import pandas as pd
import us


r = requests.request('get', 'https://www.fcc.gov/general/census-blocks-state')
soup = BeautifulSoup(r.content, 'lxml')
urls = [a['href'] for a in soup.find_all('a', href=True) if 'CSVFiles' in a.get('href')]

for url in urls:
    r = requests.get(url)
    z = zipfile.ZipFile(io.BytesIO(r.content))
    z.extractall('geo')

dfs = []
outside_mainland = {'Northern Mariana Isl': 'MP'}
for f in os.listdir('geo'):
    path = os.path.join(os.getcwd(), 'geo', f)
    state = f.split('.')[0]

    try:
        state_abbr = us.states.lookup(state).abbr
    except AttributeError:
        state_abbr = outside_mainland[state]

    df = pd.read_csv(path, dtype=str, engine='python')
    df['state_name'] = state
    df['state_abbr'] = state_abbr
    dfs.append(df)

data = pd.concat(dfs)
data.drop(columns=['tractname', 'block', 'tractcode'], inplace=True)
data.rename(columns={'state': 'state_code', 'county': 'county_code', 'cnamelong': 'county',
                     'tract': 'tract_code', 'blockcode': 'block_code', 'state_name': 'state'}, inplace=True)
data['state_county_code'] = data.state_code + data.county_code

cols = [
    'block_code',
    'state_county_code',
    'tract_code',
    'state_code',
    'county_code',
    'state_abbr',
    'state',
    'county',
]
data = data[cols]

mask = data.state_abbr.isin(['AK', 'HI', 'GU', 'MH', 'FM', 'MP', 'PW', 'PR', 'VI', 'AS'])
data = data[~mask]
data.to_csv('block_codes.csv', index=False)

import pandas as pd
import os
import numpy as np
import requests

def creation_db_sets(dir):
    response = requests.get('https://api.tcgdex.net/v2/en/sets', headers='')
    if response.status_code == 200:
        sets = response.json()  
        list_sets = []
        for set in sets:
            list_sets.append({'ID': set['id'], 'Name': set['name'], 'Card_Count': set['cardCount']['total']})
        df = pd.DataFrame(list_sets)
        df.to_excel(os.path.join(dir, f'sets.xlsx'), index=False)

#creation_db_sets('datasets')
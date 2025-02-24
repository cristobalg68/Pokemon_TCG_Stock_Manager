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

def creation_db_set(dir, set_id):
    response_1 = requests.get(f'https://api.tcgdex.net/v2/en/sets/{set_id}', headers='')
    if response_1.status_code == 200:
        set = response_1.json()  
        set_name = set['name'].replace(' ', '_')
        list_cards = []
        for card in set['cards']:
            card_id = card['id']
            response_2 = requests.get(f'https://api.tcgdex.net/v2/en/cards/{card_id}', headers='')
            if response_2.status_code == 200:
                info_card = response_2.json()
                print(info_card)
                list_cards.append({
                    'ID': card_id, 
                    'Local_ID': card['localId'], 
                    'Name': card['name'], 
                    'Rarity': info_card['rarity'],
                    'Firt_Edition': int(info_card['variants']['firstEdition']),
                    'Holo': int(info_card['variants']['holo']),
                    'Normal': int(info_card['variants']['normal']),
                    'Reverse': int(info_card['variants']['reverse']),
                    'Promo': int(info_card['variants']['wPromo']),
                    })
    df = pd.DataFrame(list_cards)
    df.to_excel(os.path.join(dir, f'cards_of_{set_name}.xlsx'), index=False)

#creation_db_set('datasets', 'sv08') # Surging Sparks
#creation_db_set('datasets', 'sv03.5') # 151
#creation_db_set('datasets', 'sv08.5') # Prismatic Evolutions

def creation_stock_db_set(dir, set_name):
    df_card = pd.read_excel(os.path.join(dir, f'cards_of_{set_name}.xlsx'))
    list_stock = []
    for _, row in df_card.iterrows():
        base = {
            'N': row['Local_ID'], 
            'Name': row['Name'], 
            'Rarity': row['Rarity']}
        for t in ['Firt_Edition', 'Holo', 'Normal', 'Reverse', 'Promo']:
            if row[t]:
                copy = base.copy()
                copy['Card_Type'] = t
                list_stock.append(copy)
    df_stock = pd.DataFrame(list_stock)
    df_stock['Quantity'] = 0
    df_stock.to_excel(os.path.join(dir, f'stock_of_{set_name}.xlsx'), index=False)

#creation_stock_db_set('datasets', 'Surging_Sparks')
#creation_stock_db_set('datasets', '151')
#creation_stock_db_set('datasets', 'Prismatic_Evolutions')
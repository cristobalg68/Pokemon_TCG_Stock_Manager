import pandas as pd
import os
import numpy as np
import json

def mixing_tables_stock(dir, set_name):
    df_products = pd.read_excel(os.path.join(dir, 'local_marketplace_products.xlsx'))
    df_products = df_products[df_products['Set_Name'] == set_name]

    set_name_file = set_name.lower().replace(' ', '_')
    df_stock = pd.read_excel(os.path.join(dir, f'stock_of_{set_name_file}.xlsx'))

    new_columns = {'Published_Quantity': [], 'Published_Price': [], 'Publication_Exists': []}
    for _, row in df_stock.iterrows():
        product = df_products[
            (df_products['N'] == row['N']) & 
            (df_products['Card_Type'] == row['Card_Type'])]
    
        if len(product) == 1:
            new_columns['Published_Quantity'].append(product.iloc[0]['Quantity'])
            new_columns['Published_Price'].append(product.iloc[0]['Price'])
            new_columns['Publication_Exists'].append(True)
        elif len(product) == 0:
            new_columns['Published_Quantity'].append(0)
            new_columns['Published_Price'].append(0)
            new_columns['Publication_Exists'].append(False)
        else:
            print(product)
    
    df_stock['Published_Quantity'] = new_columns['Published_Quantity']
    df_stock['Published_Price'] = new_columns['Published_Price']
    df_stock['Publication_Exists'] = new_columns['Publication_Exists']
    
    return df_stock

def mixing_tables_price(dir, set_name, df_mixed):
    with open(os.path.join(dir, 'RM_municipality.json'), 'r') as file:
        data = json.load(file)
    municipality_of_RM = data['comunas']

    set_name_file = set_name.lower().replace(' ', '_')
    df_offers = pd.read_excel(os.path.join(dir, f'local_marketplace_offers_pokemon_{set_name_file}.xlsx'))

    new_columns = {'Offers_Exists': [], 'Is_Excellent': [], 'In_English': [], 'Min_Offers_Price_in_RM': [], 'Min_Offers_Price_out_RM': []}
    for _, row in df_mixed.iterrows():

        offers = df_offers[
            (df_offers['N'] == row['N']) & 
            (df_offers['Card_Type'] == row['Card_Type'])]
        
        if len(offers) > 0:
            new_columns['Offers_Exists'].append(True)
            offers_en_excelent = offers[
                (offers['Language'] == 'Inglés') &
                (offers['State'] == 'Excelente (NM)')]
            
            if len(offers_en_excelent) > 0:
                new_columns['In_English'].append(True)
                new_columns['Is_Excellent'].append(True)
                offers_in_RM = offers_en_excelent[offers_en_excelent.Municipality.isin(municipality_of_RM)]         
                if len(offers_in_RM) > 0:
                    new_columns['Min_Offers_Price_in_RM'].append(offers_in_RM['Price'].min())
                else:
                    new_columns['Min_Offers_Price_in_RM'].append(-1)
                offers_out_RM = offers_en_excelent[~offers_en_excelent.Municipality.isin(municipality_of_RM)]
                if len(offers_out_RM) > 0:
                    new_columns['Min_Offers_Price_out_RM'].append(offers_out_RM['Price'].min())
                else:
                    new_columns['Min_Offers_Price_out_RM'].append(-1)
            else:
                offers_en_not_excelent = offers[
                    (offers['Language'] == 'Inglés') &
                    (offers['State'] != 'Excelente (NM)')]
                
                if len(offers_en_not_excelent) > 0:
                    new_columns['In_English'].append(True)
                    new_columns['Is_Excellent'].append(False)
                    offers_in_RM = offers_en_not_excelent[offers_en_not_excelent.Municipality.isin(municipality_of_RM)]
                    if len(offers_in_RM) > 0:
                        new_columns['Min_Offers_Price_in_RM'].append(offers_in_RM['Price'].min())
                    else:
                        new_columns['Min_Offers_Price_in_RM'].append(-1)
                    offers_out_RM = offers_en_not_excelent[~offers_en_not_excelent.Municipality.isin(municipality_of_RM)]
                    if len(offers_out_RM) > 0:
                        new_columns['Min_Offers_Price_out_RM'].append(offers_out_RM['Price'].min())
                    else:
                        new_columns['Min_Offers_Price_out_RM'].append(-1)
                else:
                    offers_not_en_excelent = offers[
                        (offers['Language'] != 'Inglés') &
                        (offers['State'] == 'Excelente (NM)')]
                    
                    if len(offers_not_en_excelent) > 0:
                        new_columns['In_English'].append(False)
                        new_columns['Is_Excellent'].append(True)
                        offers_in_RM = offers_not_en_excelent[offers_not_en_excelent.Municipality.isin(municipality_of_RM)]
                        if len(offers_in_RM) > 0:
                            new_columns['Min_Offers_Price_in_RM'].append(offers_in_RM['Price'].min())
                        else:
                            new_columns['Min_Offers_Price_in_RM'].append(-1)
                        offers_out_RM = offers_not_en_excelent[~offers_not_en_excelent.Municipality.isin(municipality_of_RM)]
                        if len(offers_out_RM) > 0:
                            new_columns['Min_Offers_Price_out_RM'].append(offers_out_RM['Price'].min())
                        else:
                            new_columns['Min_Offers_Price_out_RM'].append(-1)
                    else:
                        offers_not_en_not_excelent = offers[
                            (offers['Language'] != 'Inglés') &
                            (offers['State'] != 'Excelente (NM)')]
                        
                        if len(offers_not_en_not_excelent) > 0:
                            new_columns['In_English'].append(False)
                            new_columns['Is_Excellent'].append(False)
                            offers_in_RM = offers_not_en_not_excelent[offers_not_en_not_excelent.Municipality.isin(municipality_of_RM)]
                            if len(offers_in_RM) > 0:
                                new_columns['Min_Offers_Price_in_RM'].append(offers_in_RM['Price'].min())
                            else:
                                new_columns['Min_Offers_Price_in_RM'].append(-1)
                            offers_out_RM = offers_not_en_not_excelent[~offers_not_en_not_excelent.Municipality.isin(municipality_of_RM)]
                            if len(offers_out_RM) > 0:
                                new_columns['Min_Offers_Price_out_RM'].append(offers_out_RM['Price'].min())
                            else:
                                new_columns['Min_Offers_Price_out_RM'].append(-1)
        else:
            new_columns['Offers_Exists'].append(False)
            new_columns['In_English'].append(False)
            new_columns['Is_Excellent'].append(False)
            new_columns['Min_Offers_Price_in_RM'].append(-1)
            new_columns['Min_Offers_Price_out_RM'].append(-1)

    df_mixed['Offers_Exists'] = new_columns['Offers_Exists']
    df_mixed['In_English'] = new_columns['In_English']
    df_mixed['Is_Excellent'] = new_columns['Is_Excellent']
    df_mixed['Min_Offers_Price_in_RM'] = new_columns['Min_Offers_Price_in_RM']
    df_mixed['Min_Offers_Price_out_RM'] = new_columns['Min_Offers_Price_out_RM']
    
    return df_mixed

def generate_suggestion(row):
    if not row['Offers_Exists']:
        return "No offer available."
    
    parts = []
    
    if row['In_English']:
        parts.append("English")
    
    if row['Is_Excellent']:
        parts.append("Excellent")
    
    if row['Min_Offers_Price_in_RM'] != -1:
        parts.append(f"The minimum price within the RM is {row['Min_Offers_Price_in_RM']}")
    
    if row['Min_Offers_Price_out_RM'] != -1:
        parts.append(f"Outside the RM is {row['Min_Offers_Price_out_RM']}")
    
    return " / ".join(parts)

def analysis(df):
    df['diff'] = df['Quantity'] - df['Published_Quantity']
    unpublished = df[df['Publication_Exists'] == False]
    published = df[df['Publication_Exists'] == True]

    print('Correct Publication Stock')
    for _, row in published.iterrows():
        if row['diff'] < 0:
            price_suggestion = generate_suggestion(row)
            print('Name: {} / Card Type: {} / Stock Quantity: {} / Price Suggestion: {}'.format(row['Name'], row['Card_Type'], row['Quantity'], price_suggestion))

    print('Update Publication Stock')
    for _, row in published.iterrows():  
        if row['diff'] > 0:
            price_suggestion = generate_suggestion(row)
            print('Name: {} / Card Type: {} / Stock Quantity: {} / Price Suggestion: {}'.format(row['Name'], row['Card_Type'], row['Quantity'], price_suggestion))

    print('Create Publication')
    for _, row in unpublished.iterrows():
        if row['diff'] != 0:
            price_suggestion = generate_suggestion(row)
            print('Name: {} / Card Type: {} / Stock Quantity: {} / Price Suggestion: {}'.format(row['Name'], row['Card_Type'], row['Quantity'], price_suggestion))

def main(dir, set_name):
    df_mixed = mixing_tables_stock(dir, set_name)
    df_mixed = mixing_tables_price(dir, set_name, df_mixed)
    analysis(df_mixed)

if __name__ == "__main__":
    dir = 'datasets'
    set_name = 'Prismatic Evolutions' #Prismatic Evolutions
    main(dir, set_name)
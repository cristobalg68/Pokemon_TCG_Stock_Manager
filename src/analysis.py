import pandas as pd
import os

def mixing_tables(dir, set_name):
    df_products = pd.read_excel(os.path.join(dir, 'local_marketplace_products.xlsx'))
    df_stock = pd.read_excel(os.path.join(dir, f'stock_of_{set_name}.xlsx'))

    new_columns = {'Published_Quantity': [], 'Published_Price': [], 'Publication_Exists': []}
    for _, row in df_stock.iterrows():
        product = df_products[
            (df_products['Name'] == row['Name']) & 
            (df_products['Set_Name'] == set_name) & 
            (df_products['Card_Type'] == row['Card_Type'])]
    
        if len(product) > 0:
            new_columns['Published_Quantity'].append(product.iloc[0]['Quantity'])
            new_columns['Published_Price'].append(product.iloc[0]['Price'])
            new_columns['Publication_Exists'].append(True)
        else:
            new_columns['Published_Quantity'].append(0)
            new_columns['Published_Price'].append(0)
            new_columns['Publication_Exists'].append(False)
    
    df_stock['Published_Quantity'] = new_columns['Published_Quantity']
    df_stock['Published_Price'] = new_columns['Published_Price']
    df_stock['Publication_Exists'] = new_columns['Publication_Exists']
    
    return df_stock

def analysis(df):
    df['diff'] = df['Quantity'] - df['Published_Quantity']
    df = df[df['diff'] != 0]
    unpublished = df[df['Publication_Exists'] == False]
    published = df[df['Publication_Exists'] == True]

    print('Update Publication')
    for _, row in published.iterrows():
        print('Name: {} / Card Type: {} / Stock Quantity: {}'.format(row['Name'], row['Card_Type'], row['Quantity']))

    print('Create Publication')
    for _, row in unpublished.iterrows():
        print('Name: {} / Card Type: {} / Stock Quantity: {}'.format(row['Name'], row['Card_Type'], row['Quantity']))

def main(dir, set_name):
    df_mixed = mixing_tables(dir, set_name)
    analysis(df_mixed)

if __name__ == "__main__":
    dir = 'datasets'
    set_name = '151'
    main(dir, set_name)
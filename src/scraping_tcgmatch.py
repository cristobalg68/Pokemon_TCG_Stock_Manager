from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pandas as pd
import numpy as np
import os

def launch_browser():
    options = webdriver.ChromeOptions()
    options.add_argument("start-maximized")
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    options.page_load_strategy = 'normal'
    driver = webdriver.Chrome(options=options)
    return driver

def get_products(driver):
    products = []
    driver.get('https://tcgmatch.cl/mi-cuenta/productos')
    time.sleep(2.5)
    while True:
        table = driver.find_elements(By.CSS_SELECTOR, '#__next > div.mx-auto.flex.w-full.items-start.bg-gray-50.divide-x > main > main > div.mt-4.ring-1.ring-black.ring-opacity-5 > div.divide-y.divide-gray-200.bg-white > div')

        for i in range(len(table)):
            language = driver.find_element(By.CSS_SELECTOR, f'#__next > div.mx-auto.flex.w-full.items-start.bg-gray-50.divide-x > main > main > div.mt-4.ring-1.ring-black.ring-opacity-5 > div.divide-y.divide-gray-200.bg-white > div:nth-child({i+1}) > div:nth-child(3)').text
            state = driver.find_element(By.CSS_SELECTOR, f'#__next > div.mx-auto.flex.w-full.items-start.bg-gray-50.divide-x > main > main > div.mt-4.ring-1.ring-black.ring-opacity-5 > div.divide-y.divide-gray-200.bg-white > div:nth-child({i+1}) > div:nth-child(4)').text
            quantity = driver.find_element(By.CSS_SELECTOR, f'#__next > div.mx-auto.flex.w-full.items-start.bg-gray-50.divide-x > main > main > div.mt-4.ring-1.ring-black.ring-opacity-5 > div.divide-y.divide-gray-200.bg-white > div:nth-child({i+1}) > div:nth-child(5)').text
            price = driver.find_element(By.CSS_SELECTOR, f'#__next > div.mx-auto.flex.w-full.items-start.bg-gray-50.divide-x > main > main > div.mt-4.ring-1.ring-black.ring-opacity-5 > div.divide-y.divide-gray-200.bg-white > div:nth-child({i+1}) > div:nth-child(6)').text

            url_edit = driver.find_element(By.CSS_SELECTOR, f'#__next > div.mx-auto.flex.w-full.items-start.bg-gray-50.divide-x > main > main > div.mt-4.ring-1.ring-black.ring-opacity-5 > div.divide-y.divide-gray-200.bg-white > div:nth-child({i+1}) > div:nth-child(9) > div > a:nth-child(1)').get_attribute('href')
            
            driver.execute_script("window.open('');") 
            driver.switch_to.window(driver.window_handles[1]) 
            driver.get(url_edit)
            time.sleep(2.5)

            try:
                name = driver.find_element(By.CSS_SELECTOR, f'#__next > div:nth-child(4) > main > form > div > div > div > div.px-4.py-5.sm\:p-6.flex.flex-col.md\:flex-row.justify-around > div.text-center > h4:nth-child(2)').text
                set_name = driver.find_element(By.CSS_SELECTOR, '#__next > div:nth-child(4) > main > form > div > div > div > div.px-4.py-5.sm\:p-6.flex.flex-col.md\:flex-row.justify-around > div.text-center > h4:nth-child(3)').text
                num = driver.find_element(By.CSS_SELECTOR, '#__next > div:nth-child(4) > main > form > div > div > div > div.px-4.py-5.sm\:p-6.flex.flex-col.md\:flex-row.justify-around > div.text-center > h4:nth-child(4)').text
                product_type = 0
            except:
                name = driver.find_element(By.CSS_SELECTOR, f'#name').get_attribute('value')
                card_type = np.nan
                set_name = np.nan
                num = np.nan

                try:
                    accessory_type = driver.find_element(By.CSS_SELECTOR, '#accessoryType')
                    product_type = 2
                except:
                    product_type = 1

            driver.close()
            driver.switch_to.window(driver.window_handles[0])

            if product_type == 0:
                try:
                    card_type = driver.find_element(By.CSS_SELECTOR, f'#__next > div.mx-auto.flex.w-full.items-start.bg-gray-50.divide-x > main > main > div.mt-4.ring-1.ring-black.ring-opacity-5 > div.divide-y.divide-gray-200.bg-white > div:nth-child({i+1}) > div:nth-child(2) > div > div > span').text
                except:
                    card_type = 'Normal'
            item = {'Name': name, 
                    'Language': language, 
                    'State': state, 
                    'Quantity': quantity, 
                    'Price': price, 
                    'Product_Type': product_type, 
                    'Card_Type': card_type,
                    'Set_Name': set_name,
                    'N': num}
            products.append(item)

        if len(table) < 10:
            break
        else:
            try:
                driver.find_element(By.CSS_SELECTOR, '#__next > div.mx-auto.flex.w-full.items-start.bg-gray-50.divide-x > main > main > nav > div.flex.flex-1.justify-between.sm\:justify-end > button.relative.ml-3.inline-flex.items-center.rounded-md.bg-white.px-3.py-2.text-sm.font-semibold.text-gray-900.ring-1.ring-inset.ring-gray-300.hover\:bg-gray-50.focus-visible\:outline-offset-0').click()
                time.sleep(2.5)
            except:
                break
    
    return products

def update_stock(products, dir):
    df = pd.DataFrame(products)
    df['Quantity'] = df['Quantity'].astype(int)
    df['Price'] = df['Price'].apply(lambda x: int(x[1:-4].replace('.','')))
    df['N'] = df['N'].apply(lambda x: x[:-4] if type(x) == str else x)
    df['Card_Type'] = df['Card_Type'].apply(lambda x: x.replace('Holo Reverse','Reverse') if type(x) == str else x)
    df.to_excel(os.path.join(dir, 'local_marketplace_products.xlsx'), index=False)

def get_offer(driver):
    total_cards = driver.find_element(By.CSS_SELECTOR, '#__next > div:nth-child(4) > main > nav > div.mb-3.md\:mb-0.sm\:block > p > span:nth-child(3)').text
    pages = int(total_cards)//24 + 1

    reviewed = {}
    for _ in range(int(pages)):
        sup_index = driver.find_elements(By.CSS_SELECTOR, '#__next > div:nth-child(4) > main > nav > div.mb-3.md\:mb-0.sm\:block > p > span:nth-child(2)')[0].text
        sub_index = driver.find_elements(By.CSS_SELECTOR, '#__next > div:nth-child(4) > main > nav > div.mb-3.md\:mb-0.sm\:block > p > span:nth-child(1)')[0].text
        num_items_in_page = int(sup_index) - int(sub_index) + 1

        for i in range(num_items_in_page):
            name = driver.find_elements(By.CSS_SELECTOR, fr'#__next > div:nth-child(4) > main > div > div > div.lg\:grid.lg\:grid-cols-3.lg\:gap-x-8.xl\:grid-cols-9.\32 xl\:grid-cols-10 > section > div > a:nth-child({i+1}) > div.col-span-6.flex.flex-col.text-left > p.text-base.font-semibold')[0].text
            set_name = driver.find_elements(By.CSS_SELECTOR, fr'#__next > div:nth-child(4) > main > div > div > div.lg\:grid.lg\:grid-cols-3.lg\:gap-x-8.xl\:grid-cols-9.\32 xl\:grid-cols-10 > section > div > a:nth-child({i+1}) > div.col-span-6.flex.flex-col.text-left > p:nth-child(3)')[0].text
            num = driver.find_elements(By.CSS_SELECTOR, fr'#__next > div:nth-child(4) > main > div > div > div.lg\:grid.lg\:grid-cols-3.lg\:gap-x-8.xl\:grid-cols-9.\32 xl\:grid-cols-10 > section > div > a:nth-child({i+1}) > div.col-span-6.flex.flex-col.text-left > p:nth-child(4)')[0].text
            item_id = name + set_name + num
            if item_id not in reviewed:
                reviewed[item_id] = {}
                driver.find_element(By.CSS_SELECTOR, fr'#__next > div:nth-child(4) > main > div > div > div.lg\:grid.lg\:grid-cols-3.lg\:gap-x-8.xl\:grid-cols-9.\32 xl\:grid-cols-10 > section > div > a:nth-child({i+1})').click()
                time.sleep(2.5)

                offers = []
                try:
                    items = driver.find_elements(By.CSS_SELECTOR, '#others > ul > li')
                    in_stock = True
                    for _ in range(len(items)):
                        price = driver.find_element(By.CSS_SELECTOR, f'#others > ul > li:nth-child({i+1}) > div:nth-child(2) > p.text-green-800.font-semibold.text-center.lg\:text-left').text
                        state = driver.find_element(By.CSS_SELECTOR, f'#others > ul > li:nth-child({i+1}) > div:nth-child(2) > p.text-sm.font-light.text-center.lg\:text-left').text
                        try:
                            card_type = driver.find_element(By.CSS_SELECTOR, f'#others > ul > li:nth-child({i+1}) > div:nth-child(2) > div > span.inline-flex.items-center.rounded-full.bg-blue-50.px-2.py-1.text-xs.font-medium.text-blue-700.ring-1.ring-inset.ring-blue-700\/10').text
                        except:
                            card_type = 'Normal'
                        quantity = driver.find_element(By.CSS_SELECTOR, f'#others > ul > li:nth-child({i+1}) > div:nth-child(3) > p').text
                        try:
                            municipality = driver.find_element(By.CSS_SELECTOR, f'#others > ul > li:nth-child({i+1}) > div.flex.flex-row.items-center.gap-3 > div > a > div > p').text
                        except:
                            municipality = 'None'
                        language = driver.find_element(By.CSS_SELECTOR, f'#others > ul > li:nth-child({i+1}) > div:nth-child(2) > div > span.inline-flex.items-center.rounded-full.bg-yellow-50.px-2.py-1.text-xs.font-medium.text-yellow-800.ring-1.ring-inset.ring-yellow-600\/20').text
                        offers.append({'price': price, 'state': state, 'language': language, 'card_type': card_type, 'quantity': quantity, 'municipality': municipality})
                except:
                    in_stock = False

                reviewed[item_id]['Name'] = name
                reviewed[item_id]['Set_Name'] = set_name
                reviewed[item_id]['N'] = num
                reviewed[item_id]['In_Stock'] = in_stock
                reviewed[item_id]['Offers'] = offers

                driver.back()
    
        try:
            driver.find_element(By.CSS_SELECTOR, '#__next > div:nth-child(4) > main > nav > div.flex.flex-1.justify-between.sm\:justify-end > button.relative.ml-3.inline-flex.items-center.rounded-md.bg-white.px-3.py-2.text-sm.font-semibold.text-gray-900.ring-1.ring-inset.ring-gray-300.hover\:bg-gray-50.focus-visible\:outline-offset-0').click()
            time.sleep(2.5)
        except:
            break

    return reviewed

def order_offer(products, dir, TCG, set_name):
    processed_products = []
    for _, item in products.items():
        if item['In_Stock']:
            for offer in item['Offers']:
                processed_products.append({
                    'Name': item['Name'],
                    'Set_Name': item['Set_Name'],
                    'N': item['N'],
                    'Price': offer['price'],
                    'State': offer['state'],
                    'Card_Type': offer['card_type'],
                    'Quantity': offer['quantity'],
                    'Municipality': offer['municipality'],
                    'Language': offer['language']
                    })

    set_name_file = set_name.replace(' ', '_')
    df = pd.DataFrame(processed_products)
    df['N'] = df['N'].apply(lambda x: int(x[:-4]))
    df['Price'] = df['Price'].apply(lambda x: int(x[1:-4].replace('.','')))
    df['State'] = df['State'].apply(lambda x: x.replace('Estado: ',''))
    df['Card_Type'] = df['Card_Type'].apply(lambda x: x.replace('Holo Reverse','Reverse'))
    df['Quantity'] = df['Quantity'].apply(lambda x: int(x.replace('Cantidad disponible: ','')))
    df.to_excel(os.path.join(dir, f'local_marketplace_offers_{TCG}_{set_name_file}.xlsx'), index=False)

def main_personal_stock(dir):
    url_login = ''

    driver = launch_browser()
    driver.get(url_login)
    time.sleep(1.5)

    products = get_products(driver)
    update_stock(products, dir)
    driver.quit()

def main_marketplace_stock(dir, TCG, set_name):
    set_name_page = set_name.lower().replace(' ', '-')
    url = f'https://tcgmatch.cl/cartas/busqueda/tcg={TCG}&edicion={set_name_page}'

    driver = launch_browser()
    driver.get(url)
    time.sleep(1.5)

    products = get_offer(driver)
    order_offer(products, dir, TCG, set_name)
    driver.quit

if __name__ == "__main__":
    dir = 'datasets'
    set_name = 'Prismatic Evolutions'
    #main_personal_stock(dir)
    main_marketplace_stock(dir, 'pokemon', set_name)
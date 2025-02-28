from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
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
            time.sleep(1.5)

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
                driver.find_element(By.CSS_SELECTOR, "#__next > div.mx-auto.flex.w-full.items-start.bg-gray-50.divide-x > main > main > nav > div.flex.flex-1.justify-between.sm\:justify-end > button.relative.ml-3.inline-flex.items-center.rounded-md.bg-white.px-3.py-2.text-sm.font-semibold.text-gray-900.ring-1.ring-inset.ring-gray-300.hover\:bg-gray-50.focus-visible\:outline-offset-0").click()
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

def main(dir):
    url_login = ""

    driver = launch_browser()
    driver.get(url_login)
    time.sleep(1.5)

    products = get_products(driver)
    update_stock(products, dir)
    driver.quit()

if __name__ == "__main__":
    dir = 'datasets'
    main(dir)
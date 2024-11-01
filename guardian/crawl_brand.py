from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
import json
from concurrent.futures import ThreadPoolExecutor

def fetch_products(link):
    driver = webdriver.Chrome(service=Service('chromedriver-win64/chromedriver.exe'))
    url = 'https://www.guardian.com.vn/shopby/' + link['k']
    driver.get(url)
    time.sleep(1)

    products = driver.find_elements(By.CSS_SELECTOR, 'a.product-item-link')

    product_data = []
    for product in products:
        product_name = product.text
        product_link = product.get_attribute('href')
        product_data.append({
            'name': product_name,
            'link': product_link
        })

    driver.quit()  

  
    with open('products-link.json', 'a', encoding='utf-8') as f:
        json.dump(product_data, f, ensure_ascii=False, indent=4)
        f.write("\n")  
    print(f'Data from {url} saved.')
    return product_data


with open('brand.json', 'r', encoding='utf-8') as f:
    brand_name = json.load(f)

with ThreadPoolExecutor(max_workers=5) as executor:
    list(executor.map(fetch_products, brand_name))
